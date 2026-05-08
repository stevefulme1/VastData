"""Unit tests for vastdata.cluster.vast_vip_pool module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch


CLIENT_PATH = "ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource"


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

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_create_vip_pool(self, mock_get_client):
        """Creating a VIP pool calls POST /api/vippools/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 1,
            "name": "pool-mgmt",
            "subnet_cidr": 24,
            "ip_ranges": [{"start_ip": "10.0.0.10", "end_ip": "10.0.0.20"}],
            "role": "MANAGEMENT",
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "pool-mgmt",
            "subnet_cidr": 24,
            "subnet_cidr_ipv6": None,
            "ip_ranges": [{"start_ip": "10.0.0.10", "end_ip": "10.0.0.20"}],
            "role": "MANAGEMENT",
            "domain_name": None,
            "vlan": None,
            "tenant_id": None,
            "enabled": True,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_vip_pool import VastVipPool
        pool = VastVipPool(module)
        result = pool.create_resource()

        mock_client.post.assert_called_once()
        call_data = mock_client.post.call_args[1]["data"]
        assert call_data["name"] == "pool-mgmt"
        assert call_data["subnet_cidr"] == 24
        assert call_data["role"] == "MANAGEMENT"
        assert len(call_data["ip_ranges"]) == 1
        assert result["id"] == 1


class TestVastVipPoolDelete:
    """Test VIP pool deletion."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_delete_vip_pool(self, mock_get_client):
        """Deleting a VIP pool calls DELETE /api/vippools/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {**_base_args(), "name": "pool-mgmt", "state": "absent"}
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_vip_pool import VastVipPool
        pool = VastVipPool(module)
        pool.delete_resource({"id": 7, "name": "pool-mgmt"})

        mock_client.delete.assert_called_once_with("/api/vippools/7/")


class TestVastVipPoolIdempotent:
    """Test idempotent behavior."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_no_update_when_matching(self, mock_get_client):
        """No update triggered when params are None."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "pool-mgmt",
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

        from ansible_collections.vastdata.cluster.plugins.modules.vast_vip_pool import VastVipPool
        pool = VastVipPool(module)

        existing = {"id": 7, "name": "pool-mgmt", "role": "MANAGEMENT", "subnet_cidr": 24}
        assert not pool.needs_update(existing)

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_update_needed(self, mock_get_client):
        """When role differs, needs_update returns True."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "pool-mgmt",
            "subnet_cidr": None,
            "subnet_cidr_ipv6": None,
            "ip_ranges": None,
            "role": "PROTOCOLS",
            "domain_name": None,
            "vlan": None,
            "tenant_id": None,
            "enabled": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_vip_pool import VastVipPool
        pool = VastVipPool(module)

        existing = {"id": 7, "name": "pool-mgmt", "role": "MANAGEMENT"}
        assert pool.needs_update(existing)


class TestVastVipPoolUpdate:
    """Test VIP pool update."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_update_vip_pool(self, mock_get_client):
        """Updating a VIP pool calls PATCH /api/vippools/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.patch.return_value = {
            "id": 7,
            "name": "pool-mgmt",
            "role": "PROTOCOLS",
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "pool-mgmt",
            "subnet_cidr": None,
            "subnet_cidr_ipv6": None,
            "ip_ranges": None,
            "role": "PROTOCOLS",
            "domain_name": None,
            "vlan": None,
            "tenant_id": None,
            "enabled": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_vip_pool import VastVipPool
        pool = VastVipPool(module)
        result = pool.update_resource({"id": 7, "name": "pool-mgmt"})

        mock_client.patch.assert_called_once()
        call_data = mock_client.patch.call_args[1]["data"]
        assert call_data["role"] == "PROTOCOLS"
        assert result["id"] == 7
