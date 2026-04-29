# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Protection Policies."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_protection_policy
short_description: Manage VAST Data protection policies
description:
    - Create, update, and delete protection/retention policies on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the protection policy.
        type: str
        required: true
    prefix:
        description:
            - Prefix for snapshot naming.
        type: str
    clone_type:
        description:
            - Type of clone/replication.
        type: str
        choices: [NATIVE_REPLICATION, S3_REPLICATION, LOCAL]
    frames:
        description:
            - List of snapshot schedule frames.
            - Each frame is a dict with keys every, start_at, keep_local, keep_remote.
        type: list
        elements: dict
    indestructible:
        description:
            - Whether snapshots created by this policy are indestructible.
        type: bool
        default: false
    state:
        description:
            - The desired state of the protection policy.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create a protection policy with daily snapshots
  vastdata.cluster.vast_protection_policy:
    name: daily_protection
    prefix: daily
    clone_type: LOCAL
    frames:
      - every: 86400
        start_at: "00:00"
        keep_local: 7
        keep_remote: 0
    indestructible: false
    state: present

- name: Update protection policy to add remote replication
  vastdata.cluster.vast_protection_policy:
    name: daily_protection
    clone_type: NATIVE_REPLICATION
    frames:
      - every: 86400
        start_at: "00:00"
        keep_local: 7
        keep_remote: 14
    state: present

- name: Delete a protection policy
  vastdata.cluster.vast_protection_policy:
    name: daily_protection
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the protection policy.
    returned: on success
    type: dict
    sample: {
        "id": 42,
        "name": "daily_protection",
        "prefix": "daily",
        "clone_type": "LOCAL",
        "frames": [
            {
                "every": 86400,
                "start_at": "00:00",
                "keep_local": 7,
                "keep_remote": 0
            }
        ],
        "indestructible": false
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase

class VastProtectionPolicy(VastResourceBase):
    resource_path = "/api/protectionpolicies/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in ["name", "prefix", "clone_type", "frames", "indestructible"] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["prefix", "clone_type", "frames", "indestructible"]

def main():
    module_args = dict(
        name=dict(type="str", required=True),
        prefix=dict(type="str"),
        clone_type=dict(type="str", choices=["NATIVE_REPLICATION", "S3_REPLICATION", "LOCAL"]),
        frames=dict(type="list", elements="dict"),
        indestructible=dict(type="bool", default=False),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastProtectionPolicy(module).run()

if __name__ == "__main__":
    main()
