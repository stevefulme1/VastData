# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data local groups."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_group
short_description: Manage VAST Data local groups
description:
    - Create, update, and delete local groups on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the local group.
        type: str
        required: true
    gid:
        description:
            - Group ID for the local group.
        type: int
        required: false
    s3_superuser:
        description:
            - Grant S3 superuser privileges to the group.
        type: bool
        required: false
    state:
        description:
            - The desired state of the local group.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create a local group
  vastdata.cluster.vast_group:
    vms_host: "vms.example.com"
    vms_user: "admin"
    vms_password: "secret"
    name: "developers"
    gid: 6001
    s3_superuser: false
    state: present

- name: Update a local group
  vastdata.cluster.vast_group:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "developers"
    s3_superuser: true
    state: present

- name: Delete a local group
  vastdata.cluster.vast_group:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "developers"
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the local group.
    returned: on success
    type: dict
    sample:
        id: 1
        name: "developers"
        gid: 6001
        s3_superuser: false
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastGroup(VastResourceBase):
    resource_path = "/api/groups/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "gid",
            "s3_superuser"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["s3_superuser"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        gid=dict(type="int", required=False),
        s3_superuser=dict(type="bool", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastGroup(module).run()


if __name__ == "__main__":
    main()
