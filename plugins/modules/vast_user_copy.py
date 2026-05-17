# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data user copy operations."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_user_copy
short_description: Manage VAST Data user copy operations
description:
    - Create, update, and delete user copy operations on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    source_user_id:
        description:
            - The ID of the source user to copy.
        type: int
        required: true
    target_tenant_id:
        description:
            - The ID of the target tenant.
        type: int
        required: true
    include_keys:
        description:
            - Whether to include keys in the copy operation.
        type: bool
        default: true
    state:
        description:
            - The desired state of the user copy operation.
        type: str
        default: present
        choices: [present, absent]
    limit:
        description:
            - Maximum number of results to return.
        type: int
        default: 100
    offset:
        description:
            - Number of results to skip for pagination.
        type: int
        default: 0
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Copy user to another tenant with keys
  stevefulme1.vastdata.vast_user_copy:
    source_user_id: 100
    target_tenant_id: 2
    include_keys: true
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Copy user to another tenant without keys
  stevefulme1.vastdata.vast_user_copy:
    source_user_id: 100
    target_tenant_id: 2
    include_keys: false
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Remove user copy configuration
  stevefulme1.vastdata.vast_user_copy:
    source_user_id: 100
    target_tenant_id: 2
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the user copy operation.
    returned: on success
    type: dict
    sample:
        source_user_id: 100
        target_tenant_id: 2
        include_keys: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastUserCopy(VastResourceBase):
    resource_path = "/api/usercopy/"

    def get_resource(self):
        """Look up user copy by source_user_id + target_tenant_id."""
        source_user_id = self.module.params["source_user_id"]
        target_tenant_id = self.module.params["target_tenant_id"]
        try:
            resources = self.client.get(self.resource_path)
            if isinstance(resources, list):
                for r in resources:
                    if (r.get("source_user_id") == source_user_id
                            and r.get("target_tenant_id") == target_tenant_id):
                        return r
        except Exception:
            pass
        return None

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "source_user_id",
            "target_tenant_id",
            "include_keys"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["include_keys"]


def main():
    module_args = dict(
        source_user_id=dict(type="int", required=True),
        target_tenant_id=dict(type="int", required=True),
        include_keys=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastUserCopy(module).run()


if __name__ == "__main__":
    main()
