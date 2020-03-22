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
module: oneview_san_manager
short_description: Manage OneView SAN Manager resources.
description:
    - Provides an interface to manage SAN Manager resources. Can create, update, or delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.1"
author: "Mariana Kreisig (@marikrg)"
options:
    state:
        description:
            - Indicates the desired state for the Uplink Set resource.
              C(present) ensures data properties are compliant with OneView.
              C(absent) removes the resource from OneView, if it exists.
              C(connection_information_set) updates the connection information for the SAN Manager. This operation is
              non-idempotent.
        choices: ['present', 'absent', connection_information_set]
    data:
      description:
        - List with SAN Manager properties.
      required: true
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Creates a Device Manager for the Brocade SAN provider with the given hostname and credentials
  oneview_san_manager:
    config: "{{ config }}"
    state: present
    data:
      providerDisplayName: 'Brocade Network Advisor'
      connectionInfo:
        - name: Host
          value: '172.18.15.1'
        - name: Port
          value: '5989'
        - name: Username
          value: 'username'
        - name: Password
          value: 'password'
        - name: UseSsl
          value: true

- name: Sets the SAN Manager connection information
  oneview_san_manager:
    config: "{{ config_path }}"
    state: connection_information_set
    data:
      connectionInfo:
        - name: Host
          value: '172.18.15.1'
        - name: Port
          value: '5989'
        - name: Username
          value: 'username'
        - name: Password
          value: 'password'
        - name: UseSsl
          value: true

- name: Refreshes the SAN Manager
  oneview_san_manager:
    config: "{{ config_path }}"
    state: present
    data:
      name: '172.18.15.1'
      refreshState: 'RefreshPending'

- name: Delete the SAN Manager recently created
  oneview_san_manager:
    config: "{{ config_path }}"
    state: absent
    data:
      name: '172.18.15.1'
'''

RETURN = '''
san_manager:
    description: Has the OneView facts about the SAN Manager.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleValueError, compare


class SanManagerModule(OneViewModuleBase):
    MSG_CREATED = 'SAN Manager created successfully.'
    MSG_UPDATED = 'SAN Manager updated successfully.'
    MSG_DELETED = 'SAN Manager deleted successfully.'
    MSG_ALREADY_PRESENT = 'SAN Manager is already present.'
    MSG_ALREADY_ABSENT = 'SAN Manager is already absent.'
    MSG_SAN_MANAGER_PROVIDER_DISPLAY_NAME_NOT_FOUND = "The provider '{}' was not found."

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent', 'connection_information_set']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(SanManagerModule, self).__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)
        self.resource_client = self.oneview_client.san_managers

    def execute_module(self):
        if self.data.get('connectionInfo'):
            for connection_hash in self.data.get('connectionInfo'):
                if connection_hash.get('name') == 'Host':
                    resource_name = connection_hash.get('value')
        elif self.data.get('name'):
            resource_name = self.data.get('name')
        else:
            msg = 'A "name" or "connectionInfo" must be provided inside the "data" field for this operation. '
            msg += 'If a "connectionInfo" is provided, the "Host" name is considered as the "name" for the resource.'
            raise OneViewModuleValueError(msg.format())

        resource = self.resource_client.get_by_name(resource_name)

        if self.state == 'present':
            changed, msg, san_manager = self.__present(resource)
            return dict(changed=changed, msg=msg, ansible_facts=dict(san_manager=san_manager))

        elif self.state == 'absent':
            return self.resource_absent(resource, method='remove')

        elif self.state == 'connection_information_set':
            changed, msg, san_manager = self.__connection_information_set(resource)
            return dict(changed=changed, msg=msg, ansible_facts=dict(san_manager=san_manager))

    def __present(self, resource):
        if not resource:
            provider_uri = self.data.get('providerUri', self.__get_provider_uri_by_display_name(self.data))
            return True, self.MSG_CREATED, self.resource_client.add(self.data, provider_uri)
        else:
            merged_data = resource.copy()
            merged_data.update(self.data)

            # Remove 'connectionInfo' from comparison, since it is not possible to validate it.
            resource.pop('connectionInfo', None)
            merged_data.pop('connectionInfo', None)

            if compare(resource, merged_data):
                return False, self.MSG_ALREADY_PRESENT, resource
            else:
                updated_san_manager = self.resource_client.update(resource=merged_data, id_or_uri=resource['uri'])
                return True, self.MSG_UPDATED, updated_san_manager

    def __connection_information_set(self, resource):
        if not resource:
            return self.__present(resource)
        else:
            merged_data = resource.copy()
            merged_data.update(self.data)
            merged_data.pop('refreshState', None)
            if not self.data.get('connectionInfo', None):
                raise OneViewModuleValueError('A connectionInfo field is required for this operation.')
            updated_san_manager = self.resource_client.update(resource=merged_data, id_or_uri=resource['uri'])
            return True, self.MSG_UPDATED, updated_san_manager

    def __get_provider_uri_by_display_name(self, data):
        display_name = data.get('providerDisplayName')
        provider_uri = self.resource_client.get_provider_uri(display_name)

        if not provider_uri:
            raise OneViewModuleValueError(self.MSG_SAN_MANAGER_PROVIDER_DISPLAY_NAME_NOT_FOUND.format(display_name))

        return provider_uri


def main():
    SanManagerModule().run()


if __name__ == '__main__':
    main()
