#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_appliance_time_and_locale_configuration
short_description: Manage OneView Appliance Locale and Time Configuration.
description:
    - Provides an interface to manage Appliance Locale and Time Configuration. It can only update it.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.2.0"
author: "Thiago Miotto (@tmiotto)"
options:
    state:
        description:
            - Indicates the desired state for the Appliance Locale and Time Configuration.
              C(present) will ensure data properties are compliant with OneView.
        choices: ['present']
    data:
        description:
            - List with the Appliance Locale and Time Configuration properties.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that the Appliance Locale and Time Configuration is present with locale 'en_US.UTF-8'
  oneview_appliance_time_and_locale_configuration:
    config: "{{ config_file_path }}"
    state: present
    data:
      locale: 'en_US.UTF-8'
'''

RETURN = '''
appliance_time_and_locale_configuration:
    description: Has the facts about the OneView Appliance Locale and Time Configuration.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class ApplianceTimeAndLocaleConfigurationModule(OneViewModuleBase):
    MSG_UPDATED = 'Appliance Locale and Time Configuration updated successfully.'
    MSG_ALREADY_PRESENT = 'Appliance Locale and Time Configuration is already configured.'
    RESOURCE_FACT_NAME = 'appliance_time_and_locale_configuration'

    def __init__(self):
        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present']))

        super(ApplianceTimeAndLocaleConfigurationModule, self).__init__(additional_arg_spec=additional_arg_spec)
        self.resource_client = self.oneview_client.appliance_time_and_locale_configuration

    def execute_module(self):
        resource = self.resource_client.get()
        return self.resource_present(resource, self.RESOURCE_FACT_NAME)


def main():
    ApplianceTimeAndLocaleConfigurationModule().run()


if __name__ == '__main__':
    main()
