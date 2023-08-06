# Copyright 2016 Intel.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from cinderclient import client as cinderclient
from glanceclient import client as glanceclient
from keystoneauth1.loading import adapter as ka_adapter
from neutronclient.v2_0 import client as neutronclient

from zun.common import exception
from zun.common import keystone
import zun.conf


class OpenStackClients(object):
    """Convenience class to create and cache client instances."""

    def __init__(self, context):
        self.context = context
        self._keystone = None
        self._glance = None
        self._neutron = None
        self._cinder = None
        self._placement = None
        self._placement_ks_filter = None

    def url_for(self, **kwargs):
        return self.keystone().session.get_endpoint(**kwargs)

    def zun_url(self):
        endpoint_type = self._get_client_option('zun', 'endpoint_type')
        region_name = self._get_client_option('zun', 'region_name')
        return self.url_for(service_type='container',
                            interface=endpoint_type,
                            region_name=region_name)

    @property
    def auth_token(self):
        return self.context.auth_token or self.keystone().auth_token

    def keystone(self):
        if self._keystone:
            return self._keystone

        self._keystone = keystone.KeystoneClientV3(self.context)
        return self._keystone

    def _get_client_option(self, client, option):
        return getattr(getattr(zun.conf.CONF, '%s_client' % client), option)

    @exception.wrap_keystone_exception
    def glance(self):
        if self._glance:
            return self._glance

        glanceclient_version = self._get_client_option('glance', 'api_version')
        session = self.keystone().session

        endpoint_type = self._get_client_option('glance', 'endpoint_type')
        region_name = self._get_client_option('glance', 'region_name')
        glance_url = self.url_for(service_type='image',
                                  interface=endpoint_type,
                                  region_name=region_name)

        self._glance = glanceclient.Client(glanceclient_version,
                                           endpoint=glance_url,
                                           session=session)

        return self._glance

    @exception.wrap_keystone_exception
    def neutron(self):
        if self._neutron:
            return self._neutron

        session = self.keystone().session
        if self._get_client_option('neutron', 'ca_file'):
            session.verify = self._get_client_option('neutron', 'ca_file')
        if self._get_client_option('neutron', 'insecure'):
            session.verify = False
        endpoint_type = self._get_client_option('neutron', 'endpoint_type')
        region_name = self._get_client_option('neutron', 'region_name')
        self._neutron = neutronclient.Client(session=session,
                                             endpoint_type=endpoint_type,
                                             region_name=region_name)

        return self._neutron

    @exception.wrap_keystone_exception
    def cinder(self):
        if self._cinder:
            return self._cinder

        session = self.keystone().session
        if self._get_client_option('cinder', 'ca_file'):
            session.verify = self._get_client_option('cinder', 'ca_file')
        if self._get_client_option('cinder', 'insecure'):
            session.verify = False
        cinder_api_version = self._get_client_option('cinder', 'api_version')
        region_name = self._get_client_option('cinder', 'region_name')
        endpoint_type = self._get_client_option('cinder', 'endpoint_type')
        kwargs = {
            'session': self.keystone().session,
            'endpoint_type': endpoint_type,
            'region_name': region_name,
            'cacert': self._get_client_option('cinder', 'ca_file'),
            'insecure': self._get_client_option('cinder', 'insecure')
        }
        self._cinder = cinderclient.Client(version=cinder_api_version,
                                           **kwargs)

        return self._cinder

    @exception.wrap_keystone_exception
    def placement(self):
        if self._placement:
            return self._placement, self._placement_ks_filter

        session = self.keystone().session
        if self._get_client_option('placement', 'ca_file'):
            session.verify = self._get_client_option('placement', 'ca_file')
        if self._get_client_option('placement', 'insecure'):
            session.verify = False
        region_name = self._get_client_option('placement', 'region_name')
        endpoint_type = self._get_client_option('placement', 'endpoint_type')
        kwargs = {
            'session': self.keystone().session,
            'auth': self.keystone().auth,
        }
        self._placement_ks_filter = {'service_type': 'placement',
                                     'region_name': region_name,
                                     'interface': endpoint_type}
        self._placement = ka_adapter.Adapter().load_from_options(**kwargs)

        return self._placement, self._placement_ks_filter
