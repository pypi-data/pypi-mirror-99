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

from typing import Dict, List, Optional

from gitlab import Gitlab

from requests.auth import HTTPBasicAuth

from gitlabracadabra.auth_info import AuthInfo
from gitlabracadabra.singleton import SingletonMeta


class GitlabConnections(object, metaclass=SingletonMeta):
    """All GitLab connections by id."""

    def __init__(self) -> None:
        """All connected GitLabs.

        Intented to be used as a singleton.
        """
        self._default_id: Optional[str] = None
        self._config_files: Optional[List[str]] = None
        self._debug: bool = False
        self._gitlabs: Dict[Optional[str], Gitlab] = {}

    def load(self, default_id: Optional[str], config_files: Optional[List[str]], debug: bool) -> None:
        """Load configuration.

        Args:
            default_id: Default gitlab id.
            config_files: None or list of configuration files.
            debug: True to enable debugging.
        """
        self._default_id = default_id
        self._config_files = config_files
        self._debug = debug
        self._gitlabs = {}

    def get_gitlab(self, gitlab_id: Optional[str] = None) -> Gitlab:
        """Get a GitLab connection.

        Args:
            gitlab_id: Section in python-gitlab config files.

        Returns:
            A GitLab connection.
        """
        if gitlab_id is None:
            gitlab_id = self._default_id
        if self._gitlabs.get(gitlab_id) is None:
            self._gitlabs[gitlab_id] = self._create(gitlab_id)
        return self._gitlabs[gitlab_id]

    def get_auth_info(self, gitlab_id: Optional[str]) -> AuthInfo:
        """Get Authentication information for a GitLab connection.

        Args:
            gitlab_id: Section in python-gitlab config files.

        Returns:
            A dict, with 'headers' and 'auth' to pass to requests.

        Raises:
            ValueError: No auth info.
        """
        gl = self.get_gitlab(gitlab_id)
        if gl.private_token:
            return AuthInfo(auth=HTTPBasicAuth('personal-access-token', gl.private_token))
        if gl.oauth_token:
            return AuthInfo(auth=HTTPBasicAuth('oauth2', gl.oauth_token))
        if gl.job_token:
            return AuthInfo(auth=HTTPBasicAuth('gitlab-ci-token', gl.job_token))
        if gl.http_username:
            return AuthInfo(auth=HTTPBasicAuth(gl.http_username, gl.http_password))
        raise ValueError('No auth info')

    def _create(self, gitlab_id: Optional[str]) -> Gitlab:
        """Instanciate a GitLab connection.

        Args:
            gitlab_id: Section in python-gitlab config files.

        Returns:
            A new GitLab connection.
        """
        gl = Gitlab.from_config(gitlab_id, self._config_files)
        if gl.private_token or gl.oauth_token:
            gl.auth()
        if self._debug:
            gl.enable_debug()
        return gl
