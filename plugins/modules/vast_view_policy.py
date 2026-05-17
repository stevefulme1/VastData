# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data View Policies."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_view_policy
short_description: Manage VAST Data view policies
description:
    - Create, update, and delete view policies on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the view policy.
        type: str
        required: true
    flavor:
        description:
            - The protocol flavor for this policy.
        type: str
        choices: [NFS_EXPORT, SMB_SHARE, S3_BUCKET, MIXED]
    nfs_read_write:
        description:
            - List of hosts/networks with read-write access for NFS.
        type: list
        elements: str
    nfs_read_only:
        description:
            - List of hosts/networks with read-only access for NFS.
        type: list
        elements: str
    nfs_root_squash:
        description:
            - Root squash setting for NFS exports.
        type: str
        choices: [root_squash, no_root_squash, all_squash]
    smb_is_ca:
        description:
            - Enable SMB Continuous Availability.
        type: bool
    auth_source:
        description:
            - Authentication source for the policy.
        type: str
        choices: [PROVIDERS, NONE]
    state:
        description:
            - The desired state of the view policy.
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
- name: Create an NFS export policy
  stevefulme1.vastdata.vast_view_policy:
    name: nfs_policy
    flavor: NFS_EXPORT
    nfs_read_write:
      - 10.0.0.0/8
      - 192.168.1.0/24
    nfs_root_squash: root_squash
    auth_source: PROVIDERS
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Update view policy to add read-only access
  stevefulme1.vastdata.vast_view_policy:
    name: nfs_policy
    nfs_read_only:
      - 172.16.0.0/12
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete a view policy
  stevefulme1.vastdata.vast_view_policy:
    name: nfs_policy
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the view policy.
    returned: on success
    type: dict
    sample:
        id: 1
        name: nfs_policy
        flavor: NFS_EXPORT
        nfs_read_write: [10.0.0.0/8, 192.168.1.0/24]
        nfs_read_only: [172.16.0.0/12]
        nfs_root_squash: root_squash
        auth_source: PROVIDERS
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastViewPolicy(VastResourceBase):
    resource_path = "/api/viewpolicies/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "flavor",
            "nfs_read_write",
            "nfs_read_only",
            "nfs_root_squash",
            "smb_is_ca",
            "auth_source"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["flavor", "nfs_read_write", "nfs_read_only", "nfs_root_squash", "smb_is_ca", "auth_source"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        flavor=dict(type="str", choices=["NFS_EXPORT", "SMB_SHARE", "S3_BUCKET", "MIXED"]),
        nfs_read_write=dict(type="list", elements="str"),
        nfs_read_only=dict(type="list", elements="str"),
        nfs_root_squash=dict(type="str", choices=["root_squash", "no_root_squash", "all_squash"]),
        smb_is_ca=dict(type="bool"),
        auth_source=dict(type="str", choices=["PROVIDERS", "NONE"]),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastViewPolicy(module).run()


if __name__ == "__main__":
    main()
