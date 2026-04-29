# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Global Snapshots."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_global_snapshot
short_description: Manage VAST Data global snapshots
description:
    - Create, update, and delete global (cross-cluster) snapshots on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the global snapshot.
        type: str
        required: true
    source_snapshot_id:
        description:
            - ID of the source snapshot.
        type: int
    remote_target_id:
        description:
            - ID of the remote target.
        type: int
    loanee_root_export:
        description:
            - Loanee root export path.
        type: str
    loanee_snapshot_name:
        description:
            - Name of the loanee snapshot.
        type: str
    enabled:
        description:
            - Whether the global snapshot is enabled.
        type: bool
        default: true
    state:
        description:
            - The desired state of the global snapshot.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create a global snapshot
  vastdata.cluster.vast_global_snapshot:
    name: global_snapshot_prod
    source_snapshot_id: 123
    remote_target_id: 456
    loanee_root_export: /exports/replicated
    enabled: true
    state: present

- name: Update global snapshot configuration
  vastdata.cluster.vast_global_snapshot:
    name: global_snapshot_prod
    loanee_snapshot_name: prod_snapshot_remote
    enabled: true
    state: present

- name: Delete a global snapshot
  vastdata.cluster.vast_global_snapshot:
    name: global_snapshot_prod
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the global snapshot.
    returned: on success
    type: dict
    sample: {
        "id": 789,
        "name": "global_snapshot_prod",
        "source_snapshot_id": 123,
        "remote_target_id": 456,
        "loanee_root_export": "/exports/replicated",
        "enabled": true
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastGlobalSnapshot(VastResourceBase):
    resource_path = "/api/globalsnapshots/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "source_snapshot_id",
            "remote_target_id",
            "loanee_root_export",
            "loanee_snapshot_name",
            "enabled"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["loanee_root_export", "loanee_snapshot_name", "enabled"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        source_snapshot_id=dict(type="int"),
        remote_target_id=dict(type="int"),
        loanee_root_export=dict(type="str"),
        loanee_snapshot_name=dict(type="str"),
        enabled=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastGlobalSnapshot(module).run()


if __name__ == "__main__":
    main()
