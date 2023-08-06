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

from copy import deepcopy

import gitlab.const


def access_level(level):
    if level == 'noone':
        return 0
    elif level == 'maintainer':
        return 40
    return getattr(gitlab.const, level.upper() + '_ACCESS', None)


# Deeply update target with defaults where appropriate
def update_dict_with_defaults(target, defaults, aggregate=False):
    for k, v in defaults.items():
        if k in target:
            if isinstance(target[k], dict):
                update_dict_with_defaults(target[k], v, aggregate)
            elif isinstance(target[k], list) and aggregate:
                target[k] = deepcopy(v) + deepcopy(target[k])
        else:
            target[k] = deepcopy(v)
