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

from gitlabracadabra.objects.object import GitLabracadabraObject


class GitLabracadabraUser(GitLabracadabraObject):
    EXAMPLE_YAML_HEADER = 'mmyuser:\n  type: user\n'
    DOC = [
        '# User lifecycle',
        'gitlab_id',
        'create_object',
        'delete_object',

        '# Edit',
        '## Account',
        'name',
        # 'username',
        'email',
        'skip_confirmation',
        'skip_reconfirmation',
        'public_email',
        '## Password',
        'password',
        'reset_password',
        '## Access',
        'projects_limit',
        'can_create_group',
        'admin',
        'external',
        'provider',
        'extern_uid',
        '## Limits',
        'shared_runners_minutes_limit',
        'extra_shared_runners_minutes_limit',
        '## Profile',
        'avatar',
        'skype',
        'linkedin',
        'twitter',
        'website_url',
        'location',
        'organization',
        'bio',
        'private_profile',
        'note',
    ]
    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'User',
        'type': 'object',
        'properties': {
            # Standard properties
            'gitlab_id': {
                'type': 'string',
                'description': 'GitLab id',
                '_example': 'gitlab',
                '_doc_link': 'action_file.md#gitlab_id',
            },
            'create_object': {
                'type': 'boolean',
                'description': 'Create object if it does not exists',
            },
            'delete_object': {
                'type': 'boolean',
                'description': 'Delete object if it exists',
            },
            # From https://docs.gitlab.com/ee/api/users.html#user-creation
            # 'username': {
            #     'type': 'string',
            #     'description': 'Username',
            # },
            'name': {
                'type': 'string',
                'description': 'Name',
            },
            'email': {
                'type': 'string',
                'description': 'Email',
            },
            'skip_confirmation': {
                'type': 'boolean',
                'description': 'Skip confirmation and assume e-mail is verified',
            },
            'skip_reconfirmation': {
                'type': 'boolean',
                'description': 'Skip reconfirmation',
            },
            'public_email': {
                'type': 'string',
                'description': 'The public email of the user',
            },
            'password': {
                'type': 'string',
                'description': 'Password',
            },
            'reset_password': {
                'type': 'boolean',
                'description': 'Send user password reset link',
            },
            'projects_limit': {
                'type': 'integer',
                'description': 'Number of projects user can create',
                'multipleOf': 1,
                'minimum': 0,
            },
            'can_create_group': {
                'type': 'boolean',
                'description': 'User can create groups',
            },
            'admin': {
                'type': 'boolean',
                'description': 'User is admin',
            },
            'external': {
                'type': 'boolean',
                'description': 'Flags the user as external',
            },
            'provider': {
                'type': 'string',
                'description': 'External provider name',
            },
            'extern_uid': {
                'type': 'string',
                'description': 'External UID',
            },
            'shared_runners_minutes_limit': {
                'type': 'integer',
                'description': 'Pipeline minutes quota for this user',
                'multipleOf': 1,
                'minimum': 0,
            },
            'extra_shared_runners_minutes_limit': {
                'type': 'integer',
                'description': 'Extra pipeline minutes quota for this user',
                'multipleOf': 1,
                'minimum': 0,
            },
            'avatar': {
                'type': 'string',
                'description': 'Image file for user’s avatar',
            },
            'skype': {
                'type': 'string',
                'description': 'Skype ID',
            },
            'linkedin': {
                'type': 'string',
                'description': 'LinkedIn',
            },
            'twitter': {
                'type': 'string',
                'description': 'Twitter account',
            },
            'website_url': {
                'type': 'string',
                'description': 'Website URL',
            },
            'location': {
                'type': 'string',
                'description': 'User’s location',
            },
            'organization': {
                'type': 'string',
                'description': 'Organization name',
            },
            'bio': {
                'type': 'string',
                'description': 'User’s biography',
            },
            'private_profile': {
                'type': 'boolean',
                'description': 'User’s profile is private',
            },
            'note': {
                'type': 'string',
                'description': 'Admin note',
            },
        },
        'additionalProperties': False,
        'dependencies': {
            'email': ['skip_reconfirmation'],
        },
    }

    FIND_PARAM = 'username'

    CREATE_KEY = 'username'

    CREATE_PARAMS = ['email', 'password', 'reset_password', 'skip_confirmation', 'name']

    IGNORED_PARAMS = ['password', 'reset_password', 'skip_confirmation', 'skip_reconfirmation']

    """"_get_param()

    Get a param value.
    """
    def _get_param(self, param_name):
        if param_name == 'admin':
            param_name = 'is_admin'
        return super()._get_param(param_name)
