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

from collections import namedtuple
from typing import Any
from unittest.mock import MagicMock

from gitlabracadabra.matchers import Matcher
from gitlabracadabra.tests.case import TestCaseWithManager


TestData = namedtuple('TestData', ['patterns', 'as_callable', 'result', 'called'])

INPUT_DATA = ('item', 'item_suffix', 'prefix_item', 'another')

TEST_DATA = (
    # String patterns
    TestData('item', as_callable=False, result=['item'], called=None),
    TestData('item', as_callable=True, result=['item'], called=False),
    TestData(['item', 'extra'], as_callable=False, result=['item'], called=None),
    TestData(['item', 'extra'], as_callable=True, result=['item', 'extra'], called=False),
    # Regex patterns
    TestData('/item/', as_callable=False, result=['item'], called=None),
    TestData('/item/', as_callable=True, result=['item'], called=True),
    TestData(['/item/', '/extra/'], as_callable=False, result=['item'], called=None),
    TestData(['/item/', '/extra/'], as_callable=True, result=['item'], called=True),
    # Mixed patterns
    TestData(['another', '/item.*/'], as_callable=False, result=['item', 'item_suffix', 'another'], called=None),
    TestData(['another', '/item.*/'], as_callable=True, result=['item', 'item_suffix', 'another'], called=True),
    TestData(['another', '/.*item/'], as_callable=False, result=['item', 'prefix_item', 'another'], called=None),
    TestData(['another', '/.*item/'], as_callable=True, result=['item', 'prefix_item', 'another'], called=True),
    # Flags
    TestData('/Item/', as_callable=False, result=[], called=None),
    TestData('/Item/i', as_callable=False, result=['item'], called=None),
)


class TestMatcher(TestCaseWithManager):
    """Test Matcher class."""

    def test_match(self):
        """Test Matcher.match method."""
        for test_data in TEST_DATA:
            with self.subTest(patterns=test_data.patterns, as_callable=test_data.as_callable):
                if test_data.as_callable:
                    input_data = MagicMock()
                    input_data.return_value = list(INPUT_DATA)
                else:
                    input_data = list(INPUT_DATA)
                matches = Matcher(test_data.patterns).match(input_data)
                self.assertEqual(len(matches), len(test_data.result))
                for index, match in enumerate(matches):
                    self.assertEqual(match[0], test_data.result[index])
                self._assert_call(input_data, test_data.as_callable, test_data.called)

    def _assert_call(self, input_data: Any, as_callable: bool, called: bool) -> None:
        if as_callable and called:
            input_data.assert_called_once_with()
        elif as_callable:
            self.assertEqual(len(input_data.mock_calls), 0)
        else:
            self.assertIsNone(called)
