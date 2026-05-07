# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Kafka broker integration."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_kafka_broker
short_description: Manage VAST Data Kafka broker integration
description:
    - Create, update, and delete Kafka broker integration on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the Kafka broker configuration.
        type: str
        required: true
    brokers:
        description:
            - List of Kafka broker addresses.
        type: list
        elements: str
        required: true
    topic:
        description:
            - The Kafka topic name.
        type: str
        required: true
    security_protocol:
        description:
            - The security protocol for Kafka connection.
        type: str
        choices: [PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL]
        default: PLAINTEXT
    sasl_mechanism:
        description:
            - The SASL mechanism for authentication.
        type: str
        choices: [PLAIN, SCRAM-SHA-256, SCRAM-SHA-512]
    sasl_username:
        description:
            - The SASL username for authentication.
        type: str
    sasl_password:
        description:
            - The SASL password for authentication.
        type: str
    ssl_ca_cert:
        description:
            - The SSL CA certificate for secure connections.
        type: str
    enabled:
        description:
            - Whether the Kafka broker integration is enabled.
        type: bool
        default: true
    state:
        description:
            - The desired state of the Kafka broker configuration.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create Kafka broker with PLAINTEXT security
  stevefulme1.vastdata.vast_kafka_broker:
    name: kafka_prod
    brokers:
      - kafka1.example.com:9092
      - kafka2.example.com:9092
    topic: vast_events
    security_protocol: PLAINTEXT
    enabled: true
    state: present

- name: Create Kafka broker with SASL authentication
  stevefulme1.vastdata.vast_kafka_broker:
    name: kafka_secure
    brokers:
      - kafka1.example.com:9093
      - kafka2.example.com:9093
    topic: vast_events
    security_protocol: SASL_SSL
    sasl_mechanism: SCRAM-SHA-256
    sasl_username: vast_user
    sasl_password: "{{ vault_repl_password }}"
    ssl_ca_cert: "{{ lookup('file', '/path/to/ca.crt') }}"
    enabled: true
    state: present

- name: Delete Kafka broker configuration
  stevefulme1.vastdata.vast_kafka_broker:
    name: kafka_prod
    brokers:
      - kafka1.example.com:9092
    topic: vast_events
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the Kafka broker configuration.
    returned: on success
    type: dict
    sample:
        id: 1
        name: kafka_prod
        brokers:
          - kafka1.example.com:9092
          - kafka2.example.com:9092
        topic: vast_events
        security_protocol: PLAINTEXT
        enabled: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastKafkaBroker(VastResourceBase):
    resource_path = "/api/kafkabrokers/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "brokers",
            "topic",
            "security_protocol",
            "sasl_mechanism",
            "sasl_username",
            "sasl_password",
            "ssl_ca_cert",
            "enabled"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return [
            "brokers",
            "topic",
            "security_protocol",
            "sasl_mechanism",
            "sasl_username",
            "sasl_password",
            "ssl_ca_cert",
            "enabled"
        ]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        brokers=dict(type="list", elements="str", required=True),
        topic=dict(type="str", required=True),
        security_protocol=dict(
            type="str",
            choices=["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"],
            default="PLAINTEXT",
        ),
        sasl_mechanism=dict(type="str", choices=["PLAIN", "SCRAM-SHA-256", "SCRAM-SHA-512"]),
        sasl_username=dict(type="str"),
        sasl_password=dict(type="str", no_log=True),
        ssl_ca_cert=dict(type="str"),
        enabled=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastKafkaBroker(module).run()


if __name__ == "__main__":
    main()
