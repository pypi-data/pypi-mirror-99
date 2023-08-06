# Copyright (c) 2010 OpenStack Foundation
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
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

"""
Scheduler base class that all Schedulers should inherit from
"""

import abc

from zun.api import servicegroup
from zun import objects


class Scheduler(object, metaclass=abc.ABCMeta):
    """The base class that all Scheduler classes should inherit from."""

    def __init__(self):
        self.servicegroup_api = servicegroup.ServiceGroup()

    def hosts_up(self, context):
        """Return the list of hosts that have a running service."""

        services = objects.ZunService.list_by_binary(context, 'zun-compute')
        return [service.host
                for service in services
                if self.servicegroup_api.service_is_up(service) and
                not service.disabled]

    @abc.abstractmethod
    def select_destinations(self, context, containers, extra_specs,
                            alloc_reqs_by_rp_uuid, provider_summaries,
                            allocation_request_version=None):
        """Must override select_destinations method.

        :return: A list of dicts with 'host', 'nodename' and 'limits' as keys
            that satisfies the extra_specs and filter_properties.
        """
        raise NotImplementedError()
