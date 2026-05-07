# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data event definitions."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_event_definition
short_description: Manage VAST Data event definitions
description:
    - Create, update, and delete event definitions on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the event definition.
        type: str
        required: true
    event_type:
        description:
            - The type of event.
        type: str
        required: true
        choices: [CAPACITY, HARDWARE, PERFORMANCE, SYSTEM, SECURITY, CLUSTER, CUSTOM]
    severity:
        description:
            - The severity level of the event.
        type: str
        choices: [INFO, MINOR, MAJOR, CRITICAL]
    enabled:
        description:
            - Whether the event definition is enabled.
        type: bool
        default: true
    description:
        description:
            - Description of the event definition.
        type: str
    state:
        description:
            - The desired state of the event definition.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create a critical capacity event definition
  stevefulme1.vastdata.vast_event_definition:
    name: capacity_alert_90
    event_type: CAPACITY
    severity: CRITICAL
    enabled: true
    description: Alert when capacity exceeds 90%
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Update event definition severity
  stevefulme1.vastdata.vast_event_definition:
    name: capacity_alert_90
    event_type: CAPACITY
    severity: MAJOR
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete an event definition
  stevefulme1.vastdata.vast_event_definition:
    name: capacity_alert_90
    event_type: CAPACITY
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the event definition.
    returned: on success
    type: dict
    sample:
        id: 1
        name: capacity_alert_90
        event_type: CAPACITY
        severity: CRITICAL
        enabled: true
        description: Alert when capacity exceeds 90%
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastEventDefinition(VastResourceBase):
    resource_path = "/api/eventdefinitions/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "event_type",
            "severity",
            "enabled",
            "description"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["severity", "enabled", "description"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        event_type=dict(
            type="str", required=True,
            choices=["CAPACITY", "HARDWARE", "PERFORMANCE", "SYSTEM", "SECURITY", "CLUSTER", "CUSTOM"],
        ),
        severity=dict(type="str", choices=["INFO", "MINOR", "MAJOR", "CRITICAL"]),
        enabled=dict(type="bool", default=True),
        description=dict(type="str"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastEventDefinition(module).run()


if __name__ == "__main__":
    main()
