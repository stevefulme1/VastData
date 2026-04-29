# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data S3 Lifecycle Rules."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_s3_lifecycle_rule
short_description: Manage VAST Data S3 lifecycle rules
description:
    - Create, update, and delete S3 lifecycle rules on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the lifecycle rule.
        type: str
        required: true
    view_id:
        description:
            - ID of the view this lifecycle rule applies to.
        type: int
        required: true
    prefix:
        description:
            - Object key prefix to which this rule applies.
        type: str
    enabled:
        description:
            - Whether the lifecycle rule is enabled.
        type: bool
        default: true
    expiration_days:
        description:
            - Number of days after which objects expire.
        type: int
    noncurrent_version_expiration_days:
        description:
            - Number of days after which noncurrent versions expire.
        type: int
    abort_incomplete_multipart_upload_days:
        description:
            - Number of days after which incomplete multipart uploads are aborted.
        type: int
    state:
        description:
            - The desired state of the lifecycle rule.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create an S3 lifecycle rule
  vastdata.cluster.vast_s3_lifecycle_rule:
    name: expire_old_logs
    view_id: 1
    prefix: logs/
    enabled: true
    expiration_days: 90
    abort_incomplete_multipart_upload_days: 7
    state: present

- name: Update lifecycle rule to expire noncurrent versions
  vastdata.cluster.vast_s3_lifecycle_rule:
    name: expire_old_logs
    view_id: 1
    noncurrent_version_expiration_days: 30
    state: present

- name: Delete a lifecycle rule
  vastdata.cluster.vast_s3_lifecycle_rule:
    name: expire_old_logs
    view_id: 1
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the S3 lifecycle rule.
    returned: on success
    type: dict
    sample:
        id: 1
        name: expire_old_logs
        view_id: 1
        prefix: logs/
        enabled: true
        expiration_days: 90
        noncurrent_version_expiration_days: 30
        abort_incomplete_multipart_upload_days: 7
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastS3LifecycleRule(VastResourceBase):
    resource_path = "/api/s3lifecyclerules/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "view_id",
            "prefix",
            "enabled",
            "expiration_days",
            "noncurrent_version_expiration_days",
            "abort_incomplete_multipart_upload_days"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return [
            "prefix",
            "enabled",
            "expiration_days",
            "noncurrent_version_expiration_days",
            "abort_incomplete_multipart_upload_days"
        ]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        view_id=dict(type="int", required=True),
        prefix=dict(type="str"),
        enabled=dict(type="bool", default=True),
        expiration_days=dict(type="int"),
        noncurrent_version_expiration_days=dict(type="int"),
        abort_incomplete_multipart_upload_days=dict(type="int"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastS3LifecycleRule(module).run()


if __name__ == "__main__":
    main()
