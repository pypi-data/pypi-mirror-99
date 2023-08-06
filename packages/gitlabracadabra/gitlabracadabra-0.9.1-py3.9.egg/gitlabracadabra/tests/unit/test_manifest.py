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

from requests import HTTPError, codes

from gitlabracadabra.containers.manifest import Manifest
from gitlabracadabra.containers.registry import Registry
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCase


class TestManifest(TestCase):
    """Test Manifest class."""

    @my_vcr.use_cassette
    def test_tag_list(self, cass):
        """Test tag_list method.

        Args:
            cass: VCR cassette.
        """
        registry = Registry('docker.io')
        manifest = Manifest(registry, 'library/debian')
        self.assertIsInstance(manifest, Manifest)
        tag_list = manifest.tag_list()
        self.assertIsInstance(tag_list, list)
        self.assertIn('buster', tag_list)
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_not_found(self, cass):
        """Test proper 404 handling.

        Args:
            cass: VCR cassette.
        """
        registry = Registry('docker.io')
        for attr in 'digest', 'size', 'mime_type':
            with self.subTest(attr=attr):
                with self.assertRaises(HTTPError) as cm:
                    manifest = Manifest(registry, 'library/debian', tag='not_found')
                    getattr(manifest, attr)
                self.assertEqual(cm.exception.response.status_code, codes['not_found'])  # noqa: WPS441
        self.assertFalse(Manifest(registry, 'library/debian', tag='not_found').exists())
        self.assertTrue(cass.all_played)
