# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Dynamic inventory plugin for VAST Data VMs and tenants."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
name: vast_inventory
short_description: Dynamic inventory for VAST Data VMs and tenants
description:
    - Queries the VAST Data VMS API for virtual machines and tenants.
    - Groups hosts by tenant name and VM state.
    - Populates host variables including vm_id, tenant, state, and
      ip_addresses.
    - Uses the vastpy Python SDK for API communication.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    plugin:
        description:
            - Token that ensures this is a source file for the plugin.
        required: true
        choices: [stevefulme1.vastdata.vast_inventory]
    api_host:
        description:
            - Hostname or IP address of the VAST VMS API.
        required: true
        type: str
    api_user:
        description:
            - Username for VMS API authentication.
        type: str
    api_password:
        description:
            - Password for VMS API authentication.
        type: str
    api_token:
        description:
            - API token for VMS API authentication.
        type: str
    validate_certs:
        description:
            - Whether to validate SSL certificates.
        type: bool
        default: true
"""

EXAMPLES = r"""
# vast_inventory.yml
plugin: stevefulme1.vastdata.vast_inventory
api_host: vast-cluster-01.example.com
api_user: admin
api_password: "{{ vault_vms_password }}"
validate_certs: true
"""

try:
    from vastpy import VASTClient
    HAS_VASTPY = True
except ImportError:
    HAS_VASTPY = False

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin


class InventoryModule(BaseInventoryPlugin):
    NAME = "stevefulme1.vastdata.vast_inventory"

    def verify_file(self, path):
        """Validate the inventory source file."""
        valid = False
        if super().verify_file(path):
            if path.endswith((".yml", ".yaml")):
                valid = True
        return valid

    def _get_client(self, config):
        """Create an authenticated VASTClient from inventory config."""
        if not HAS_VASTPY:
            raise AnsibleError(
                "The 'vastpy' Python SDK is required. Install with: pip install vastpy"
            )

        host = config.get("api_host")
        if not host:
            raise AnsibleError("'api_host' is required in the inventory configuration.")

        api_token = config.get("api_token")
        username = config.get("api_user")
        password = config.get("api_password")
        verify_ssl = config.get("validate_certs", True)

        try:
            if api_token:
                return VASTClient(
                    host=host,
                    api_token=api_token,
                    verify_ssl=verify_ssl,
                )
            elif username and password:
                return VASTClient(
                    host=host,
                    username=username,
                    password=password,
                    verify_ssl=verify_ssl,
                )
            else:
                raise AnsibleError(
                    "Either 'api_token' or both 'api_user' and 'api_password' "
                    "are required in the inventory configuration."
                )
        except AnsibleError:
            raise
        except Exception as e:
            raise AnsibleError("Failed to connect to VAST VMS at {0}: {1}".format(host, e))

    def parse(self, inventory, loader, path, cache=True):
        """Parse the inventory source and populate inventory."""
        super().parse(inventory, loader, path, cache)
        self._read_config_data(path)

        config = {
            "api_host": self.get_option("api_host"),
            "api_user": self.get_option("api_user"),
            "api_password": self.get_option("api_password"),
            "api_token": self.get_option("api_token"),
            "validate_certs": self.get_option("validate_certs"),
        }

        client = self._get_client(config)

        # Fetch tenants and build a lookup by ID
        try:
            tenants_raw = client.get("/api/tenants/")
            if not isinstance(tenants_raw, list):
                tenants_raw = [tenants_raw] if tenants_raw else []
        except Exception as e:
            raise AnsibleError("Failed to query tenants: {0}".format(e))

        tenant_map = {}
        for t in tenants_raw:
            tid = t.get("id")
            tname = t.get("name", "tenant_{0}".format(tid))
            tenant_map[tid] = tname

        # Fetch VMs
        try:
            vms = client.get("/api/vms/")
            if not isinstance(vms, list):
                vms = [vms] if vms else []
        except Exception as e:
            raise AnsibleError("Failed to query VMs: {0}".format(e))

        for vm in vms:
            vm_name = vm.get("name")
            if not vm_name:
                continue

            self.inventory.add_host(vm_name)

            # Set host variables
            vm_id = vm.get("id")
            state = vm.get("state", "unknown")
            tenant_id = vm.get("tenant_id")
            tenant_name = tenant_map.get(tenant_id, "tenant_{0}".format(tenant_id))
            ip_addresses = vm.get("ip_addresses", [])

            self.inventory.set_variable(vm_name, "vm_id", vm_id)
            self.inventory.set_variable(vm_name, "tenant", tenant_name)
            self.inventory.set_variable(vm_name, "state", state)
            self.inventory.set_variable(vm_name, "ip_addresses", ip_addresses)

            # Group by tenant
            tenant_group = self._sanitize_group_name("tenant_{0}".format(tenant_name))
            self.inventory.add_group(tenant_group)
            self.inventory.add_child(tenant_group, vm_name)

            # Group by state
            state_group = self._sanitize_group_name("state_{0}".format(state))
            self.inventory.add_group(state_group)
            self.inventory.add_child(state_group, vm_name)

    @staticmethod
    def _sanitize_group_name(name):
        """Sanitize a string for use as an Ansible group name."""
        return name.lower().replace(" ", "_").replace("-", "_")
