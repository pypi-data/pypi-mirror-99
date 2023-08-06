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

from oslo_utils import uuidutils

from zun.common import exception
import zun.conf
from zun.db import api as dbapi
from zun.tests.unit.db import base
from zun.tests.unit.db import utils

CONF = zun.conf.CONF


class DbNetworkTestCase(base.DbTestCase):

    def setUp(self):
        super(DbNetworkTestCase, self).setUp()

    def test_create_network(self):
        utils.create_test_network(context=self.context)

    def test_create_network_already_exists(self):
        utils.create_test_network(context=self.context,
                                  uuid='123', neutron_net_id='456')
        with self.assertRaisesRegex(exception.NetworkAlreadyExists,
                                    'A network with UUID 123.*'):
            utils.create_test_network(context=self.context, uuid='123')
        with self.assertRaisesRegex(exception.NetworkAlreadyExists,
                                    'A network with neutron_net_id 456.*'):
            utils.create_test_network(context=self.context,
                                      neutron_net_id='456')

    def test_list_networks(self):
        uuids = []
        for i in range(1, 6):
            network = utils.create_test_network(
                uuid=uuidutils.generate_uuid(),
                context=self.context,
                neutron_net_id=uuidutils.generate_uuid(),
                name='network' + str(i))
            uuids.append(str(network['uuid']))
        res = dbapi.list_networks(self.context)
        res_uuids = [r.uuid for r in res]
        self.assertEqual(sorted(uuids), sorted(res_uuids))
