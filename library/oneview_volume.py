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
module: oneview_volume
short_description: Manage OneView Volume resources.
description:
    - Provides an interface to manage Volume resources. It allows create, update, delete or repair the volume, and
      create or delete a snapshot.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    state:
        description:
            - Indicates the desired state for the Volume resource.
              C(present) creates/adds the resource when it does not exist, otherwise it updates the resource. When the
              resource already exists, the update operation is non-convergent, since it is always called even though
              the given options are compliant with the existent data. To change the name of the volume, a C(newName) in
              the I(data) must be provided.
              C(absent) by default deletes a volume from OneView and the storage system. When export_only is True, the
              volume is removed only from OneView.
              C(repaired) removes extra presentations from a specified volume on the storage system. This operation is
              non-idempotent.
              C(snapshot_created) creates a snapshot for the volume specified. This operation is non-idempotent.
              C(snapshot_deleted) deletes a snapshot from OneView and the storage system.
        choices: ['present', 'absent', 'repaired', 'snapshot_created', 'snapshot_deleted']
    data:
      description:
        - Volume or snapshot data.
      required: true
    export_only:
      description:
        - If set to True, when the status is C(absent) and the resource exists, it will be removed only from OneView.
      default: False
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Volume with a specified Storage Pool
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: present
    data:
      properties:
        name: 'Volume with Storage Pool'
        description: 'Test volume with common creation: Storage Pool'
        size: 2147483648  # 2GB
        storagePool: '{{ storage_pool_uri }}'
      templateUri: '/rest/storage-volume-templates/e2f95f1d-de9d-406e-803f-a8aa00da92b0'
      isPermanent: false
      initialScopeUris: ['/rest/scopes/754e0dce-3cbd-4188-8923-edf86f068bf7']
  delegate_to: localhost

- name: Create a volume with a specified Snapshot Pool
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: present
    data:
      properties:
        name: 'Volume with Snapshot Pool'
        description: 'Test volume with common creation: Storage System + Storage Pool + Snapshot Pool'
        size: 1073741824  # 1GB
        storagePool: '{{ storage_pool_uri }}'
        snapshotPool: '{{ storage_pool_uri }}'
      templateUri: '/rest/storage-volume-templates/e2f95f1d-de9d-406e-803f-a8aa00da92b0'
      isPermanent: false
      initialScopeUris: ['/rest/scopes/754e0dce-3cbd-4188-8923-edf86f068bf7']
  delegate_to: localhost

- name: Add a volume for management by the appliance using the WWN of the volume
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 300
    state: present
    data:
      type: AddStorageVolumeV2
      name: 'Volume added with a specific WWN'
      description: 'Test volume added for management: Storage System + Storage Pool + WWN'
      storageSystemUri: '/rest/storage-systems/TXQ1000307'
      wwn: 'DC:32:13:72:47:00:10:00:30:71:47:16:33:58:47:95'
      provisioningParameters:
          shareable: True
  when: wwn is defined

- name: Update the name of the volume to 'Volume with Storage Pool - Renamed' and shareable to false
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: present
    data:
      name: 'Volume with Storage Pool'
      newName: 'Volume with Storage Pool - Renamed'
      isShareable: False
    delegate_to: localhost

- name: Remove extra presentations from the specified volume on the storage system
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: repaired
    data:
      name: 'Volume with Storage Pool - Renamed'

- name: Create a new snapshot for the specified volume
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: snapshot_created
    data:
      name: 'Volume with Snapshot Pool'
      snapshotParameters:
        name: 'test_snapshot'
        description: 'New snapshot'

- name: Delete the snapshot
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: snapshot_deleted
    data:
      name: 'Volume with Snapshot Pool'
      snapshotParameters:
        name: 'test_snapshot'

- name: Delete the volume previously created with a Storage Pool
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: absent
    data:
      name: 'Volume with Storage Pool - Renamed'

- name: Delete the volume previously created with a Snapshot Pool
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: absent
    data:
      name: 'Volume with Snapshot Pool - Renamed'

- name: Delete the volume previously added using the WWN of the volume
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: absent
    data:
      name: 'Volume added with a specific WWN'
    export_only: True
'''

RETURN = '''
storage_volume:
    description: Has the facts about the Storage Volume.
    returned: On state 'present', but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleValueError, OneViewModuleResourceNotFound, OneViewModuleException


class VolumeModule(OneViewModuleBase):
    MSG_CREATED = 'Volume added/created successfully.'
    MSG_UPDATED = 'Volume updated successfully.'
    MSG_DELETED = 'Volume removed/deleted successfully.'
    MSG_REPAIRED = 'Volume repaired successfully.'
    MSG_ALREADY_MANAGED = 'Volume is already managed by the appliance.'
    MSG_ADDED = 'Volume is now managed by the appliance.'
    MSG_SNAPSHOT_CREATED = 'Volume snapshot created successfully.'
    MSG_SNAPSHOT_DELETED = 'Volume snapshot deleted successfully.'
    MSG_NOT_FOUND = 'Volume not found.'
    MSG_SNAPSHOT_NOT_FOUND = 'Snapshot not found.'
    MSG_ALREADY_ABSENT = 'Volume is already absent.'
    MSG_NO_OPTIONS_PROVIDED = 'No options provided.'
    MSG_NEW_NAME_INVALID = 'Rename failed: the new name provided is being used by another Volume.'

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present', 'absent', 'managed', 'repaired',
                         'snapshot_created', 'snapshot_deleted']
            ),
            data=dict(required=True, type='dict'),
            export_only=dict(required=False, type='bool'),
            suppress_device_updates=dict(required=False, type='bool')
        )
        super(VolumeModule, self).__init__(additional_arg_spec=argument_spec,
                                           validate_etag_support=True)

        self.resource_client = self.oneview_client.volumes

    def execute_module(self):
        if self.data.get('deviceVolumeName'):
            name = self.data.get('deviceVolumeName')
        else:
            name = self.data.get('name') or self.data.get('properties').get('name')
        resource = self.get_by_name(name)

        if self.state == 'present':
            return self.__present(resource)
        if self.state == 'managed':
            return self.__managed(resource)
        elif self.state == 'absent':
            return self.__absent(resource)
        else:
            if not resource:
                raise OneViewModuleResourceNotFound(self.MSG_NOT_FOUND)

            if self.state == 'repaired':
                return self.__repair(resource)
            elif self.state == 'snapshot_created':
                return self.__create_snapshot(resource)
            elif self.state == 'snapshot_deleted':
                return self.__delete_snapshot(resource)

    def __present(self, resource):
        if 'snapshotUri' in self.data:
            return self.__create_from_snapshot()
        elif not resource:
            return self.__create()
        else:
            return self.__update(resource)

    def __managed(self, resource):
        if not resource:
            resource = self.resource_client.add_from_existing(self.data)
            changed = True
            msg = self.MSG_ADDED
        else:
            changed = False
            msg = self.MSG_ALREADY_MANAGED
        return dict(changed=changed, msg=msg, ansible_facts=dict(storage_volume=resource))

    def __absent(self, resource):
        if resource:
            self.resource_client.delete(resource,
                                        export_only=self.module.params.get('export_only'),
                                        suppress_device_updates=self.module.params.get('suppress_device_updates'))
            return dict(changed=True, msg=self.MSG_DELETED)
        else:
            return dict(changed=False, msg=self.MSG_ALREADY_ABSENT)

    def __create(self):
        created_volume = self.resource_client.create(self.data)
        return dict(changed=True,
                    msg=self.MSG_CREATED,
                    ansible_facts=dict(storage_volume=created_volume))

    def __create_from_snapshot(self):
        created_volume = self.resource_client.create_from_snapshot(self.data)
        return dict(changed=True,
                    msg=self.MSG_CREATED,
                    ansible_facts=dict(storage_volume=created_volume))

    def __update(self, resource):
        new_name = self.data.pop('newName', None)
        if new_name:
            new_resource = self.get_by_name(new_name)
            if new_resource:
                raise OneViewModuleValueError(self.MSG_NEW_NAME_INVALID)
            self.data['name'] = new_name
        merged_data = resource.copy()
        merged_data.update(self.data)

        updated_volume = self.resource_client.update(merged_data)

        return dict(changed=True,
                    msg=self.MSG_UPDATED,
                    ansible_facts=dict(storage_volume=updated_volume))

    def __repair(self, resource):

        self.resource_client.repair(resource['uri'])
        return dict(changed=True, msg=self.MSG_REPAIRED)

    def __create_snapshot(self, resource):
        if 'snapshotParameters' not in self.data:
            raise OneViewModuleResourceNotFound(self.MSG_NO_OPTIONS_PROVIDED)

        self.resource_client.create_snapshot(resource['uri'], self.data['snapshotParameters'])
        return dict(changed=True, msg=self.MSG_SNAPSHOT_CREATED)

    def __delete_snapshot(self, resource):
        if 'snapshotParameters' not in self.data:
            raise OneViewModuleResourceNotFound(self.MSG_NO_OPTIONS_PROVIDED)

        snapshot = self.__get_snapshot_by_name(resource, self.data)
        if not snapshot:
            raise OneViewModuleResourceNotFound(self.MSG_SNAPSHOT_NOT_FOUND)
        else:
            self.resource_client.delete_snapshot(snapshot)
            return dict(changed=True, msg=self.MSG_SNAPSHOT_DELETED)

    def __get_snapshot_by_name(self, resource, data):
        if 'name' not in data['snapshotParameters']:
            raise OneViewModuleValueError(self.MSG_NO_OPTIONS_PROVIDED)

        result = self.resource_client.get_snapshot_by(resource['uri'], 'name',
                                                      data['snapshotParameters']['name'])
        return result[0] if result else None


def main():
    VolumeModule().run()


if __name__ == '__main__':
    main()
