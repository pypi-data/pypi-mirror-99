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

from unittest import TestCase

from gitlab import Gitlab

from gitlabracadabra.gitlab_connections import GitlabConnections


class TestCaseWithManager(TestCase):
    def setUp(self):
        GitlabConnections()._gitlabs = {None: Gitlab(  # noqa: S106
            'http://localhost:3000',
            private_token='xsYEYpTSbxrCafAhpnAp',
        )}

    def tearDown(self):
        GitlabConnections()._gitlabs = {}
