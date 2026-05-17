# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Global-Local Snapshots."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_global_local_snapshot
short_description: Manage VAST Data global-local snapshot mappings
description:
    - Create, update, and delete global-local snapshot mappings on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the global-local snapshot mapping.
        type: str
        required: true
    global_snapshot_id:
        description:
            - ID of the global snapshot.
        type: int
        required: true
    local_snapshot_id:
        description:
            - ID of the local snapshot.
        type: int
        required: true
    remote_target_id:
        description:
            - ID of the remote target.
        type: int
    state:
        description:
            - The desired state of the global-local snapshot mapping.
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
- name: Create a global-local snapshot mapping
  stevefulme1.vastdata.vast_global_local_snapshot:
    name: mapping_prod_to_dr
    global_snapshot_id: 789
    local_snapshot_id: 123
    remote_target_id: 456
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Update global-local snapshot mapping
  stevefulme1.vastdata.vast_global_local_snapshot:
    name: mapping_prod_to_dr
    global_snapshot_id: 789
    local_snapshot_id: 123
    remote_target_id: 789
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete a global-local snapshot mapping
  stevefulme1.vastdata.vast_global_local_snapshot:
    name: mapping_prod_to_dr
    global_snapshot_id: 789
    local_snapshot_id: 123
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the global-local snapshot mapping.
    returned: on success
    type: dict
    sample: {
        "id": 321,
        "name": "mapping_prod_to_dr",
        "global_snapshot_id": 789,
        "local_snapshot_id": 123,
        "remote_target_id": 456
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastGlobalLocalSnapshot(VastResourceBase):
    resource_path = "/api/globallocalsnapshots/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "global_snapshot_id",
            "local_snapshot_id",
            "remote_target_id"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["remote_target_id"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        global_snapshot_id=dict(type="int", required=True),
        local_snapshot_id=dict(type="int", required=True),
        remote_target_id=dict(type="int"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastGlobalLocalSnapshot(module).run()


if __name__ == "__main__":
    main()
