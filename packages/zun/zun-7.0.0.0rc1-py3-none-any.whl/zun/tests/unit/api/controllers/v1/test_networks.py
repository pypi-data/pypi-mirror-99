# Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from unittest.mock import patch

from zun.tests.unit.api import base as api_base
from zun.tests.unit.db import utils


class TestNetworkController(api_base.FunctionalTest):
    @patch('zun.common.policy.enforce')
    @patch('zun.compute.api.API.network_create')
    def test_network_create(self, mock_network_create, mock_policy):
        mock_policy.return_value = True
        test_object = utils.create_test_network(context=self.context)
        mock_network_create.return_value = test_object
        params = ('{"name": "network-test", "neutron_net_id": "test-id"}')
        response = self.post('/v1/networks/',
                             params=params,
                             content_type='application/json')

        self.assertEqual(200, response.status_int)
        self.assertTrue(mock_network_create.called)

    @patch('zun.objects.ZunNetwork.list')
    @patch('zun.common.policy.enforce')
    @patch('zun.compute.api.API.network_delete')
    def test_network_delete(self, mock_network_delete, mock_policy,
                            mock_network_list):
        mock_policy.return_value = True
        test_object = utils.create_test_network(context=self.context)
        mock_network_list.return_value = [test_object]
        response = self.delete('/v1/networks/%s' % test_object.get('uuid'))
        self.assertEqual(204, response.status_int)
        self.assertTrue(mock_network_delete.called)
