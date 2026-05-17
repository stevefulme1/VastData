# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data tenant encryption."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_tenant_encryption
short_description: Manage VAST Data tenant encryption
description:
    - Create, update, and delete tenant encryption configuration on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    tenant_id:
        description:
            - The ID of the tenant.
        type: int
        required: true
    encryption_group_id:
        description:
            - The ID of the encryption group.
        type: int
        required: true
    enabled:
        description:
            - Whether encryption is enabled for this tenant.
        type: bool
        default: true
    state:
        description:
            - The desired state of the tenant encryption.
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
- name: Enable encryption for a tenant
  stevefulme1.vastdata.vast_tenant_encryption:
    tenant_id: 1
    encryption_group_id: 10
    enabled: true
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Disable encryption for a tenant
  stevefulme1.vastdata.vast_tenant_encryption:
    tenant_id: 1
    encryption_group_id: 10
    enabled: false
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Remove tenant encryption configuration
  stevefulme1.vastdata.vast_tenant_encryption:
    tenant_id: 1
    encryption_group_id: 10
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the tenant encryption.
    returned: on success
    type: dict
    sample:
        tenant_id: 1
        encryption_group_id: 10
        enabled: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastTenantEncryption(VastResourceBase):
    resource_path = "/api/tenantencryption/"

    def get_resource(self):
        """Look up tenant encryption by tenant_id."""
        tenant_id = self.module.params["tenant_id"]
        try:
            resources = self.client.get(self.resource_path)
            if isinstance(resources, list):
                for r in resources:
                    if r.get("tenant_id") == tenant_id:
                        return r
        except Exception:
            pass
        return None

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "tenant_id",
            "encryption_group_id",
            "enabled"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["encryption_group_id", "enabled"]


def main():
    module_args = dict(
        tenant_id=dict(type="int", required=True),
        encryption_group_id=dict(type="int", required=True),
        enabled=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastTenantEncryption(module).run()


if __name__ == "__main__":
    main()
