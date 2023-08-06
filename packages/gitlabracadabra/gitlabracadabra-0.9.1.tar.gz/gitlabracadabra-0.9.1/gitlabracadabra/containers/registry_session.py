# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2021 Mathieu Parent <math.parent@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.request import parse_http_list, parse_keqv_list

from requests import Response, Session, codes
from requests.structures import CaseInsensitiveDict

from gitlabracadabra.auth_info import AuthInfo
from gitlabracadabra.containers.const import DOCKER_HOSTNAME, DOCKER_REGISTRY
from gitlabracadabra.containers.scope import Scope, all_scopes


if TYPE_CHECKING:
    from typing import Any, Dict, List, MutableMapping, Optional, Tuple

    from requests.auth import AuthBase


class RegistrySession(object):
    """Container registry HTTP methods."""

    def __init__(self, hostname: str, auth_info: Optional[AuthInfo] = None) -> None:
        """Instanciate a registry connection.

        Args:
            hostname: fqdn of a registry.
            auth_info: Authentication information.
        """
        if hostname == DOCKER_HOSTNAME:
            self._hostname = DOCKER_REGISTRY
        else:
            self._hostname = hostname
        self._auth_info = auth_info or AuthInfo()
        self._scheme = 'https'
        self._session = Session()
        self._session.headers = CaseInsensitiveDict({'Docker-Distribution-Api-Version': 'registry/2.0'})
        self._tokens: Dict[Scope, Optional[str]] = {}
        # Cache where blobs are present
        # Key is digest, value is a list of manifest names
        # Used in WithBlobs
        self._blobs: Dict[str, List[str]] = {}

    def __del__(self) -> None:  # noqa:WPS603
        """Destroy a registry connection."""
        self._session.close()

    @property
    def hostname(self) -> str:
        """Get hostname.

        Returns:
            The registry hostname.
        """
        if self._hostname == DOCKER_REGISTRY:
            return DOCKER_HOSTNAME
        return self._hostname

    def request(  # noqa:WPS211
        self,
        method: str,
        url: str,
        *,
        scope: Optional[Scope] = None,  # noqa: E1136
        params: Optional[MutableMapping[str, str]] = None,  # noqa: WPS110
        data: Any = None,  # noqa: E1136,WPS110
        headers: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None,  # noqa: E1136
        accept: Optional[Tuple[str, ...]] = None,  # noqa: E1136
        auth: Optional[AuthBase] = None,
        stream: Optional[bool] = None,  # noqa: E1136
        raise_for_status: bool = True,
    ) -> Response:
        """Send an HTTP GET request.

        Args:
            method: HTTP method.
            url: Either a path or a full url.
            scope: A scope.
            params: query string params.
            data: Request body stream.
            headers: Request headers.
            content_type: Uploaded MIME type.
            accept: An optional list of accepted mime-types.
            auth: HTTPBasicAuth.
            stream: Stream the response.
            raise_for_status: Raises `requests.HTTPError`, if one occurred.

        Returns:
            A Response.
        """
        if url.startswith('/'):
            url = '{0}://{1}{2}'.format(self._scheme, self._hostname, url)
        if headers:
            headers = headers.copy()
        else:
            headers = {}
        if accept:
            headers['Accept'] = ', '.join(accept)
        if content_type:
            headers['Content-Type'] = content_type

        self._connect(scope)
        response = self._session.request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            stream=stream,
        )
        if raise_for_status:
            response.raise_for_status()
        return response

    def _connect(self, scope: Optional[Scope]) -> None:
        """Connect.

        Args:
            scope: A scope.
        """
        if scope is None or all_scopes in self._tokens:
            self._set_session_auth()
            return
        elif scope in self._tokens:
            self._set_session_auth(token=self._tokens.get(scope))
            return
        response = self.request('get', '/v2/', raise_for_status=False)
        if response.status_code == codes['ok']:
            self._tokens[all_scopes] = None
            return
        if response.status_code == codes['unauthorized']:
            if response.headers['Www-Authenticate'].startswith('Bearer '):
                self._get_bearer_token(response, scope)
                self._set_session_auth(token=self._tokens.get(scope))
                return
        response.raise_for_status()

    def _set_session_auth(self, token: Optional[str] = None) -> None:  # noqa:E1136
        if token is None:
            if 'Authorization' in self._session.headers:
                self._session.headers.pop('Authorization')
        else:
            self._session.headers['Authorization'] = 'Bearer {0}'.format(token)

    def _get_bearer_token(self, response: Response, scope: Scope) -> None:
        _, _, challenge = response.headers['Www-Authenticate'].partition('Bearer ')
        challenge_parameters = parse_keqv_list(parse_http_list(challenge))
        get_params = {}
        if 'service' in challenge_parameters:
            get_params['service'] = challenge_parameters.get('service', 'unknown')
        get_params['scope'] = 'repository:{0}:{1}'.format(scope.remote_name, scope.actions)
        response = self.request(
            'get',
            challenge_parameters['realm'],
            params=get_params,
            headers=self._auth_info.headers,
            auth=self._auth_info.auth,
        )
        json = response.json()
        self._tokens[scope] = json.get('token', json.get('access_token'))
