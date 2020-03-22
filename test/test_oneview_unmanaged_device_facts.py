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
from oneview_module_loader import UnmanagedDeviceFactsModule

ERROR_MSG = 'Fake message error'

UNMANAGED_DEVICE_NAME = "New Unmanaged Device Name"
UNMANAGED_DEVICE_URI = "/rest/unmanaged-devices/831083d9-dc9b-46af-8d71-6da55f9fda12"

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=UNMANAGED_DEVICE_NAME,
    options=None
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=UNMANAGED_DEVICE_NAME,
    options=['environmental_configuration']
)

UNMANAGED_DEVICE = dict(
    category="unmanaged-devices",
    created="2016-09-22T15:43:07.037Z",
    deviceType="Server",
    height=None,
    id="831083d9-dc9b-46af-8d71-6da55f9fda12",
    model="Procurve 4200VL",
    name=UNMANAGED_DEVICE_NAME,
    state="Unmanaged",
    status="Disabled",
    uri=UNMANAGED_DEVICE_URI,
    uuid="831083d9-dc9b-46af-8d71-6da55f9fda12"
)

ENVIRONMENTAL_CONFIGURATION = dict(
    calibratedMaxPower=-1,
    capHistorySupported=False,
    height=-1,
    historyBufferSize=0
)


@pytest.mark.resource(TestUnmanagedDeviceFactsModule='unmanaged_devices')
class TestUnmanagedDeviceFactsModule(OneViewBaseFactsTest):
    def test_get_all(self):
        unmanaged_devices = [UNMANAGED_DEVICE]
        self.resource.get_all.return_value = unmanaged_devices
        self.mock_ansible_module.params = PARAMS_GET_ALL

        UnmanagedDeviceFactsModule().run()

        self.resource.get_all.assert_called_once_with()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts=dict(unmanaged_devices=unmanaged_devices),
            changed=False
        )

    def test_get_by(self):
        unmanaged_devices = [UNMANAGED_DEVICE]
        self.resource.get_by.return_value = unmanaged_devices
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        UnmanagedDeviceFactsModule().run()

        self.resource.get_by.assert_called_once_with('name', UNMANAGED_DEVICE_NAME)
        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts=dict(unmanaged_devices=unmanaged_devices),
            changed=False
        )

    def test_get_by_with_options(self):
        unmanaged_devices = [UNMANAGED_DEVICE]
        self.resource.get_by.return_value = unmanaged_devices
        self.resource.get_environmental_configuration.return_value = ENVIRONMENTAL_CONFIGURATION

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        UnmanagedDeviceFactsModule().run()

        self.resource.get_by.assert_called_once_with('name', UNMANAGED_DEVICE_NAME)
        self.resource.get_environmental_configuration.assert_called_once_with(
            id_or_uri=UNMANAGED_DEVICE_URI
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts=dict(
                unmanaged_devices=unmanaged_devices,
                unmanaged_device_environmental_configuration=ENVIRONMENTAL_CONFIGURATION
            ),
            changed=False
        )


if __name__ == '__main__':
    pytest.main([__file__])
