# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data NFS exports."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_nfs_export
short_description: Manage VAST Data NFS export rules
description:
    - Create, update, and delete NFS export rules on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the NFS export.
        type: str
        required: true
    path:
        description:
            - Filesystem path to export.
        type: str
    export_policy:
        description:
            - Name or ID of the export policy to associate.
        type: str
    protocols:
        description:
            - List of NFS protocol versions to enable.
        type: list
        elements: str
    access_type:
        description:
            - Access type for the export (e.g. RW, RO).
        type: str
    squash:
        description:
            - Squash setting for the export (e.g. NO_SQUASH, ROOT_SQUASH).
        type: str
    anon_uid:
        description:
            - Anonymous UID for squashed access.
        type: int
    anon_gid:
        description:
            - Anonymous GID for squashed access.
        type: int
    state:
        description:
            - The desired state of the NFS export.
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
- name: Create an NFS export
  stevefulme1.vastdata.vast_nfs_export:
    name: prod_data_export
    path: /data/production
    access_type: RW
    squash: ROOT_SQUASH
    anon_uid: 65534
    anon_gid: 65534
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Update NFS export access type
  stevefulme1.vastdata.vast_nfs_export:
    name: prod_data_export
    path: /data/production
    access_type: RO
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete an NFS export
  stevefulme1.vastdata.vast_nfs_export:
    name: prod_data_export
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the NFS export.
    returned: on success
    type: dict
    sample: {
        "id": 42,
        "name": "prod_data_export",
        "path": "/data/production",
        "access_type": "RW",
        "squash": "ROOT_SQUASH",
        "anon_uid": 65534,
        "anon_gid": 65534
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastNfsExport(VastResourceBase):
    resource_path = "/api/nfsexports/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "path",
            "export_policy",
            "protocols",
            "access_type",
            "squash",
            "anon_uid",
            "anon_gid",
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["path", "export_policy", "protocols", "access_type", "squash", "anon_uid", "anon_gid"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        path=dict(type="str"),
        export_policy=dict(type="str"),
        protocols=dict(type="list", elements="str"),
        access_type=dict(type="str"),
        squash=dict(type="str"),
        anon_uid=dict(type="int"),
        anon_gid=dict(type="int"),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastNfsExport(module).run()


if __name__ == "__main__":
    main()
