# Copyright 2014 Hewlett-Packard Development Company, L.P.
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
#

from novaclient import exceptions as nova_exceptions
from oslo_log import log as logging

from trove.common import clients
from trove.common import exception
from trove.network import base

LOG = logging.getLogger(__name__)


class NovaNetwork(base.NetworkDriver):

    def __init__(self, context, region_name):
        try:
            self.client = clients.create_nova_client(
                context, region_name)
        except nova_exceptions.ClientException as e:
            raise exception.TroveError(str(e))

    def get_sec_group_by_id(self, group_id):
        try:
            return self.client.security_groups.get(group_id)
        except nova_exceptions.ClientException as e:
            LOG.exception('Failed to get remote security group')
            raise exception.TroveError(str(e))

    def delete_security_group(self, sec_group_id):
        try:
            self.client.security_groups.delete(sec_group_id)
        except nova_exceptions.ClientException as e:
            LOG.exception('Failed to delete remote security group')
            raise exception.SecurityGroupDeletionError(str(e))

    def delete_security_group_rule(self, sec_group_rule_id):
        try:
            self.client.security_group_rules.delete(sec_group_rule_id)

        except nova_exceptions.ClientException as e:
            LOG.exception('Failed to delete rule to remote security group')
            raise exception.SecurityGroupRuleDeletionError(str(e))
