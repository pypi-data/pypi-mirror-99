# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 Mathieu Parent <math.parent@gmail.com>
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

from collections import namedtuple
from unittest.mock import MagicMock, call, patch

from gitlabracadabra.containers.registries import Registries
from gitlabracadabra.containers.registry import Registry
from gitlabracadabra.containers.with_digest import WithDigest
from gitlabracadabra.objects.project import GitLabracadabraProject
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


VERIFY_CHECKSUM_METHOD = '_verify_checksum'

TestData = namedtuple('TestData', ['mirrors', 'mappings'])

TEST_DATA = (
    TestData(
        [{'from': 'debian'}],
        (('docker.io/library/debian:latest', 'mygroup/myproject/library/debian:latest'),),
    ),
    TestData(
        [{'from': 'debian:buster'}],
        (('docker.io/library/debian:buster', 'mygroup/myproject/library/debian:buster'),),
    ),
    TestData(
        [{'from': 'debian:buster', 'to': ''}],
        (('docker.io/library/debian:buster', 'mygroup/myproject:buster'),),
    ),
    TestData(
        [{'from': 'debian:buster', 'to': ':latest'}],
        (('docker.io/library/debian:buster', 'mygroup/myproject:latest'),),
    ),
    TestData(
        [{'from': 'quay.org/coreos/etcd:v3.4.1', 'to': 'etcd:v3.4.1'}],
        (('quay.org/coreos/etcd:v3.4.1', 'mygroup/myproject/etcd:v3.4.1'),),
    ),
    TestData(
        [{'from': {'repositories': ['a']}, 'to': 'etcd:v3.4.1'}],
        (('docker.io/library/a:latest', 'mygroup/myproject/etcd:v3.4.1'),),
    ),
    TestData(
        [{'from': {'repositories': ['a', 'b']}, 'to': 'etcd:v3.4.1'}],
        (
            ('docker.io/library/a:latest', 'mygroup/myproject/etcd:v3.4.1'),
            ('docker.io/library/b:latest', 'mygroup/myproject/etcd:v3.4.1'),
        ),
    ),
    TestData(
        [{'from': {
            'base': 'k8s.gcr.io/kubernetes',
            'repositories': ['kube-apiserver', 'kube-proxy'],
            'tags': ['v1.20.4', 'v1.20.6'],
        }}],
        (
            ('k8s.gcr.io/kubernetes/kube-apiserver:v1.20.4', 'mygroup/myproject/kubernetes/kube-apiserver:v1.20.4'),
            ('k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6', 'mygroup/myproject/kubernetes/kube-apiserver:v1.20.6'),
            ('k8s.gcr.io/kubernetes/kube-proxy:v1.20.4', 'mygroup/myproject/kubernetes/kube-proxy:v1.20.4'),
            ('k8s.gcr.io/kubernetes/kube-proxy:v1.20.6', 'mygroup/myproject/kubernetes/kube-proxy:v1.20.6'),
        ),
    ),
    TestData(
        [{
            'from': {
                'base': 'k8s.gcr.io/kubernetes',
                'repositories': ['kube-apiserver', 'kube-proxy'],
                'tags': ['v1.20.4', 'v1.20.6'],
            },
            'to': {},
        }],
        (
            ('k8s.gcr.io/kubernetes/kube-apiserver:v1.20.4', 'mygroup/myproject/k8s.gcr.io/kubernetes/kube-apiserver:v1.20.4'),
            ('k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6', 'mygroup/myproject/k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6'),
            ('k8s.gcr.io/kubernetes/kube-proxy:v1.20.4', 'mygroup/myproject/k8s.gcr.io/kubernetes/kube-proxy:v1.20.4'),
            ('k8s.gcr.io/kubernetes/kube-proxy:v1.20.6', 'mygroup/myproject/k8s.gcr.io/kubernetes/kube-proxy:v1.20.6'),
        ),
    ),
    TestData(
        [{
            'from': {
                'base': 'k8s.gcr.io/kubernetes',
                'repositories': ['kube-apiserver', 'kube-proxy'],
                'tags': ['v1.20.4', 'v1.20.6'],
            },
            'to': {
                'base': 'new_base',
            },
        }],
        (
            ('k8s.gcr.io/kubernetes/kube-apiserver:v1.20.4', 'mygroup/myproject/new_base/kube-apiserver:v1.20.4'),
            ('k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6', 'mygroup/myproject/new_base/kube-apiserver:v1.20.6'),
            ('k8s.gcr.io/kubernetes/kube-proxy:v1.20.4', 'mygroup/myproject/new_base/kube-proxy:v1.20.4'),
            ('k8s.gcr.io/kubernetes/kube-proxy:v1.20.6', 'mygroup/myproject/new_base/kube-proxy:v1.20.6'),
        ),
    ),
    TestData(
        [{
            'from': {
                'base': 'k8s.gcr.io/kubernetes',
                'repositories': ['kube-apiserver', 'kube-proxy'],
                'tags': ['v1.20.4', 'v1.20.6'],
            },
            'to': {
                'repository': 'new_repo',
            },
        }],
        (
            ('k8s.gcr.io/kubernetes/kube-apiserver:v1.20.4', 'mygroup/myproject/k8s.gcr.io/kubernetes/new_repo:v1.20.4'),
            ('k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6', 'mygroup/myproject/k8s.gcr.io/kubernetes/new_repo:v1.20.6'),
            ('k8s.gcr.io/kubernetes/kube-proxy:v1.20.4', 'mygroup/myproject/k8s.gcr.io/kubernetes/new_repo:v1.20.4'),
            ('k8s.gcr.io/kubernetes/kube-proxy:v1.20.6', 'mygroup/myproject/k8s.gcr.io/kubernetes/new_repo:v1.20.6'),
        ),
    ),
    TestData(
        [{
            'from': {
                'base': 'k8s.gcr.io/kubernetes',
                'repositories': ['kube-apiserver', 'kube-proxy'],
                'tags': ['v1.20.4', 'v1.20.6'],
            },
            'to': {
                'tag': 'new_tag',
            },
        }],
        (
            ('k8s.gcr.io/kubernetes/kube-apiserver:v1.20.4', 'mygroup/myproject/k8s.gcr.io/kubernetes/kube-apiserver:new_tag'),
            ('k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6', 'mygroup/myproject/k8s.gcr.io/kubernetes/kube-apiserver:new_tag'),
            ('k8s.gcr.io/kubernetes/kube-proxy:v1.20.4', 'mygroup/myproject/k8s.gcr.io/kubernetes/kube-proxy:new_tag'),
            ('k8s.gcr.io/kubernetes/kube-proxy:v1.20.6', 'mygroup/myproject/k8s.gcr.io/kubernetes/kube-proxy:new_tag'),
        ),
    ),
    # Regexps
    TestData(
        [{
            'from': {
                'repositories': ['busybox', 'debian'],
                'tags': ['/(uns|s)(id|table)/'],
            },
            'to': {
                'tag': r'how-\1-\2',
            },
        }],
        (
            ('docker.io/library/busybox:stable', 'mygroup/myproject/busybox:how-s-table'),
            ('docker.io/library/busybox:unstable', 'mygroup/myproject/busybox:how-uns-table'),
            ('docker.io/library/debian:sid', 'mygroup/myproject/debian:how-s-id'),
            ('docker.io/library/debian:stable', 'mygroup/myproject/debian:how-s-table'),
            ('docker.io/library/debian:unstable', 'mygroup/myproject/debian:how-uns-table'),
        ),
    ),
)


class TestProjectImageMirrors(TestCaseWithManager):
    """Test image_mirrors param."""

    @my_vcr.use_cassette
    def test_image_mirrors_mocked(self, cass):
        """Test image_mirrors, with mocked Registry.import_manifest.

        Args:
            cass: VCR cassette.
        """
        registry = Registries().get_registry('registry.example.com')
        for test_data in TEST_DATA:
            with self.subTest(mirrors=test_data.mirrors):
                with patch.object(Registry, 'import_manifest', autospec=True) as import_manifest_mock:
                    project = GitLabracadabraProject('memory', 'mygroup/myproject', {
                        'image_mirrors': test_data.mirrors,
                    })
                    self.assertEqual(project.errors(), [])
                    project._get = MagicMock()  # noqa: WPS437
                    project._obj = type('', (), {})()  # noqa: WPS437
                    project._obj.container_registry_image_prefix = 'registry.example.com/mygroup/myproject'  # noqa: WPS437
                    project.process()
                    self._assert_mappings(registry, import_manifest_mock, test_data.mappings)
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_image_mirrors_auth(self, cass):
        """Test image_mirrors, auth'ing using JWT.

        Args:
            cass: VCR cassette.
        """
        expected_digest = 'sha256:c6b45a95f932202dbb27c31333c4789f45184a744060f6e569cc9d2bf1b9ad6f'
        with patch.object(WithDigest, VERIFY_CHECKSUM_METHOD) as verify_checksum_mock:
            verify_checksum_mock.return_value = None
            project = GitLabracadabraProject('memory', 'root/test_registry', {
                'image_mirrors': [{
                    'from': 'busybox',
                    'to': 'busybox',
                }],
            })
            self.assertEqual(project.errors(), [])
            with patch('gitlabracadabra.containers.registry_importer.logger', autospec=True) as logger:
                project.process()
                logger.info.assert_has_calls([call(
                    '%s%s %simported as %s:%s (%s, %s, %s)',
                    '[root/test_registry] ',
                    'docker.io/library/busybox:latest@{0}'.format(expected_digest),
                    '',
                    'root/test_registry/busybox',
                    'latest',
                    '1+0=1 uploaded+existing manifests',
                    '2+0+0=2 uploaded+mounted+existing blobs',
                    '766112+0+0=766112 uploaded+mounted+existing blobs size',
                )])
        self.assertTrue(cass.all_played)

    def _assert_mappings(self, registry, import_manifest_mock, mappings):
        self.assertEqual(len(import_manifest_mock.mock_calls), len(mappings))
        for mapping_index, mapping in enumerate(mappings):
            _, args, kwargs = import_manifest_mock.mock_calls[mapping_index]
            self.assertEqual(len(args), 3)
            self.assertEqual(args[0], registry)
            self.assertEqual(str(args[1]), mapping[0])
            self.assertEqual(
                '{0}:{1}'.format(args[2], kwargs['tag']),
                mapping[1],
            )
            self.assertEqual(
                kwargs,
                {
                    'tag': mapping[1].rsplit(':').pop(),
                    'platform': None,
                    'log_prefix': '[mygroup/myproject] ',
                    'dry_run': False,
                },
            )
