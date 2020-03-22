#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019 Hewlett Packard Enterprise Development LP
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
module: oneview_sas_interconnect
short_description: Manage the OneView SAS Interconnect resources.
description:
    - Provides an interface to manage the SAS Interconnect. Can change the power state, UID light state, perform soft
      and hard reset, and refresh the SAS Interconnect state.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Bruno Souza (@bsouza)"
options:
    state:
        description:
            - Indicates the desired state for the Switch.
              C(powered_on) turns the power on.
              C(powered_off) turns the power off.
              C(uid_on) turns the UID light on.
              C(uid_off) turns the UID light off.
              C(soft_reset) performs a soft reset.
              C(hard_reset) performs a hard reset.
              C(refreshed) performs a refresh.
        choices: ['powered_on', 'powered_off', 'uid_on', 'uid_off', 'soft_reset', 'hard_reset', 'refreshed']
    name:
        description:
            - The SAS Interconnect name.
        required: True
notes:
    - This resource is only available on HPE Synergy
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that a SAS Interconnect is powered on
  oneview_sas_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: powered_on
    name: "0000A66101, interconnect 1"

- name: Refresh a SAS Interconnect
  oneview_sas_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: refreshed
    name: "0000A66101, interconnect 1"

- name: Perform a hard reset
  oneview_sas_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: hard_reset
    name: "0000A66101, interconnect 1"
'''

RETURN = ''' # '''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound


class SasInterconnectModule(OneViewModule):
    MSG_NOT_FOUND = 'SAS Interconnect not found.'
    MSG_NOTHING_TO_DO = 'Nothing to do.'

    states_success_message = dict(
        refreshed='SAS Interconnect refreshed successfully.',
        powered_on='SAS Interconnect powered on successfully.',
        powered_off='SAS Interconnect powered off successfully.',
        uid_on='SAS Interconnect UID state turned on successfully.',
        uid_off='SAS Interconnect UID state turned off successfully.',
        soft_reset='SAS Interconnect soft reset successfully.',
        hard_reset='SAS Interconnect hard reset successfully.'
    )

    states = dict(
        refreshed=dict(),
        powered_on=dict(operation='replace', path='/powerState', value='On'),
        powered_off=dict(operation='replace', path='/powerState', value='Off'),
        uid_on=dict(operation='replace', path='/uidState', value='On'),
        uid_off=dict(operation='replace', path='/uidState', value='Off'),
        soft_reset=dict(operation='replace', path='/softResetState', value='Reset'),
        hard_reset=dict(operation='replace', path='/hardResetState', value='Reset')
    )

    argument_spec = dict(
        state=dict(required=True, choices=states.keys()),
        name=dict(required=True, type='str'),
    )

    actions = ['soft_reset', 'hard_reset']

    def __init__(self):
        super(SasInterconnectModule, self).__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.sas_interconnects)

    def execute_module(self):
        changed, msg, facts = False, '', dict()
        if not self.current_resource:
            raise OneViewModuleResourceNotFound(self.MSG_NOT_FOUND)

        if self.state == 'refreshed':
            facts['sas_interconnect'] = self.current_resource.refresh_state(
                configuration=dict(refreshState="RefreshPending")
            )
            changed = True
            msg = self.states_success_message[self.state]
        elif self.states.get(self.state):
            changed, msg, facts['sas_interconnect'] = self.change_state(self.state)

        return dict(changed=changed, msg=msg, ansible_facts=facts)

    def change_state(self, state_name):
        changed = False
        state = self.states[state_name]
        property_name = state['path'][1:]

        if state_name in self.actions or self.current_resource.data[property_name] != state['value']:
            self.current_resource.patch(**state)
            msg = self.states_success_message[state_name]
            changed = True
        else:
            msg = self.MSG_NOTHING_TO_DO

        return changed, msg, self.current_resource.data


def main():
    SasInterconnectModule().run()


if __name__ == '__main__':
    main()
