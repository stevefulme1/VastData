# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data local users."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_user
short_description: Manage VAST Data local users
description:
    - Create, update, and delete local users on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the local user.
        type: str
        required: true
    uid:
        description:
            - User ID for the local user.
        type: int
        required: false
    password:
        description:
            - Password for the local user.
        type: str
        required: false
    allow_create_bucket:
        description:
            - Allow user to create S3 buckets.
        type: bool
        required: false
    allow_delete_bucket:
        description:
            - Allow user to delete S3 buckets.
        type: bool
        required: false
    s3_superuser:
        description:
            - Grant S3 superuser privileges to the user.
        type: bool
        required: false
    state:
        description:
            - The desired state of the local user.
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
- name: Create a local user
  stevefulme1.vastdata.vast_user:
    vms_host: "vms.example.com"
    vms_user: "admin"
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true
    name: "john_doe"
    uid: 5001
    password: "{{ vault_user_password }}"
    allow_create_bucket: true
    allow_delete_bucket: false
    s3_superuser: false
    state: present

- name: Update a local user
  stevefulme1.vastdata.vast_user:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "john_doe"
    allow_create_bucket: false
    s3_superuser: true
    state: present

- name: Delete a local user
  stevefulme1.vastdata.vast_user:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "john_doe"
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the local user.
    returned: on success
    type: dict
    sample:
        id: 1
        name: "john_doe"
        uid: 5001
        allow_create_bucket: true
        allow_delete_bucket: false
        s3_superuser: false
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastUser(VastResourceBase):
    resource_path = "/api/users/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "uid",
            "password",
            "allow_create_bucket",
            "allow_delete_bucket",
            "s3_superuser"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["password", "allow_create_bucket", "allow_delete_bucket", "s3_superuser"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        uid=dict(type="int", required=False),
        password=dict(type="str", required=False, no_log=True),
        allow_create_bucket=dict(type="bool", required=False),
        allow_delete_bucket=dict(type="bool", required=False),
        s3_superuser=dict(type="bool", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastUser(module).run()


if __name__ == "__main__":
    main()
