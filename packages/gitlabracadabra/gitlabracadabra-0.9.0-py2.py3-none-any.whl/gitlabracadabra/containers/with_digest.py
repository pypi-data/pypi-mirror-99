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

from hashlib import sha256
from os import rename
from os.path import getsize, isfile
from shutil import copyfileobj
from typing import TYPE_CHECKING, Any, BinaryIO, Optional, Tuple
from urllib.parse import quote

from requests import HTTPError, Response, codes

from gitlabracadabra.containers.const import DIGEST_HEADER
from gitlabracadabra.containers.scope import PULL, Scope
from gitlabracadabra.disk_cache import cache_dir


if TYPE_CHECKING:
    from gitlabracadabra.containers.registry_importer import RegistryImporter


class WithDigest(object):  # noqa:WPS214
    """An object with a digest."""

    supported_mime_types: Optional[Tuple[str, ...]] = None

    def __init__(  # noqa:WPS211
        self,
        registry: RegistryImporter,
        manifest_name: str,
        digest: Optional[str] = None,
        *,
        size: Optional[int] = None,
        mime_type: Optional[str] = None,
    ) -> None:
        """Initialize an object with a digest.

        Args:
            registry: Registry.
            manifest_name: Manifest name (Example: library/debian).
            digest: Digest (Example: sha256:5890f8ba95f680c87fcf89e51190098641b4f646102ce7ca906e7f83c84874dc).
            size: Size (Example: 42).
            mime_type: Content-Type / mediaType.
        """
        self._registry = registry
        self._manifest_name = manifest_name
        self._digest = digest
        self._size = size
        self._mime_type = mime_type
        self._exists: Optional[bool] = None
        self._fd: Optional[BinaryIO] = None

    def __eq__(self, other: Any) -> bool:
        """Compare.

        Args:
            other: Compare

        Returns:
            True if registry, manifest name, digest, size and mime_types are equal.
        """
        return (
            type(self) == type(other) and  # noqa: WPS516
            self.__dict__ == other.__dict__  # noqa: WPS609
        )

    @property
    def registry(self) -> RegistryImporter:
        """Get the registry.

        Returns:
            The registry.
        """
        return self._registry

    @property
    def manifest_name(self) -> str:
        """Get the manifest name.

        Returns:
            The manifest name.
        """
        return self._manifest_name

    @property
    def digest(self) -> str:
        """Get the digest.

        Returns:
            The digest.

        Raises:
            ValueError: Unable to get digest.
        """
        if self._digest is None:
            self._retrieve()
        if self._digest is None:
            raise ValueError('Unable to get digest')
        return self._digest

    @property
    def size(self) -> int:
        """Get the size.

        Returns:
            The size.

        Raises:
            ValueError: Unable to get size.
        """
        if self._size is None:
            try:
                self._size = getsize(self.cache_path)
            except FileNotFoundError:
                self._retrieve()
        if self._size is None:
            raise ValueError('Unable to get size')
        return self._size

    @property
    def mime_type(self) -> Optional[str]:
        """Get the MIME type (mediaType).

        Returns:
            The MIME type.
        """
        if self._mime_type is None:
            self._retrieve()
        return self._mime_type

    @property
    def cache_path(self) -> str:
        """Get the cache path (local).

        Returns:
            Local path.
        """
        return str(cache_dir('containers_cache') / quote(self.digest, safe=''))

    @property
    def registry_path(self) -> str:
        """Get the registry path.

        Raises:
            NotImplementedError: Needs to be implemented in subclasses.
        """
        raise NotImplementedError

    def __enter__(self) -> WithDigest:
        """Open the cached file.

        Returns:
            self.

        Raises:
            RuntimeError: File already opened.
        """
        self._ensure_cached()
        if self._fd is not None:
            raise RuntimeError('File already opened')
        self._fd = open(self.cache_path, 'rb')  # noqa:WPS515
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """Close the cached file.

        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        if self._fd is not None:
            self._fd.close()
            self._fd = None

    def read(self, n: int = -1) -> bytes:  # noqa: WPS111
        """Read the cached file.

        Args:
            n: buffer size.

        Returns:
            Bytes.

        Raises:
            ValueError: File is not opened.
        """
        if self._fd is None:
            raise ValueError('File is not opened')
        return self._fd.read(n)

    def scope(self, actions: str = PULL) -> Scope:
        """Get a scope.

        Args:
            actions: Scope action.

        Returns:
            A scope.
        """
        return Scope(self.manifest_name, actions)

    def exists(self) -> bool:  # noqa: WPS231
        """Get Blob/Manifest existence in the associated registry.

        Returns:
            True or False.

        Raises:
            HTTPError: Error when fetching existence.
        """
        if self._exists is None:
            try:  # noqa:WPS229
                self._retrieve()
                self._exists = True
                self.register()
            except HTTPError as err:
                if err.response.status_code != codes['not_found']:
                    raise err
                self._exists = False
        return self._exists

    def register(self) -> None:
        """Notify the registry that the Digest exists."""
        # Overridden in Blob

    def _ensure_cached(self) -> None:
        if not isfile(self.cache_path):
            self._retrieve(with_content=True)

    def _retrieve(self, *, with_content: bool = False) -> None:
        method = 'head'
        if with_content:
            method = 'get'
        with self._request(method) as response:
            if self._digest is None:
                self._digest = response.headers.get(DIGEST_HEADER)
            elif DIGEST_HEADER in response.headers:
                if self._digest != response.headers.get(DIGEST_HEADER):
                    raise ValueError('Retrieved digest does not match {0} != {1}'.format(
                        response.headers.get(DIGEST_HEADER),
                        self._digest,
                    ))
            if 'Content-Type' in response.headers:
                self._mime_type = response.headers.get('Content-Type')
            cache_path = self.cache_path
            self._size = int(response.headers['Content-Length'])
            if method != 'head':
                tmpfilename = '{0}.tmp'.format(cache_path)
                self._save_to(response.raw, tmpfilename)
                self._verify_checksum(tmpfilename)
                rename(tmpfilename, cache_path)

    def _request(self, method: str) -> Response:
        return self.registry.request(
            method,
            self.registry_path,
            scope=self.scope(),
            accept=self.supported_mime_types,
            stream=True,
        )

    def _save_to(self, stream: Any, tmpfilename: str) -> None:
        with open(tmpfilename, 'wb') as tmpfile:
            copyfileobj(stream, tmpfile)

    def _verify_checksum(self, tmpfilename: str) -> None:
        sha256_hash = sha256()
        buf_len = 4096
        with open(tmpfilename, 'rb') as tmpfile:
            for byte_block in iter(lambda: tmpfile.read(buf_len), b''):  # noqa:WPS426
                sha256_hash.update(byte_block)
        computed_digest = 'sha256:{0}'.format(sha256_hash.hexdigest())
        if computed_digest != self.digest:
            raise ValueError('Checksum mismatch: {0} != {1}'.format(computed_digest, self.digest))
