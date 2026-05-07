# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data event definition configurations."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_event_definition_config
short_description: Manage VAST Data event definition configurations
description:
    - Create, update, and delete event definition configurations on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    event_definition_id:
        description:
            - The ID of the event definition.
        type: int
        required: true
    notification_target:
        description:
            - The notification target type.
        type: str
        choices: [EMAIL, SNMP, SYSLOG, WEBHOOK]
    target_address:
        description:
            - The target address for notifications.
        type: str
        required: true
    enabled:
        description:
            - Whether the event definition configuration is enabled.
        type: bool
        default: true
    state:
        description:
            - The desired state of the event definition configuration.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Configure email notification for an event
  stevefulme1.vastdata.vast_event_definition_config:
    event_definition_id: 1
    notification_target: EMAIL
    target_address: alerts@example.com
    enabled: true
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Configure SNMP trap for an event
  stevefulme1.vastdata.vast_event_definition_config:
    event_definition_id: 1
    notification_target: SNMP
    target_address: 192.168.1.100:162
    enabled: true
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Remove event definition configuration
  stevefulme1.vastdata.vast_event_definition_config:
    event_definition_id: 1
    notification_target: EMAIL
    target_address: alerts@example.com
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the event definition configuration.
    returned: on success
    type: dict
    sample:
        event_definition_id: 1
        notification_target: EMAIL
        target_address: alerts@example.com
        enabled: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastEventDefinitionConfig(VastResourceBase):
    resource_path = "/api/eventdefinitionconfigs/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "event_definition_id",
            "notification_target",
            "target_address",
            "enabled"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["notification_target", "target_address", "enabled"]


def main():
    module_args = dict(
        event_definition_id=dict(type="int", required=True),
        notification_target=dict(type="str", choices=["EMAIL", "SNMP", "SYSLOG", "WEBHOOK"]),
        target_address=dict(type="str", required=True),
        enabled=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastEventDefinitionConfig(module).run()


if __name__ == "__main__":
    main()
