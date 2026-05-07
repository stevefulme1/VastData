# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data tenant client metrics."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_tenant_client_metrics
short_description: Manage VAST Data tenant client metrics
description:
    - Create, update, and delete tenant client metrics configuration on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    tenant_id:
        description:
            - The ID of the tenant.
        type: int
        required: true
    enabled:
        description:
            - Whether client metrics are enabled for this tenant.
        type: bool
        required: true
    protocols:
        description:
            - List of protocols to collect metrics for.
        type: list
        elements: str
        choices: [NFS, SMB, S3]
    state:
        description:
            - The desired state of the tenant client metrics.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Enable client metrics for a tenant
  stevefulme1.vastdata.vast_tenant_client_metrics:
    tenant_id: 1
    enabled: true
    protocols:
      - NFS
      - SMB
      - S3
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Update protocols for client metrics
  stevefulme1.vastdata.vast_tenant_client_metrics:
    tenant_id: 1
    enabled: true
    protocols:
      - NFS
      - SMB
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Disable client metrics for a tenant
  stevefulme1.vastdata.vast_tenant_client_metrics:
    tenant_id: 1
    enabled: false
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the tenant client metrics.
    returned: on success
    type: dict
    sample:
        tenant_id: 1
        enabled: true
        protocols:
          - NFS
          - SMB
          - S3
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastTenantClientMetrics(VastResourceBase):
    resource_path = "/api/tenantclientmetrics/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "tenant_id",
            "enabled",
            "protocols"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["enabled", "protocols"]


def main():
    module_args = dict(
        tenant_id=dict(type="int", required=True),
        enabled=dict(type="bool", required=True),
        protocols=dict(type="list", elements="str", choices=["NFS", "SMB", "S3"]),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastTenantClientMetrics(module).run()


if __name__ == "__main__":
    main()
