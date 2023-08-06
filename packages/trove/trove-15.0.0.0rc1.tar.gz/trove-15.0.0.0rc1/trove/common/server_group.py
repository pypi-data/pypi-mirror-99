# Copyright 2016 Tesora, Inc.
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

from oslo_log import log as logging

from trove.common.clients import create_nova_client


LOG = logging.getLogger(__name__)


class ServerGroup(object):

    @classmethod
    def load(cls, context, instance_id):
        client = create_nova_client(context)
        server_group = None
        expected_name = "locality_%s" % instance_id
        try:
            for sg in client.server_groups.list():
                if sg.name == expected_name:
                    server_group = sg
        except Exception:
            LOG.exception("Could not load server group for instance %s",
                          instance_id)

        if not server_group:
            LOG.info('No server group found for instance %s', instance_id)

        return server_group

    @classmethod
    def create(cls, context, locality, name_suffix):
        client = create_nova_client(context)
        server_group_name = "%s_%s" % ('locality', name_suffix)
        server_group = client.server_groups.create(
            name=server_group_name, policies=[locality])
        LOG.debug("Created '%(locality)s' server group called %(group_name)s "
                  "(id: %(group_id)s).",
                  {'locality': locality, 'group_name': server_group_name,
                   'group_id': server_group.id})

        return server_group

    @classmethod
    def delete(cls, context, server_group, force=False):
        # Only delete the server group if we're the last member in it, or if
        # it has no members
        if server_group:
            if force or len(server_group.members) <= 1:
                LOG.info("Deleting server group %s", server_group.id)
                client = create_nova_client(context)
                client.server_groups.delete(server_group.id)
            else:
                LOG.debug("Skipping delete of server group %(id)s "
                          "(members: %(members)s).",
                          {'id': server_group.id,
                           'members': server_group.members})

    @classmethod
    def convert_to_hint(cls, server_group, hints=None):
        if server_group:
            hints = hints or {}
            hints["group"] = server_group.id
        return hints

    @classmethod
    def build_scheduler_hint(cls, context, locality, name_suffix):
        scheduler_hint = None
        if locality:
            # Build the scheduler hint, but only if locality's a string
            if isinstance(locality, str):
                server_group = cls.create(
                    context, locality, name_suffix)
                scheduler_hint = cls.convert_to_hint(
                    server_group)
            else:
                # otherwise assume it's already in hint form (i.e. a dict)
                scheduler_hint = locality
        return scheduler_hint

    @classmethod
    def get_locality(cls, server_group):
        locality = None
        if server_group:
            locality = server_group.policies[0]
        return locality
