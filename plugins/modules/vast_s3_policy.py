# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data S3 Policies."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_s3_policy
short_description: Manage VAST Data S3 bucket policies
description:
    - Create, update, and delete S3 bucket policies on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the S3 policy.
        type: str
        required: true
    policy:
        description:
            - The S3 policy document in JSON format.
        type: dict
        required: true
        suboptions:
            Version:
                description:
                    - Policy version.
                type: str
                required: true
            Statement:
                description:
                    - List of policy statements.
                type: list
                elements: dict
                required: true
    tenant_id:
        description:
            - ID of the tenant this policy belongs to.
        type: int
    state:
        description:
            - The desired state of the S3 policy.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create an S3 bucket policy
  stevefulme1.vastdata.vast_s3_policy:
    name: public_read_policy
    policy:
      Version: "2012-10-17"
      Statement:
        - Effect: Allow
          Principal: "*"
          Action:
            - s3:GetObject
          Resource:
            - arn:aws:s3:::mybucket/*
    tenant_id: 1
    state: present

- name: Update S3 policy to restrict access
  stevefulme1.vastdata.vast_s3_policy:
    name: public_read_policy
    policy:
      Version: "2012-10-17"
      Statement:
        - Effect: Deny
          Principal: "*"
          Action:
            - s3:DeleteObject
          Resource:
            - arn:aws:s3:::mybucket/*
    state: present

- name: Delete an S3 policy
  stevefulme1.vastdata.vast_s3_policy:
    name: public_read_policy
    policy:
      Version: "2012-10-17"
      Statement: []
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the S3 policy.
    returned: on success
    type: dict
    sample:
        id: 1
        name: public_read_policy
        policy:
            Version: "2012-10-17"
            Statement:
                - Effect: Allow
                  Principal: "*"
                  Action: [s3:GetObject]
                  Resource: [arn:aws:s3:::mybucket/*]
        tenant_id: 1
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastS3Policy(VastResourceBase):
    resource_path = "/api/s3policies/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "policy",
            "tenant_id"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["policy"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        policy=dict(type="dict", required=True),
        tenant_id=dict(type="int"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastS3Policy(module).run()


if __name__ == "__main__":
    main()
