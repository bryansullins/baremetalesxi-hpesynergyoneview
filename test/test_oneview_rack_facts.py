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

import pytest

from hpe_test_utils import OneViewBaseFactsTest
from oneview_module_loader import RackFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_MANDATORY_MISSING = dict(
    config='config.json',
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="RackName01"
)

PARAMS_GET_ALL = dict(
    config='config.json',
)

PARAMS_GET_TOPOLOGY = dict(
    config='config.json',
    name="RackName01",
    options=['deviceTopology']
)


@pytest.mark.resource(TestRackFactsModule='racks')
class TestRackFactsModule(OneViewBaseFactsTest):
    def test_should_get_all(self):
        self.resource.get_all.return_value = {"name": "Rack Name"}

        self.mock_ansible_module.params = PARAMS_GET_ALL

        RackFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(racks=({"name": "Rack Name"}))
        )

    def test_should_get_by_name(self):
        self.resource.get_by.return_value = {"name": "Rack Name"}

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        RackFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(racks=({"name": "Rack Name"}))
        )

    def test_should_get_rack_device_topology(self):
        rack = [{"name": "Rack Name", "uri": "/rest/uri/123"}]
        self.resource.get_by.return_value = rack
        self.resource.get_device_topology.return_value = {"name": "Rack Name"}

        self.mock_ansible_module.params = PARAMS_GET_TOPOLOGY

        RackFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'rack_device_topology': {'name': 'Rack Name'},
                           'racks': rack}
        )


if __name__ == '__main__':
    pytest.main([__file__])
