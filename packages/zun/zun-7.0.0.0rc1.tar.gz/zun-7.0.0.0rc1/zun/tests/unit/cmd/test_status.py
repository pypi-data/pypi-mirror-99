# Copyright (c) 2018 NEC, Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from unittest import mock

from oslo_upgradecheck.upgradecheck import Code

from zun.cmd import status
from zun.tests import base


class TestUpgradeChecks(base.TestCase):

    def setUp(self):
        super(TestUpgradeChecks, self).setUp()
        self.cmd = status.Checks()

    @mock.patch.object(status.Checks, "_cmd_exists")
    def test__numactl_check_ok(self, mock_cmd_exists):
        mock_cmd_exists.return_value = True
        check_result = self.cmd._numactl_check()
        self.assertEqual(
            Code.SUCCESS, check_result.code)

    @mock.patch.object(status.Checks, "_cmd_exists")
    def test__numactl_check_fail(self, mock_cmd_exists):
        mock_cmd_exists.return_value = False
        check_result = self.cmd._numactl_check()
        self.assertEqual(
            Code.FAILURE, check_result.code)
