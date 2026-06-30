"""Unit tests for stevefulme1.vastdata.vast_vip_pool module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch


CLIENT_PATH = "ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource"


def _base_args():
    return {
        "vms_host": "vms.example.com",
        "vms_port": 443,
        "vms_user": "admin",
        "vms_password": "secret",
        "api_token": None,
        "validate_certs": True,
        "wait": True,
        "wait_timeout": 600,
        "wait_interval": 10,
    }


class TestVastVipPoolCreate:
    """Test VIP pool creation."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_create_vip_pool(self, mock_get_client):
        """Creating a VIP pool calls POST /api/vippools/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 1,
            "name": "protocols-vip-pool",
            "subnet_cidr": 24,
            "role": "PROTOCOLS",
            "vlan": 100,
            "enabled": True,
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "protocols-vip-pool",
            "subnet_cidr": 24,
            "subnet_cidr_ipv6": None,
            "ip_ranges": [{"start_ip": "192.168.1.10", "end_ip": "192.168.1.20"}],
            "role": "PROTOCOLS",
            "domain_name": None,
            "vlan": 100,
            "tenant_id": None,
            "enabled": True,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_vip_pool import VastVipPool
        pool = VastVipPool(module)
        result = pool.create_resource()

        mock_client.post.assert_called_once()
        call_data = mock_client.post.call_args[1]["data"]
        assert call_data["name"] == "protocols-vip-pool"
        assert call_data["subnet_cidr"] == 24
        assert call_data["role"] == "PROTOCOLS"
        assert result["id"] == 1


class TestVastVipPoolDelete:
    """Test VIP pool deletion."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_delete_vip_pool(self, mock_get_client):
        """Deleting a VIP pool calls DELETE /api/vippools/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "protocols-vip-pool",
            "subnet_cidr": 24,
            "state": "absent",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_vip_pool import VastVipPool
        pool = VastVipPool(module)
        pool.delete_resource({"id": 5, "name": "protocols-vip-pool"})

        mock_client.delete.assert_called_once_with("/api/vippools/5/")


class TestVastVipPoolIdempotent:
    """Test idempotent behavior."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_no_change_needed(self, mock_get_client):
        """When VIP pool exists and matches, needs_update returns False."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "protocols-vip-pool",
            "subnet_cidr": None,
            "subnet_cidr_ipv6": None,
            "ip_ranges": None,
            "role": None,
            "domain_name": None,
            "vlan": None,
            "tenant_id": None,
            "enabled": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_vip_pool import VastVipPool
        pool = VastVipPool(module)

        existing = {
            "id": 1,
            "name": "protocols-vip-pool",
            "subnet_cidr": 24,
            "role": "PROTOCOLS",
            "vlan": 100,
            "enabled": True,
        }
        assert not pool.needs_update(existing)

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_update_needed(self, mock_get_client):
        """When vlan differs, needs_update returns True."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "protocols-vip-pool",
            "subnet_cidr": None,
            "subnet_cidr_ipv6": None,
            "ip_ranges": None,
            "role": None,
            "domain_name": None,
            "vlan": 200,
            "tenant_id": None,
            "enabled": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_vip_pool import VastVipPool
        pool = VastVipPool(module)

        existing = {
            "id": 1,
            "name": "protocols-vip-pool",
            "subnet_cidr": 24,
            "vlan": 100,
        }
        assert pool.needs_update(existing)

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_update_resource(self, mock_get_client):
        """Updating a VIP pool calls PATCH /api/vippools/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.patch.return_value = {
            "id": 1,
            "name": "protocols-vip-pool",
            "vlan": 200,
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "protocols-vip-pool",
            "subnet_cidr": None,
            "subnet_cidr_ipv6": None,
            "ip_ranges": None,
            "role": None,
            "domain_name": None,
            "vlan": 200,
            "tenant_id": None,
            "enabled": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_vip_pool import VastVipPool
        pool = VastVipPool(module)
        result = pool.update_resource({"id": 1, "name": "protocols-vip-pool"})

        mock_client.patch.assert_called_once()
        assert result["vlan"] == 200
