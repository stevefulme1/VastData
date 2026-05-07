# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Views."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_view
short_description: Manage VAST Data views
description:
    - Create, update, and delete views on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the view.
        type: str
        required: true
    path:
        description:
            - The filesystem path for the view.
        type: str
        required: true
    protocols:
        description:
            - List of protocols enabled for this view.
        type: list
        elements: str
        choices: [NFS, SMB, S3]
    policy_id:
        description:
            - ID of the view policy to apply.
        type: int
    tenant_id:
        description:
            - ID of the tenant this view belongs to.
        type: int
    alias:
        description:
            - Alias name for the view.
        type: str
    bucket:
        description:
            - S3 bucket name.
        type: str
    share:
        description:
            - SMB share name.
        type: str
    nfs_interop_flags:
        description:
            - NFS interoperability flags.
        type: str
    s3_versioning:
        description:
            - Enable S3 versioning for the view.
        type: bool
    create_dir:
        description:
            - Automatically create the directory if it doesn't exist.
        type: bool
        default: true
    state:
        description:
            - The desired state of the view.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create a multi-protocol view
  stevefulme1.vastdata.vast_view:
    name: shared_data
    path: /data/shared
    protocols:
      - NFS
      - SMB
      - S3
    policy_id: 1
    bucket: shared-bucket
    share: shared
    create_dir: true
    state: present

- name: Update view to enable S3 versioning
  stevefulme1.vastdata.vast_view:
    name: shared_data
    path: /data/shared
    s3_versioning: true
    state: present

- name: Delete a view
  stevefulme1.vastdata.vast_view:
    name: shared_data
    path: /data/shared
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the view.
    returned: on success
    type: dict
    sample:
        id: 1
        name: shared_data
        path: /data/shared
        protocols: [NFS, SMB, S3]
        policy_id: 1
        bucket: shared-bucket
        share: shared
        s3_versioning: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastView(VastResourceBase):
    resource_path = "/api/views/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "path",
            "protocols",
            "policy_id",
            "tenant_id",
            "alias",
            "bucket",
            "share",
            "nfs_interop_flags",
            "s3_versioning",
            "create_dir"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["protocols", "policy_id", "alias", "bucket", "share", "nfs_interop_flags", "s3_versioning"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        path=dict(type="str", required=True),
        protocols=dict(type="list", elements="str", choices=["NFS", "SMB", "S3"]),
        policy_id=dict(type="int"),
        tenant_id=dict(type="int"),
        alias=dict(type="str"),
        bucket=dict(type="str"),
        share=dict(type="str"),
        nfs_interop_flags=dict(type="str"),
        s3_versioning=dict(type="bool"),
        create_dir=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastView(module).run()


if __name__ == "__main__":
    main()
