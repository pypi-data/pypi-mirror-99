# Copyright 2015 OpenStack Foundation
# All Rights Reserved.
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

from testtools.matchers import HasLength

from zun import objects
from zun.tests.unit.db import base
from zun.tests.unit.db import utils


class TestNetworkObject(base.DbTestCase):

    def setUp(self):
        super(TestNetworkObject, self).setUp()
        self.fake_network = utils.get_test_network()

    def test_create(self):
        with mock.patch.object(self.dbapi, 'create_network',
                               autospec=True) as mock_create_network:
            mock_create_network.return_value = self.fake_network
            network = objects.ZunNetwork(self.context, **self.fake_network)
            network.create(self.context)
            mock_create_network.assert_called_once_with(self.context,
                                                        self.fake_network)
            self.assertEqual(self.context, network._context)

    def test_save(self):
        uuid = self.fake_network['uuid']
        with mock.patch.object(self.dbapi, 'get_network_by_uuid',
                               autospec=True) as mock_get_network:
            mock_get_network.return_value = self.fake_network
            with mock.patch.object(self.dbapi, 'update_network',
                                   autospec=True) as mock_update_network:
                network = objects.ZunNetwork.get_by_uuid(self.context, uuid)
                network.name = 'network-test'
                network.neutron_net_id = 'test-id'
                network.save()
                mock_get_network.assert_called_once_with(self.context, uuid)
                params = {'name': 'network-test', 'neutron_net_id': 'test-id'}
                mock_update_network.assert_called_once_with(None,
                                                            uuid,
                                                            params)
                self.assertEqual(self.context, network._context)

    def test_list(self):
        with mock.patch.object(self.dbapi, 'list_networks',
                               autospec=True) as mock_get_list:
            mock_get_list.return_value = [self.fake_network]
            networks = objects.ZunNetwork.list(self.context)
            self.assertEqual(1, mock_get_list.call_count)
            self.assertThat(networks, HasLength(1))
            self.assertIsInstance(networks[0], objects.ZunNetwork)
            self.assertEqual(self.context, networks[0]._context)
