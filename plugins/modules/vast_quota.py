# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Quotas."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_quota
short_description: Manage VAST Data storage quotas
description:
    - Create, update, and delete storage quotas on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the quota.
        type: str
        required: true
    path:
        description:
            - The filesystem path for the quota.
        type: str
        required: true
    tenant_id:
        description:
            - ID of the tenant this quota belongs to.
        type: int
    soft_limit:
        description:
            - Soft limit for storage in bytes.
        type: int
    hard_limit:
        description:
            - Hard limit for storage in bytes.
        type: int
    grace_period:
        description:
            - Grace period for soft limit enforcement.
        type: str
    soft_limit_inodes:
        description:
            - Soft limit for number of inodes.
        type: int
    hard_limit_inodes:
        description:
            - Hard limit for number of inodes.
        type: int
    enable_alarms:
        description:
            - Enable alarms when quota thresholds are reached.
        type: bool
        default: true
    entity:
        description:
            - Entity to which the quota applies.
        type: dict
        suboptions:
            name:
                description:
                    - Entity name.
                type: str
            identifier_type:
                description:
                    - Type of identifier.
                type: str
            identifier:
                description:
                    - Entity identifier.
                type: str
    state:
        description:
            - The desired state of the quota.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create a storage quota
  stevefulme1.vastdata.vast_quota:
    name: team_quota
    path: /data/teams/engineering
    soft_limit: 5497558138880
    hard_limit: 10995116277760
    grace_period: 7d
    enable_alarms: true
    entity:
      name: engineering
      identifier_type: gid
      identifier: "1001"
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Update quota limits
  stevefulme1.vastdata.vast_quota:
    name: team_quota
    path: /data/teams/engineering
    soft_limit: 10995116277760
    hard_limit: 21990232555520
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete a quota
  stevefulme1.vastdata.vast_quota:
    name: team_quota
    path: /data/teams/engineering
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the quota.
    returned: on success
    type: dict
    sample:
        id: 1
        name: team_quota
        path: /data/teams/engineering
        soft_limit: 5497558138880
        hard_limit: 10995116277760
        grace_period: 7d
        enable_alarms: true
        entity:
            name: engineering
            identifier_type: gid
            identifier: "1001"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastQuota(VastResourceBase):
    resource_path = "/api/quotas/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "path",
            "tenant_id",
            "soft_limit",
            "hard_limit",
            "grace_period",
            "soft_limit_inodes",
            "hard_limit_inodes",
            "enable_alarms",
            "entity"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return [
            "soft_limit",
            "hard_limit",
            "grace_period",
            "soft_limit_inodes",
            "hard_limit_inodes",
            "enable_alarms",
            "entity"
        ]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        path=dict(type="str", required=True),
        tenant_id=dict(type="int"),
        soft_limit=dict(type="int"),
        hard_limit=dict(type="int"),
        grace_period=dict(type="str"),
        soft_limit_inodes=dict(type="int"),
        hard_limit_inodes=dict(type="int"),
        enable_alarms=dict(type="bool", default=True),
        entity=dict(type="dict"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastQuota(module).run()


if __name__ == "__main__":
    main()
