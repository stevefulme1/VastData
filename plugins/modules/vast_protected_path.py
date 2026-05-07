# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Protected Paths."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_protected_path
short_description: Manage VAST Data protected paths
description:
    - Create, update, and delete protected paths on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the protected path.
        type: str
        required: true
    source_dir:
        description:
            - The source directory path to protect.
        type: str
        required: true
    tenant_id:
        description:
            - ID of the tenant this protected path belongs to.
        type: int
    protection_policy_id:
        description:
            - ID of the protection policy to apply.
        type: int
    state:
        description:
            - The desired state of the protected path.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create a protected path
  stevefulme1.vastdata.vast_protected_path:
    name: critical_data_protection
    source_dir: /data/critical
    protection_policy_id: 1
    tenant_id: 1
    state: present

- name: Update protected path policy
  stevefulme1.vastdata.vast_protected_path:
    name: critical_data_protection
    source_dir: /data/critical
    protection_policy_id: 2
    state: present

- name: Delete a protected path
  stevefulme1.vastdata.vast_protected_path:
    name: critical_data_protection
    source_dir: /data/critical
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the protected path.
    returned: on success
    type: dict
    sample:
        id: 1
        name: critical_data_protection
        source_dir: /data/critical
        protection_policy_id: 1
        tenant_id: 1
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastProtectedPath(VastResourceBase):
    resource_path = "/api/protectedpaths/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "source_dir",
            "tenant_id",
            "protection_policy_id"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["protection_policy_id"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        source_dir=dict(type="str", required=True),
        tenant_id=dict(type="int"),
        protection_policy_id=dict(type="int"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastProtectedPath(module).run()


if __name__ == "__main__":
    main()
