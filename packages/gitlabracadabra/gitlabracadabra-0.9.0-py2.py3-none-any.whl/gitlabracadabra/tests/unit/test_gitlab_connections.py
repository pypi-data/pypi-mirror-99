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

from contextlib import contextmanager
from typing import Generator
from unittest.mock import call, patch

from gitlab import Gitlab, __version__ as gitlab_version

from gitlabracadabra.gitlab.connections import GitlabConnections
from gitlabracadabra.tests.case import TestCase
from gitlabracadabra.tests.patchfuncs import patch_open


class TestGitlabConnections(TestCase):
    """Test GitlabConnections class."""

    @contextmanager
    def fake_config(self, call_count: int = 1) -> Generator[GitlabConnections, None, None]:
        """Fake configuration.

        Args:
            call_count: Number of Gitlab objects created.

        Yields:
            The Gitlab connections singleton.
        """
        config_path = '/path/to/python-gitlab.cfg'
        singleton = GitlabConnections()
        singleton.load(None, [config_path], debug=False)
        config = """
            [global]
            default = gitlab

            [gitlab]
            url = https://gitlab.com
            private_token = T0k3n

            [internal]
            url = https://gitlab.example.com
            private_token = n3k0T
        """
        with patch('os.path.exists') as os_path_exists_mock:
            with patch_open({config_path: config}):
                with patch.object(Gitlab, 'auth') as auth_mock:
                    os_path_exists_mock.return_value = True
                    yield singleton
                    if gitlab_version != '1.6.0':
                        self.assertEqual(  # noqa: WPS220
                            os_path_exists_mock.mock_calls,
                            [call(config_path) for _ in range(call_count)],
                        )
                    self.assertEqual(auth_mock.mock_calls, [call() for _ in range(call_count)])

    def test_singleton(self) -> None:
        """Ensure singleton pattern."""
        singleton1 = GitlabConnections()
        singleton2 = GitlabConnections()
        self.assertEqual(id(singleton1), id(singleton2))

    def test_get_connection_none(self) -> None:
        """Get default Gitlab connection."""
        with self.fake_config() as singleton:
            gl1 = singleton.get_connection()
            self.assertEqual(gl1.pygitlab.api_url, 'https://gitlab.com/api/v4')
            self.assertEqual(gl1.pygitlab.private_token, 'T0k3n')
            gl2 = singleton.get_connection(None)
            self.assertEqual(id(gl1), id(gl2))

    def test_get_connection_internal(self) -> None:
        """Get another Gitlab connection."""
        with self.fake_config() as singleton:
            gl1 = singleton.get_connection('internal')
            self.assertEqual(gl1.pygitlab.api_url, 'https://gitlab.example.com/api/v4')
            self.assertEqual(gl1.pygitlab.private_token, 'n3k0T')
            gl2 = singleton.get_connection('internal')
            self.assertEqual(id(gl1), id(gl2))

    def test_get_connection_both(self) -> None:
        """Get several Gitlab connections."""
        with self.fake_config(2) as singleton:
            gl1 = singleton.get_connection()
            gl2 = singleton.get_connection('internal')
            self.assertEqual(gl1.pygitlab.api_url, 'https://gitlab.com/api/v4')
            self.assertEqual(gl1.pygitlab.private_token, 'T0k3n')
            self.assertEqual(gl2.pygitlab.api_url, 'https://gitlab.example.com/api/v4')
            self.assertEqual(gl2.pygitlab.private_token, 'n3k0T')
