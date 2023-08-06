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

import inspect
import os
import re

from vcr import VCR


def _gitlabracadabra_func_path_generator(function):
    func_file = inspect.getfile(function)
    method_name = function.__name__  # test_no_create
    instance_name = function.__self__.__class__.__name__  # TestUser
    fixture_name = (re.sub(r'^Test', r'', instance_name) +
                    '_' +
                    re.sub(r'^test_', r'', method_name) +
                    '.yaml')
    return os.path.join(os.path.dirname(func_file),
                        'fixtures',
                        fixture_name,
                        )


def _gitlabracadabra_uri_matcher(r1, r2):
    r1_uri = r1.uri
    r2_uri = r2.uri
    # Workaround 'all=True' in API calls
    # with python-gitlab < 1.8.0
    # See https://github.com/python-gitlab/python-gitlab/pull/701
    if r1_uri.endswith('all=True'):
        r1_uri = r1_uri[0:-9]
    # Ignore host and port
    r1_uri = re.sub('http://[^:/]+(:\\d+)?/', 'http://localhost/', r1_uri)
    r2_uri = re.sub('http://[^:/]+(:\\d+)?/', 'http://localhost/', r2_uri)
    return r1_uri == r2_uri


my_vcr = VCR(
    match_on=['method', 'gitlabracadabra_uri', 'body'],
    func_path_generator=_gitlabracadabra_func_path_generator,
    record_mode='once',  # change to 'new_episodes' to append to existing fixtures
    inject_cassette=True,
)
my_vcr.register_matcher('gitlabracadabra_uri', _gitlabracadabra_uri_matcher)
