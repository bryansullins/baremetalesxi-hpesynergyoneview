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
from oneview_module_loader import PowerDeviceFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Power Device"
)

PARAMS_WITH_OPTIONS = dict(
    config='config.json',
    name="Test Power Device",
    options=[
        'powerState', 'uidState',
        {"utilization": {"fields": 'AveragePower',
                         "filter": 'startDate=2016-05-30T03:29:42.000Z',
                         "view": 'day'}}]
)


@pytest.mark.resource(TestPowerDeviceFactsModule='power_devices')
class TestPowerDeviceFactsModule(OneViewBaseFactsTest):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """

    def test_should_get_all_power_devices(self):
        self.resource.get_all.return_value = {"name": "Power Device Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        PowerDeviceFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(power_devices=({"name": "Power Device Name"}))
        )

    def test_should_get_power_device_by_name(self):
        self.resource.get_by.return_value = {"name": "Power Device Name"}
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        PowerDeviceFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(power_devices=({"name": "Power Device Name"}))
        )

    def test_should_get_power_device_by_name_with_options(self):
        self.resource.get_by.return_value = [{"name": "Power Device Name", "uri": "resuri"}]
        self.resource.get_power_state.return_value = {'subresource': 'ps'}
        self.resource.get_uid_state.return_value = {'subresource': 'uid'}
        self.resource.get_utilization.return_value = {'subresource': 'util'}
        self.mock_ansible_module.params = PARAMS_WITH_OPTIONS

        PowerDeviceFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'power_devices': [{'name': 'Power Device Name', 'uri': 'resuri'}],
                           'power_device_power_state': {'subresource': 'ps'},
                           'power_device_uid_state': {'subresource': 'uid'},
                           'power_device_utilization': {'subresource': 'util'},
                           }
        )


if __name__ == '__main__':
    pytest.main([__file__])
