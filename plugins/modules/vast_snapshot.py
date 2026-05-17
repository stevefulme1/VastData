# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Snapshots."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_snapshot
short_description: Manage VAST Data snapshots
description:
    - Create, update, and delete snapshots on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the snapshot.
        type: str
        required: true
    path:
        description:
            - Path to snapshot.
        type: str
        required: true
    tenant_id:
        description:
            - Tenant ID for the snapshot.
        type: int
    expiration_time:
        description:
            - Expiration time for the snapshot.
        type: str
    indestructible:
        description:
            - Whether the snapshot is indestructible.
        type: bool
        default: false
    state:
        description:
            - The desired state of the snapshot.
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
- name: Create a snapshot
  stevefulme1.vastdata.vast_snapshot:
    name: daily_snapshot_2025_01_15
    path: /data/production
    tenant_id: 1
    expiration_time: "2025-02-15T00:00:00Z"
    indestructible: false
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Update snapshot expiration
  stevefulme1.vastdata.vast_snapshot:
    name: daily_snapshot_2025_01_15
    path: /data/production
    expiration_time: "2025-03-15T00:00:00Z"
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete a snapshot
  stevefulme1.vastdata.vast_snapshot:
    name: daily_snapshot_2025_01_15
    path: /data/production
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the snapshot.
    returned: on success
    type: dict
    sample: {
        "id": 123,
        "name": "daily_snapshot_2025_01_15",
        "path": "/data/production",
        "tenant_id": 1,
        "expiration_time": "2025-02-15T00:00:00Z",
        "indestructible": false
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastSnapshot(VastResourceBase):
    resource_path = "/api/snapshots/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "path",
            "tenant_id",
            "expiration_time",
            "indestructible"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["expiration_time", "indestructible"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        path=dict(type="str", required=True),
        tenant_id=dict(type="int"),
        expiration_time=dict(type="str"),
        indestructible=dict(type="bool", default=False),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastSnapshot(module).run()


if __name__ == "__main__":
    main()
