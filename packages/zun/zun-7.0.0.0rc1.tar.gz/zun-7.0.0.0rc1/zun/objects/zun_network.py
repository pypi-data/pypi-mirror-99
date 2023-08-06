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

from oslo_versionedobjects import fields

from zun.db import api as dbapi
from zun.objects import base


@base.ZunObjectRegistry.register
class ZunNetwork(base.ZunPersistentObject, base.ZunObject):
    # Version 1.0: Initial version
    # Version 1.1: Add destroy method
    VERSION = '1.1'

    fields = {
        'id': fields.IntegerField(),
        'uuid': fields.UUIDField(nullable=True),
        'project_id': fields.StringField(nullable=True),
        'user_id': fields.StringField(nullable=True),
        'name': fields.StringField(nullable=True),
        'network_id': fields.StringField(nullable=True),
        'neutron_net_id': fields.StringField(nullable=True),
    }

    @staticmethod
    def _from_db_object(network, db_network):
        """Converts a database entity to a formal object."""
        for field in network.fields:
            setattr(network, field, db_network[field])

        network.obj_reset_changes()
        return network

    @staticmethod
    def _from_db_object_list(db_objects, cls, context):
        """Converts a list of database entities to a list of formal objects."""
        return [cls._from_db_object(cls(context), obj)
                for obj in db_objects]

    @base.remotable_classmethod
    def get_by_uuid(cls, context, uuid):
        """Find an network based on uuid and return a :class:`ZunNetwork` object.

        :param uuid: the uuid of a network.
        :param context: Security context
        :returns: a :class:`ZunNetwork` object.
        """
        db_network = dbapi.get_network_by_uuid(context, uuid)
        network = cls._from_db_object(cls(context), db_network)
        return network

    @base.remotable
    def create(self, context):
        """Create a ZunNetwork record in the DB.

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: ZunNetwork(context)

        """
        values = self.obj_get_changes()
        db_network = dbapi.create_network(context, values)
        self._from_db_object(self, db_network)

    @base.remotable_classmethod
    def list(cls, context, limit=None, marker=None,
             sort_key=None, sort_dir=None, filters=None):
        """Return a list of ZunNetwork objects.

        :param context: Security context.
        :param limit: maximum number of resources to return in a single result.
        :param marker: pagination marker for large data sets.
        :param sort_key: column to sort results by.
        :param sort_dir: direction to sort. "asc" or "desc".
        :param filters: filters when list networks.
        :returns: a list of :class:`ZunNetwork` object.

        """
        db_networks = dbapi.list_networks(
            context, limit=limit, marker=marker, sort_key=sort_key,
            sort_dir=sort_dir, filters=filters)
        return cls._from_db_object_list(db_networks, cls, context)

    @base.remotable
    def save(self, context=None):
        """Save updates to this ZunNetwork.

        Updates will be made column by column based on the result
        of self.what_changed().

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: ZunNetwork(context)
        """
        updates = self.obj_get_changes()
        dbapi.update_network(context, self.uuid, updates)

        self.obj_reset_changes()

    @base.remotable
    def destroy(self, context=None):
        dbapi.destroy_network(context, self.uuid)
        self.obj_reset_changes()
