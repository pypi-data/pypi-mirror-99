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

from logging import getLogger
from re import IGNORECASE, Pattern, compile as re_compile, error as re_error
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Callable, List, Match, Optional, Union

    InputData = Union[
        List[str],
        Callable[[], List[str]],
    ]
    Patterns = List[Union[str, Pattern[str]]]


logger = getLogger(__name__)


class Matcher(object):
    """Matcher."""

    def __init__(
        self,
        patterns: Union[str, List[str]],
        *,
        log_prefix: str = '',
    ) -> None:
        """Initialize a matcher.

        Args:
            patterns: A pattern or list of patterns.
            log_prefix: Log prefix.
        """
        self._log_prefix = log_prefix
        if not isinstance(patterns, list):
            patterns = [patterns]
        self._patterns: Patterns = []
        for pattern in patterns:
            parsed = self._parse_pattern(pattern)
            if parsed is not None:
                self._patterns.append(parsed)

    def match(
        self,
        input_data: InputData,
    ) -> List[Match]:
        """Filer.

        Args:
            input_data: Either a list of string or an input function, called only when needed (and at most once).

        Returns:
            List of matches.
        """
        has_regex = any(isinstance(pattern, Pattern) for pattern in self._patterns)
        if not isinstance(input_data, list) and has_regex:
            input_data = input_data()
        if isinstance(input_data, list):
            return self._match_list(input_data)
        return self._match_all()

    def _match_list(self, input_data: List[str]) -> List[Match[str]]:
        matched_items: List[Match[str]] = []
        for current_item in input_data:
            match = self._match_item(current_item)
            if match:
                matched_items.append(match)
        return matched_items

    def _match_item(self, current_item: str) -> Optional[Match[str]]:
        if current_item in self._patterns:
            return re_compile('^.*$').match(current_item)
        for pattern in self._patterns:
            if isinstance(pattern, Pattern):
                match = pattern.match(current_item)
                if match:
                    return match
        return None

    def _match_all(self) -> List[Match[str]]:
        matched_items: List[Match[str]] = []
        for pattern in self._patterns:
            if not isinstance(pattern, Pattern):
                match = re_compile('^.*$').match(pattern)
                if match:
                    matched_items.append(match)
        return matched_items

    def _parse_pattern(self, pattern: str) -> Union[None, str, Pattern[str]]:
        """Parse a pattern.

        Args:
            pattern: The pattern as string.

        Returns:
            A string for exact match or a pattern.
        """
        if pattern.startswith('/'):
            flags_str = pattern.rsplit('/', 1).pop()
            flags = 0
            for flag in flags_str:
                if flag == 'i':
                    flags |= IGNORECASE
                else:
                    logger.warning(
                        '%sInvalid regular expression flag %s in %s. Flag ignored.',
                        self._log_prefix,
                        flag,
                        pattern,
                    )
            try:
                return re_compile(
                    '^{0}$'.format(pattern[1:pattern.rindex('/')]),
                    flags,
                )
            except re_error as err:
                logger.warning(  # noqa: G200
                    '%sInvalid regular expression %s: %s. Skipping pattern.',
                    self._log_prefix,
                    pattern,
                    str(err),
                )
                return None
        return pattern
