#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_fc_network_facts
short_description: Retrieve the facts about one or more of the OneView Fibre Channel Networks
description:
    - Retrieve the facts about one or more of the Fibre Channel Networks from OneView.
version_added: "2.4"
requirements:
    - hpOneView >= 5.0.0
author:
    - Felipe Bulsoni (@fgbulsoni)
    - Thiago Miotto (@tmiotto)
    - Adriane Cardozo (@adriane-cardozo)
options:
    name:
      description:
        - Fibre Channel Network name.

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Fibre Channel Networks
  oneview_fc_network_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
  delegate_to: localhost

- debug: var=fc_networks

- name: Gather paginated, filtered and sorted facts about Fibre Channel Networks
  oneview_fc_network_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    params:
      start: 1
      count: 3
      sort: 'name:descending'
      filter: 'fabricType=FabricAttach'
  delegate_to: localhost
- debug: var=fc_networks

- name: Gather facts about a Fibre Channel Network by name
  oneview_fc_network_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    name: network name
  delegate_to: localhost

- debug: var=fc_networks
'''

RETURN = '''
fc_networks:
    description: Has all the OneView facts about the Fibre Channel Networks.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class FcNetworkFactsModule(OneViewModule):
    def __init__(self):

        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )

        super(FcNetworkFactsModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.fc_networks

    def execute_module(self):

        if self.module.params['name']:
            fc_networks = self.resource_client.get_by('name', self.module.params['name'])
        else:
            fc_networks = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(fc_networks=fc_networks))


def main():
    FcNetworkFactsModule().run()


if __name__ == '__main__':
    main()
