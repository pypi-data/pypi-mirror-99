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

from oslo_log import log as logging
from oslo_versionedobjects import fields

from zun.common import consts
from zun.common import exception
from zun.common.i18n import _
from zun.db import api as dbapi
from zun.objects import base
from zun.objects import exec_instance as exec_inst
from zun.objects import fields as z_fields
from zun.objects import pci_device
from zun.objects import registry


LOG = logging.getLogger(__name__)


CONTAINER_OPTIONAL_ATTRS = ["pci_devices", "exec_instances", "registry"]


@base.ZunObjectRegistry.register
class Cpuset(base.ZunObject):
    VERSION = '1.0'

    fields = {
        'cpuset_cpus': fields.SetOfIntegersField(nullable=True),
        'cpuset_mems': fields.SetOfIntegersField(nullable=True),
    }

    def _to_dict(self):
        return {
            'cpuset_cpus': self.cpuset_cpus,
            'cpuset_mems': self.cpuset_mems
        }

    @classmethod
    def _from_dict(cls, data_dict):
        if not data_dict:
            obj = cls(cpuset_cpus=None, cpuset_mems=None)
        else:
            cpuset_cpus = data_dict.get('cpuset_cpus')
            cpuset_mems = data_dict.get('cpuset_mems')
            obj = cls(cpuset_cpus=cpuset_cpus, cpuset_mems=cpuset_mems)
        obj.obj_reset_changes()
        return obj


class ContainerBase(base.ZunPersistentObject, base.ZunObject):

    fields = {
        'id': fields.IntegerField(),
        'container_id': fields.StringField(nullable=True),
        'uuid': fields.UUIDField(nullable=True),
        'name': fields.StringField(nullable=True),
        'project_id': fields.StringField(nullable=True),
        'user_id': fields.StringField(nullable=True),
        'image': fields.StringField(nullable=True),
        'cpu': fields.FloatField(nullable=True),
        'cpu_policy': fields.StringField(nullable=True),
        'cpuset': fields.ObjectField("Cpuset", nullable=True),
        'memory': fields.StringField(nullable=True),
        'command': fields.ListOfStringsField(nullable=True),
        'status': z_fields.ContainerStatusField(nullable=True),
        'status_reason': fields.StringField(nullable=True),
        'task_state': z_fields.TaskStateField(nullable=True),
        'environment': fields.DictOfStringsField(nullable=True),
        'workdir': fields.StringField(nullable=True),
        'auto_remove': fields.BooleanField(nullable=True),
        'ports': z_fields.ListOfIntegersField(nullable=True),
        'hostname': fields.StringField(nullable=True),
        'labels': fields.DictOfStringsField(nullable=True),
        'addresses': z_fields.JsonField(nullable=True),
        'image_pull_policy': fields.StringField(nullable=True),
        'host': fields.StringField(nullable=True),
        'restart_policy': fields.DictOfStringsField(nullable=True),
        'status_detail': fields.StringField(nullable=True),
        'interactive': fields.BooleanField(nullable=True),
        'tty': fields.BooleanField(nullable=True),
        'image_driver': fields.StringField(nullable=True),
        'websocket_url': fields.StringField(nullable=True),
        'websocket_token': fields.StringField(nullable=True),
        'security_groups': fields.ListOfStringsField(nullable=True),
        'runtime': fields.StringField(nullable=True),
        'pci_devices': fields.ListOfObjectsField('PciDevice',
                                                 nullable=True),
        'disk': fields.IntegerField(nullable=True),
        'auto_heal': fields.BooleanField(nullable=True),
        'started_at': fields.DateTimeField(tzinfo_aware=False, nullable=True),
        'exposed_ports': z_fields.JsonField(nullable=True),
        'exec_instances': fields.ListOfObjectsField('ExecInstance',
                                                    nullable=True),
        'privileged': fields.BooleanField(nullable=True),
        'healthcheck': z_fields.JsonField(nullable=True),
        'registry_id': fields.IntegerField(nullable=True),
        'registry': fields.ObjectField("Registry", nullable=True),
        'annotations': z_fields.JsonField(nullable=True),
        'cni_metadata': z_fields.JsonField(nullable=True),
        'entrypoint': fields.ListOfStringsField(nullable=True),
    }

    # should be redefined in subclasses
    container_type = None

    @staticmethod
    def _from_db_object(container, db_container):
        """Converts a database entity to a formal object."""
        for field in container.fields:
            if field in ['pci_devices', 'exec_instances', 'registry',
                         'containers', 'init_containers']:
                continue
            if field == 'cpuset':
                container.cpuset = Cpuset._from_dict(
                    db_container['cpuset'])
                continue
            setattr(container, field, db_container[field])

        container.obj_reset_changes()
        return container

    @staticmethod
    def _from_db_object_list(db_objects, cls, context):
        """Converts a list of database entities to a list of formal objects."""
        return [cls._from_db_object(cls(context), obj)
                for obj in db_objects]

    @base.remotable_classmethod
    def get_by_uuid(cls, context, uuid):
        """Find a container based on uuid and return a :class:`Container` object.

        :param uuid: the uuid of a container.
        :param context: Security context
        :returns: a :class:`Container` object.
        """
        db_container = dbapi.get_container_by_uuid(context, cls.container_type,
                                                   uuid)
        container = cls._from_db_object(cls(context), db_container)
        return container

    @base.remotable_classmethod
    def get_by_name(cls, context, name):
        """Find a container based on name and return a Container object.

        :param name: the logical name of a container.
        :param context: Security context
        :returns: a :class:`Container` object.
        """
        db_container = dbapi.get_container_by_name(context, cls.container_type,
                                                   name)
        container = cls._from_db_object(cls(context), db_container)
        return container

    @staticmethod
    def get_container_any_type(context, uuid):
        """Find a container of any type based on uuid.

        :param uuid: the uuid of a container.
        :param context: Security context
        :returns: a :class:`ContainerBase` object.
        """
        db_container = dbapi.get_container_by_uuid(context, consts.TYPE_ANY,
                                                   uuid)
        type = db_container['container_type']
        if type == consts.TYPE_CONTAINER:
            container_cls = Container
        elif type == consts.TYPE_CAPSULE:
            container_cls = Capsule
        elif type == consts.TYPE_CAPSULE_CONTAINER:
            container_cls = CapsuleContainer
        elif type == consts.TYPE_CAPSULE_INIT_CONTAINER:
            container_cls = CapsuleInitContainer
        else:
            raise exception.ZunException(_('Unknown container type: %s'), type)

        obj = container_cls(context)
        container = container_cls._from_db_object(obj, db_container)
        return container

    @base.remotable_classmethod
    def list(cls, context, limit=None, marker=None,
             sort_key=None, sort_dir=None, filters=None):
        """Return a list of Container objects.

        :param context: Security context.
        :param limit: maximum number of resources to return in a single result.
        :param marker: pagination marker for large data sets.
        :param sort_key: column to sort results by.
        :param sort_dir: direction to sort. "asc" or "desc".
        :param filters: filters when list containers, the filter name could be
                        'name', 'image', 'project_id', 'user_id', 'memory'.
                        For example, filters={'image': 'nginx'}
        :returns: a list of :class:`Container` object.

        """
        db_containers = dbapi.list_containers(
            context, cls.container_type, limit=limit, marker=marker,
            sort_key=sort_key, sort_dir=sort_dir, filters=filters)
        return cls._from_db_object_list(db_containers, cls, context)

    @base.remotable_classmethod
    def list_by_host(cls, context, host):
        """Return a list of Container objects by host.

        :param context: Security context.
        :param host: A compute host.
        :returns: a list of :class:`Container` object.

        """
        db_containers = dbapi.list_containers(context, cls.container_type,
                                              filters={'host': host})
        return cls._from_db_object_list(db_containers, cls, context)

    @base.remotable
    def create(self, context):
        """Create a Container record in the DB.

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Container(context)

        """
        values = self.obj_get_changes()
        cpuset_obj = values.pop('cpuset', None)
        if cpuset_obj is not None:
            values['cpuset'] = cpuset_obj._to_dict()
        annotations = values.pop('annotations', None)
        if annotations is not None:
            values['annotations'] = self.fields['annotations'].to_primitive(
                self, 'annotations', self.annotations)
        cni_metadata = values.pop('cni_metadata', None)
        if cni_metadata is not None:
            values['cni_metadata'] = self.fields['cni_metadata'].to_primitive(
                self, 'cni_metadata', self.cni_metadata)
        values['container_type'] = self.container_type
        db_container = dbapi.create_container(context, values)
        self._from_db_object(self, db_container)

    @base.remotable
    def destroy(self, context=None):
        """Delete the Container from the DB.

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Container(context)
        """
        dbapi.destroy_container(context, self.container_type, self.uuid)
        self.obj_reset_changes()

    @base.remotable
    def save(self, context=None):
        """Save updates to this Container.

        Updates will be made column by column based on the result
        of self.what_changed().

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Container(context)
        """
        updates = self.obj_get_changes()
        cpuset_obj = updates.pop('cpuset', None)
        if cpuset_obj is not None:
            updates['cpuset'] = cpuset_obj._to_dict()
        annotations = updates.pop('annotations', None)
        if annotations is not None:
            updates['annotations'] = self.fields['annotations'].to_primitive(
                self, 'annotations', self.annotations)
        cni_metadata = updates.pop('cni_metadata', None)
        if cni_metadata is not None:
            updates['cni_metadata'] = self.fields['cni_metadata'].to_primitive(
                self, 'cni_metadata', self.cni_metadata)
        dbapi.update_container(context, self.container_type, self.uuid,
                               updates)

        self.obj_reset_changes()

    @base.remotable
    def refresh(self, context=None):
        """Loads updates for this Container.

        Loads a container with the same uuid from the database and
        checks for updated attributes. Updates are applied from
        the loaded container column by column, if there are any updates.

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Container(context)
        """
        current = self.__class__.get_by_uuid(self._context, uuid=self.uuid)
        for field in self.fields:
            if self.obj_attr_is_set(field) and \
               getattr(self, field) != getattr(current, field):
                setattr(self, field, getattr(current, field))

    def obj_load_attr(self, attrname):
        if attrname not in CONTAINER_OPTIONAL_ATTRS:
            raise exception.ObjectActionError(
                action='obj_load_attr',
                reason=_('attribute %s not lazy-loadable') % attrname)

        if not self._context:
            raise exception.OrphanedObjectError(method='obj_load_attr',
                                                objtype=self.obj_name())

        LOG.debug("Lazy-loading '%(attr)s' on %(name)s uuid %(uuid)s",
                  {'attr': attrname,
                   'name': self.obj_name(),
                   'uuid': self.uuid,
                   })

        # NOTE(danms): We handle some fields differently here so that we
        # can be more efficient
        if attrname == 'pci_devices':
            self._load_pci_devices()

        if attrname == 'exec_instances':
            self._load_exec_instances()

        if attrname == 'registry':
            self._load_registry()

        self.obj_reset_changes([attrname])

    def _load_pci_devices(self):
        self.pci_devices = pci_device.PciDevice.list_by_container_uuid(
            self._context, self.uuid)

    def _load_exec_instances(self):
        self.exec_instances = exec_inst.ExecInstance.list_by_container_id(
            self._context, self.id)

    def _load_registry(self):
        self.registry = None
        if self.registry_id:
            self.registry = registry.Registry.get_by_id(
                self._context, self.registry_id)

    @base.remotable_classmethod
    def get_count(cls, context, project_id, flag):
        """Get the counts of Container objects in the database.

        :param context: The request context for database access.
        :param project_id: The project_id to count across.
        :param flag: The name of resource, one of the following options:
                     - containers: Count the number of containers owned by the
                     project.
                     - memory: The sum of containers's memory.
                     - cpu: The sum of container's cpu.
                     - disk: The sum of container's disk size.
        """
        usage = dbapi.count_usage(context, cls.container_type, project_id,
                                  flag)[0] or 0.0
        return usage


@base.ZunObjectRegistry.register
class Container(ContainerBase):
    # Version 1.0: Initial version
    # Version 1.1: Add container_id column
    # Version 1.2: Add memory column
    # Version 1.3: Add task_state column
    # Version 1.4: Add cpu, workdir, ports, hostname and labels columns
    # Version 1.5: Add meta column
    # Version 1.6: Add addresses column
    # Version 1.7: Add host column
    # Version 1.8: Add restart_policy
    # Version 1.9: Add status_detail column
    # Version 1.10: Add tty, stdin_open
    # Version 1.11: Add image_driver
    # Version 1.12: Add 'Created' to ContainerStatus
    # Version 1.13: Add more task states for container
    # Version 1.14: Add method 'list_by_host'
    # Version 1.15: Combine tty and stdin_open
    # Version 1.16: Add websocket_url and token
    # Version 1.17: Add security_groups
    # Version 1.18: Add auto_remove
    # Version 1.19: Add runtime column
    # Version 1.20: Change runtime to String type
    # Version 1.21: Add pci_device attribute
    # Version 1.22: Add 'Deleting' to ContainerStatus
    # Version 1.23: Add the missing 'pci_devices' attribute
    # Version 1.24: Add the storage_opt attribute
    # Version 1.25: Change TaskStateField definition
    # Version 1.26:  Add auto_heal
    # Version 1.27: Make auto_heal field nullable
    # Version 1.28: Add 'Dead' to ContainerStatus
    # Version 1.29: Add 'Restarting' to ContainerStatus
    # Version 1.30: Add capsule_id attribute
    # Version 1.31: Add 'started_at' attribute
    # Version 1.32: Add 'exec_instances' attribute
    # Version 1.33: Change 'command' to List type
    # Version 1.34: Add privileged to container
    # Version 1.35: Add 'healthcheck' attribute
    # Version 1.36: Add 'get_count' method
    # Version 1.37: Add 'exposed_ports' attribute
    # Version 1.38: Add 'cpuset' attribute
    # Version 1.39: Add 'register' and 'registry_id' attributes
    # Version 1.40: Add 'tty' attributes
    # Version 1.41: Add 'annotations' attributes
    # Version 1.42: Remove 'meta' attribute
    # Version 1.43: Add 'cni_metadata' attribute
    # Version 1.44: Add 'entrypoint' attribute
    VERSION = '1.44'

    container_type = consts.TYPE_CONTAINER


@base.ZunObjectRegistry.register
class Capsule(ContainerBase):
    # Version 1.0: Initial version
    # Version 1.1: Add 'tty' attributes
    # Version 1.2: Add 'annotations' attributes
    # Version 1.3: Remove 'meta' attribute
    # Version 1.4: Add 'cni_metadata' attribute
    VERSION = '1.4'

    container_type = consts.TYPE_CAPSULE

    fields = {
        'containers': fields.ListOfObjectsField('CapsuleContainer',
                                                nullable=True),
        'init_containers': fields.ListOfObjectsField('CapsuleInitContainer',
                                                     nullable=True),
    }

    def as_dict(self):
        capsule_dict = super(Capsule, self).as_dict()
        capsule_dict['containers'] = [c.as_dict() for c in self.containers]
        capsule_dict['init_containers'] = [c.as_dict()
                                           for c in self.init_containers]
        return capsule_dict

    def obj_load_attr(self, attrname):
        if attrname == 'containers':
            self._load_capsule_containers()
            self.obj_reset_changes([attrname])
        elif attrname == 'init_containers':
            self._load_capsule_init_containers()
            self.obj_reset_changes([attrname])
        else:
            super(Capsule, self).obj_load_attr(attrname)

    def _load_capsule_containers(self):
        self.containers = CapsuleContainer.list_by_capsule_id(
            self._context, self.id)

    def _load_capsule_init_containers(self):
        self.init_containers = CapsuleInitContainer.list_by_capsule_id(
            self._context, self.id)


@base.ZunObjectRegistry.register
class CapsuleContainer(ContainerBase):
    # Version 1.0: Initial version
    # Version 1.1: Add 'tty' attributes
    # Version 1.2: Add 'annotations' attributes
    # Version 1.3: Remove 'meta' attribute
    # Version 1.4: Add 'cni_metadata' attribute
    VERSION = '1.4'

    container_type = consts.TYPE_CAPSULE_CONTAINER

    fields = {
        'capsule_id': fields.IntegerField(nullable=False),
    }

    @base.remotable_classmethod
    def list_by_capsule_id(cls, context, capsule_id):
        """Return a list of Container objects by capsule_id.

        :param context: Security context.
        :param host: A capsule id.
        :returns: a list of :class:`Container` object.

        """
        db_containers = dbapi.list_containers(
            context, cls.container_type, filters={'capsule_id': capsule_id})
        return Container._from_db_object_list(db_containers, cls, context)


@base.ZunObjectRegistry.register
class CapsuleInitContainer(ContainerBase):
    # Version 1.0: Initial version
    # Version 1.1: Add 'tty' attributes
    # Version 1.2: Add 'annotations' attributes
    # Version 1.3: Remove 'meta' attribute
    # Version 1.4: Add 'cni_metadata' attribute
    VERSION = '1.4'

    container_type = consts.TYPE_CAPSULE_INIT_CONTAINER

    fields = {
        'capsule_id': fields.IntegerField(nullable=False),
    }

    @base.remotable_classmethod
    def list_by_capsule_id(cls, context, capsule_id):
        """Return a list of Container objects by capsule_id.

        :param context: Security context.
        :param host: A capsule id.
        :returns: a list of :class:`Container` object.

        """
        db_containers = dbapi.list_containers(
            context, cls.container_type, filters={'capsule_id': capsule_id})
        return Container._from_db_object_list(db_containers, cls, context)
