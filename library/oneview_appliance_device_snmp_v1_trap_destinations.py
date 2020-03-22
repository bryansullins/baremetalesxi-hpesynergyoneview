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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_appliance_device_snmp_v1_trap_destinations
short_description: Manage the Appliance Device SNMPv1 Trap Destinations.
description:
    - Provides an interface to manage the Appliance Device SNMPv1 Trap Destinations.
version_added: "2.5"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.8.0"
author:
    "Gianluca Zecchi (@gzecchi)"
options:
    state:
        description:
          - Indicates the desired state for the Appliance Device SNMPv1 Trap Destinations.
            C(present) ensures data properties are compliant with OneView.
            C(absent) removes the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with the SNMPv1 Trap Destination properties
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Create or Update an Appliance Device SNMPv1 Trap Destination by Destination Address
  oneview_appliance_device_snmp_v1_trap_destinations:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
      communityString: "public"
      destination: "10.0.0.1"
      port: 162
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v1_trap_destinations

- name: Create or Update an Appliance Device SNMPv1 Trap Destination by URI
  oneview_appliance_device_snmp_v1_trap_destinations:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
      communityString: "private"
      uri: "/rest/appliance/trap-destinations/1"
      port: 162
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v1_trap_destinations

- name: Delete an Appliance Device SNMPv1 Trap Destination by Destination Address
  oneview_appliance_device_snmp_v1_trap_destinations:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: absent
    data:
      destination: "10.0.0.1"
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v1_trap_destinations

- name: Delete an Appliance Device SNMPv1 Trap Destination by URI
  oneview_appliance_device_snmp_v1_trap_destinations:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: absent
    data:
        uri: "/rest/appliance/trap-destinations/1"
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v1_trap_destinations
'''

RETURN = '''
appliance_device_snmp_v1_trap_destinations:
    description: Has all the OneView facts about the OneView appliance SNMPv1 trap forwarding destinations.
    returned: On state 'present'.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleException, OneViewModuleValueError


class ApplianceDeviceSnmpV1TrapDestinationsModule(OneViewModuleBase):
    MSG_CREATED = 'Appliance Device SNMPv1 Trap Destination created successfully.'
    MSG_UPDATED = 'Appliance Device SNMPv1 Trap Destination updated successfully.'
    MSG_DELETED = 'Appliance Device SNMPv1 Trap Destination deleted successfully.'
    MSG_ALREADY_PRESENT = 'Appliance Device SNMPv1 Trap Destination is already present.'
    MSG_ALREADY_ABSENT = 'Appliance Device SNMPv1 Trap Destination is already absent.'
    MSG_VALUE_ERROR = 'The destination or the uri attrbiutes must be specfied'
    RESOURCE_FACT_NAME = 'appliance_device_snmp_v1_trap_destinations'

    argument_spec = dict(
        data=dict(required=True, type='dict'),
        state=dict(
            required=True,
            choices=['present', 'absent'])
    )

    def __init__(self):
        super(ApplianceDeviceSnmpV1TrapDestinationsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.appliance_device_snmp_v1_trap_destinations

    def execute_module(self):
        if self.data.get('uri'):
            query = self.resource_client.get_by('uri', self.data.get('uri'))
            resource = query[0] if query and query[0].get('uri') == self.data['uri'] else None
        elif self.data.get('destination'):
            query = self.resource_client.get_by('destination', self.data.get('destination'))
            resource = query[0] if query and query[0].get('destination') == self.data['destination'] else None
        else:
            raise OneViewModuleValueError(self.MSG_VALUE_ERROR)

        if self.state == 'present':
            return self.resource_present(resource, self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent(resource)


def main():
    ApplianceDeviceSnmpV1TrapDestinationsModule().run()


if __name__ == '__main__':
    main()
