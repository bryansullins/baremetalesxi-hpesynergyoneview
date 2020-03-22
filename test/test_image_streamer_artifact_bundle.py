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

import mock
import pytest

from copy import deepcopy
from hpe_test_utils import ImageStreamerBaseTest
from oneview_module_loader import ArtifactBundleModule

ERROR_MSG = 'Fake message error'


@pytest.mark.resource(TestArtifactBundleModule='artifact_bundles')
class TestArtifactBundleModule(ImageStreamerBaseTest):
    """
    ImageStreamerBaseTest has common tests for the main function, also provides the
    mocks used in this test class.
    """

    @pytest.fixture(autouse=True)
    def specific_set_up(self):
        self.TASK_CREATE = self.EXAMPLES[0]['image_streamer_artifact_bundle']
        self.TASK_DOWNLOAD = self.EXAMPLES[1]['image_streamer_artifact_bundle']
        self.TASK_DOWNLOAD_ARCHIVE = self.EXAMPLES[2]['image_streamer_artifact_bundle']
        self.TASK_UPLOAD = self.EXAMPLES[3]['image_streamer_artifact_bundle']
        self.TASK_BACKUP_UPLOAD = self.EXAMPLES[4]['image_streamer_artifact_bundle']
        self.TASK_CREATE_BACKUP = self.EXAMPLES[5]['image_streamer_artifact_bundle']
        self.TASK_EXTRACT = self.EXAMPLES[6]['image_streamer_artifact_bundle']
        self.TASK_BACKUP_EXTRACT = self.EXAMPLES[7]['image_streamer_artifact_bundle']
        self.TASK_UPDATE = self.EXAMPLES[8]['image_streamer_artifact_bundle']
        self.TASK_REMOVE = self.EXAMPLES[9]['image_streamer_artifact_bundle']

        self.BUILD_PLANS = dict(
            resourceUri="/rest/build-plans/ab65bb06-4387-48a0-9a5d-0b0da2888508",
            readOnly="false"
        )

        self.ARTIFACT_BUNDLE = dict(
            name="Artifact Bundle",
            description="Description of Artifact Bundles Test",
            buildPlans=[self.BUILD_PLANS]
        )

        self.DEPLOYMENT_GROUP = dict(
            resourceUri="/rest/deployment-groups/asd32232132-444-423a0-92dd-025asd234df508",
            name="Deployment Group Name"
        )

    def test_create_artifact_bundle(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = self.ARTIFACT_BUNDLE
        self.mock_ansible_module.params = self.TASK_CREATE

        ArtifactBundleModule().run()

        self.resource.create.assert_called_once_with(
            self.ARTIFACT_BUNDLE
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_CREATED,
            ansible_facts=dict(artifact_bundle=self.ARTIFACT_BUNDLE)
        )

    def test_download_artifact_bundle(self):
        artifact_bundle = self.TASK_CREATE['data']
        artifact_bundle['uri'] = '/rest/artifact-bundles/1'

        self.resource.get_by.return_value = [artifact_bundle]

        self.mock_ansible_module.params = self.TASK_DOWNLOAD

        ArtifactBundleModule().run()

        download_file = self.TASK_DOWNLOAD['data']['destinationFilePath']
        uri = artifact_bundle['uri']

        self.resource.download_artifact_bundle.assert_called_once_with(uri, download_file)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_DOWNLOADED,
            ansible_facts={})

    def test_download_archives_artifact_bundle(self):
        artifact_bundle = self.TASK_CREATE['data']
        artifact_bundle['uri'] = '/rest/artifact-bundles/1'

        self.resource.get_by.return_value = [artifact_bundle]

        self.mock_ansible_module.params = self.TASK_DOWNLOAD_ARCHIVE

        ArtifactBundleModule().run()

        download_file = self.TASK_DOWNLOAD_ARCHIVE['data']['destinationFilePath']
        uri = artifact_bundle['uri']

        self.resource.download_archive_artifact_bundle.assert_called_once_with(uri, download_file)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_ARCHIVE_DOWNLOADED,
            ansible_facts={})

    def test_upload_artifact_bundle_should_upload_when_file_not_uploaded_yet(self):
        self.resource.get_by.return_value = []
        self.resource.upload_bundle_from_file.return_value = self.ARTIFACT_BUNDLE

        self.mock_ansible_module.params = self.TASK_UPLOAD

        ArtifactBundleModule().run()

        self.resource.upload_bundle_from_file.assert_called_once_with(
            self.TASK_UPLOAD['data']['localArtifactBundleFilePath'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_UPLOADED,
            ansible_facts=dict(artifact_bundle=self.ARTIFACT_BUNDLE))

    def test_upload_artifact_bundle_should_do_nothing_when_file_already_uploaded(self):
        self.resource.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.resource.upload_bundle_from_file.return_value = self.ARTIFACT_BUNDLE

        self.mock_ansible_module.params = self.TASK_UPLOAD

        ArtifactBundleModule().run()

        self.resource.get_by.assert_called_once_with('name', 'uploaded_artifact')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(artifact_bundle=self.ARTIFACT_BUNDLE))

    def test_upload_backup_artifact_bundle(self):
        self.resource.get_by.return_value = []
        self.resource.upload_backup_bundle_from_file.return_value = self.DEPLOYMENT_GROUP

        self.mock_ansible_module.params = self.TASK_BACKUP_UPLOAD

        ArtifactBundleModule().run()

        self.resource.upload_backup_bundle_from_file.assert_called_once_with(
            self.TASK_BACKUP_UPLOAD['data']['localBackupArtifactBundleFilePath'],
            self.TASK_BACKUP_UPLOAD['data']['deploymentGroupURI'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_BACKUP_UPLOADED,
            ansible_facts=dict(artifact_bundle_deployment_group=self.DEPLOYMENT_GROUP))

    def test_create_backup_artifact_bundle(self):
        artifact_bundle = self.TASK_CREATE['data']
        artifact_bundle['uri'] = '/rest/artifact-bundles/1'

        self.resource.create_backup.return_value = self.DEPLOYMENT_GROUP

        self.mock_ansible_module.params = self.TASK_CREATE_BACKUP

        ArtifactBundleModule().run()

        self.resource.create_backup.assert_called_once_with(
            self.TASK_CREATE_BACKUP['data'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_BACKUP_CREATED,
            ansible_facts=dict(artifact_bundle_deployment_group=self.DEPLOYMENT_GROUP))

    def test_extract_artifact_bundle(self):
        artifact_bundle = self.TASK_CREATE['data']
        artifact_bundle['uri'] = '/rest/artifact-bundles/1'

        self.resource.get_by.return_value = [artifact_bundle]

        self.resource.extract_bundle.return_value = artifact_bundle

        self.mock_ansible_module.params = self.TASK_EXTRACT

        ArtifactBundleModule().run()

        self.resource.extract_bundle.assert_called_once_with(artifact_bundle)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_EXTRACTED,
            ansible_facts=dict(artifact_bundle=artifact_bundle))

    def test_backup_extract_artifact_bundle(self):
        artifact_bundle = self.TASK_CREATE['data']
        artifact_bundle['uri'] = '/rest/artifact-bundles/1'

        self.resource.get_by.return_value = [artifact_bundle]

        self.resource.extract_backup_bundle.return_value = self.DEPLOYMENT_GROUP

        self.mock_ansible_module.params = self.TASK_BACKUP_EXTRACT

        ArtifactBundleModule().run()

        self.resource.extract_backup_bundle.assert_called_once_with(
            self.TASK_CREATE_BACKUP['data'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_BACKUP_EXTRACTED,
            ansible_facts=dict(artifact_bundle_deployment_group=self.DEPLOYMENT_GROUP))

    def test_update_artifact_bundle(self):
        artifact_bundle_updated = deepcopy(self.ARTIFACT_BUNDLE)
        artifact_bundle_updated['name'] = 'Artifact Bundle Updated'

        self.resource.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.resource.update.return_value = artifact_bundle_updated

        self.mock_ansible_module.params = self.TASK_UPDATE

        ArtifactBundleModule().run()

        self.resource.update.assert_called_once_with(
            artifact_bundle_updated
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_UPDATED,
            ansible_facts=dict(artifact_bundle=artifact_bundle_updated)
        )

    def test_update_artifact_bundle_by_newname(self):
        artifact_bundle_updated = deepcopy(self.ARTIFACT_BUNDLE)
        artifact_bundle_updated['name'] = 'Artifact Bundle Updated'

        self.resource.get_by.side_effect = [None, [self.ARTIFACT_BUNDLE]]
        self.resource.update.return_value = artifact_bundle_updated

        self.mock_ansible_module.params = self.TASK_UPDATE

        ArtifactBundleModule().run()

        self.resource.update.assert_called_once_with(
            artifact_bundle_updated
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_UPDATED,
            ansible_facts=dict(artifact_bundle=artifact_bundle_updated)
        )

    @mock.patch('image_streamer_artifact_bundle.compare')
    def test_should_do_nothing_when_no_changes_provided(self, mock_resource_compare):
        mock_resource_compare.return_value = True

        self.resource.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.mock_ansible_module.params = self.TASK_UPDATE

        ArtifactBundleModule().run()

        self.resource.create.not_been_called()
        self.resource.update.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(artifact_bundle=self.ARTIFACT_BUNDLE)
        )

    def test_should_do_nothing_when_no_newname_provided(self):
        self.resource.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.mock_ansible_module.params = self.TASK_CREATE

        ArtifactBundleModule().run()

        self.resource.create.not_been_called()
        self.resource.update.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(artifact_bundle=self.ARTIFACT_BUNDLE)
        )

    def test_delete_artifact_bundle(self):
        self.resource.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.resource.delete.return_value = self.ARTIFACT_BUNDLE

        self.mock_ansible_module.params = self.TASK_REMOVE

        ArtifactBundleModule().run()

        self.resource.delete.assert_called_once_with(
            self.ARTIFACT_BUNDLE
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_DELETED,
        )

    def test_should_do_nothing_when_already_absent(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = self.TASK_REMOVE

        ArtifactBundleModule().run()

        self.resource.delete.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_ALREADY_ABSENT,
        )


if __name__ == '__main__':
    pytest.main([__file__])
