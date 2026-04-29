# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data SAML single sign-on configuration."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_saml_config
short_description: Manage VAST Data SAML single sign-on
description:
    - Create, update, and delete SAML single sign-on configuration on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the SAML configuration.
        type: str
        required: true
    idp_entity_id:
        description:
            - Identity Provider entity ID.
        type: str
        required: true
    idp_sso_url:
        description:
            - Identity Provider single sign-on URL.
        type: str
        required: true
    idp_certificate:
        description:
            - Identity Provider certificate for signature verification.
        type: str
        required: true
    sp_entity_id:
        description:
            - Service Provider entity ID.
        type: str
    sign_requests:
        description:
            - Whether to sign SAML requests.
        type: bool
        default: true
    enabled:
        description:
            - Whether SAML authentication is enabled.
        type: bool
        default: true
    state:
        description:
            - The desired state of the SAML configuration.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create SAML configuration
  vastdata.cluster.vast_saml_config:
    name: okta_saml
    idp_entity_id: http://www.okta.com/exk1234567890
    idp_sso_url: https://example.okta.com/app/vast/exk1234567890/sso/saml
    idp_certificate: |
      -----BEGIN CERTIFICATE-----
      MIIDpDCCAoygAwIBAgIGAXabcdefMA0GCSqGSIb3DQEBCwUAMIGSMQswCQYDVQQG
      ...
      -----END CERTIFICATE-----
    sp_entity_id: https://vast.example.com/saml
    sign_requests: true
    enabled: true
    state: present
    vast_host: vast.example.com
    vast_username: admin
    vms_password: "{{ vault_vms_password }}"

- name: Update SAML configuration
  vastdata.cluster.vast_saml_config:
    name: okta_saml
    idp_entity_id: http://www.okta.com/exk1234567890
    idp_sso_url: https://example.okta.com/app/vast/exk1234567890/sso/saml
    idp_certificate: |
      -----BEGIN CERTIFICATE-----
      MIIDpDCCAoygAwIBAgIGAXabcdefMA0GCSqGSIb3DQEBCwUAMIGSMQswCQYDVQQG
      ...
      -----END CERTIFICATE-----
    sign_requests: false
    enabled: true
    state: present
    vast_host: vast.example.com
    vast_username: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete SAML configuration
  vastdata.cluster.vast_saml_config:
    name: okta_saml
    state: absent
    vast_host: vast.example.com
    vast_username: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the SAML configuration.
    returned: on success
    type: dict
    sample:
        id: 1
        name: okta_saml
        idp_entity_id: http://www.okta.com/exk1234567890
        idp_sso_url: https://example.okta.com/app/vast/exk1234567890/sso/saml
        sp_entity_id: https://vast.example.com/saml
        sign_requests: true
        enabled: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastSamlConfig(VastResourceBase):
    resource_path = "/api/saml/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "idp_entity_id",
            "idp_sso_url",
            "idp_certificate",
            "sp_entity_id",
            "sign_requests",
            "enabled"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["idp_entity_id", "idp_sso_url", "idp_certificate", "sp_entity_id", "sign_requests", "enabled"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        idp_entity_id=dict(type="str", required=True),
        idp_sso_url=dict(type="str", required=True),
        idp_certificate=dict(type="str", required=True),
        sp_entity_id=dict(type="str"),
        sign_requests=dict(type="bool", default=True),
        enabled=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastSamlConfig(module).run()


if __name__ == "__main__":
    main()
