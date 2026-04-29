# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data S3 Replication Peers."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_s3_replication_peer
short_description: Manage VAST Data S3 replication peers
description:
    - Create, update, and delete S3 replication peers on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the S3 replication peer.
        type: str
        required: true
    bucket_name:
        description:
            - Name of the S3 bucket.
        type: str
        required: true
    url:
        description:
            - S3 endpoint URL.
        type: str
        required: true
    access_key:
        description:
            - S3 access key ID.
        type: str
        required: true
    secret_key:
        description:
            - S3 secret access key.
        type: str
        required: true
        no_log: true
    region:
        description:
            - AWS region for the S3 bucket.
        type: str
    proxy_url:
        description:
            - Proxy URL for S3 access.
        type: str
    aws_iam_role:
        description:
            - AWS IAM role ARN for S3 access.
        type: str
    state:
        description:
            - The desired state of the S3 replication peer.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create an S3 replication peer
  vastdata.cluster.vast_s3_replication_peer:
    name: s3_backup_peer
    bucket_name: vast-backups
    url: https://s3.us-east-1.amazonaws.com
    access_key: AKIAIOSFODNN7EXAMPLE
    secret_key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    region: us-east-1
    state: present

- name: Update S3 replication peer credentials
  vastdata.cluster.vast_s3_replication_peer:
    name: s3_backup_peer
    bucket_name: vast-backups
    url: https://s3.us-east-1.amazonaws.com
    access_key: AKIAIOSFODNN7NEWKEY
    secret_key: newSecretKeyExample123456789
    region: us-east-1
    state: present

- name: Delete an S3 replication peer
  vastdata.cluster.vast_s3_replication_peer:
    name: s3_backup_peer
    bucket_name: vast-backups
    url: https://s3.us-east-1.amazonaws.com
    access_key: AKIAIOSFODNN7EXAMPLE
    secret_key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the S3 replication peer.
    returned: on success
    type: dict
    sample: {
        "id": 200,
        "name": "s3_backup_peer",
        "bucket_name": "vast-backups",
        "url": "https://s3.us-east-1.amazonaws.com",
        "region": "us-east-1"
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase

class VastS3ReplicationPeer(VastResourceBase):
    resource_path = "/api/s3replicationpeers/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in ["name", "bucket_name", "url", "access_key", "secret_key", "region", "proxy_url", "aws_iam_role"] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["bucket_name", "url", "access_key", "secret_key", "region", "proxy_url", "aws_iam_role"]

def main():
    module_args = dict(
        name=dict(type="str", required=True),
        bucket_name=dict(type="str", required=True),
        url=dict(type="str", required=True),
        access_key=dict(type="str", required=True),
        secret_key=dict(type="str", required=True, no_log=True),
        region=dict(type="str"),
        proxy_url=dict(type="str"),
        aws_iam_role=dict(type="str"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastS3ReplicationPeer(module).run()

if __name__ == "__main__":
    main()
