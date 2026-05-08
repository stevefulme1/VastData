"""Unit tests for vastdata.cluster.vast_quota module."""

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


class TestVastQuotaCreate:
    """Test quota creation."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_create_quota(self, mock_get_client):
        """Creating a quota calls POST /api/quotas/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 20,
            "name": "team-quota",
            "path": "/data/team",
            "hard_limit": 1099511627776,
            "soft_limit": 549755813888,
            "grace_period": "7d",
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "team-quota",
            "path": "/data/team",
            "tenant_id": None,
            "soft_limit": 549755813888,
            "hard_limit": 1099511627776,
            "grace_period": "7d",
            "soft_limit_inodes": None,
            "hard_limit_inodes": None,
            "enable_alarms": True,
            "entity": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_quota import VastQuota
        quota = VastQuota(module)
        result = quota.create_resource()

        mock_client.post.assert_called_once()
        call_data = mock_client.post.call_args[1]["data"]
        assert call_data["name"] == "team-quota"
        assert call_data["path"] == "/data/team"
        assert call_data["hard_limit"] == 1099511627776
        assert call_data["soft_limit"] == 549755813888
        assert result["id"] == 20


class TestVastQuotaDelete:
    """Test quota deletion."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_delete_quota(self, mock_get_client):
        """Deleting a quota calls DELETE /api/quotas/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {**_base_args(), "name": "old-quota", "state": "absent"}
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_quota import VastQuota
        quota = VastQuota(module)
        quota.delete_resource({"id": 44, "name": "old-quota"})

        mock_client.delete.assert_called_once_with("/api/quotas/44/")


class TestVastQuotaIdempotent:
    """Test idempotent behavior."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_no_update_when_matching(self, mock_get_client):
        """No update triggered when params are None."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "team-quota",
            "path": "/data/team",
            "tenant_id": None,
            "soft_limit": None,
            "hard_limit": None,
            "grace_period": None,
            "soft_limit_inodes": None,
            "hard_limit_inodes": None,
            "enable_alarms": None,
            "entity": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_quota import VastQuota
        quota = VastQuota(module)

        existing = {"id": 20, "name": "team-quota", "path": "/data/team", "hard_limit": 1099511627776}
        assert not quota.needs_update(existing)

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_update_needed(self, mock_get_client):
        """When hard_limit differs, needs_update returns True."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "team-quota",
            "path": "/data/team",
            "tenant_id": None,
            "soft_limit": None,
            "hard_limit": 2199023255552,
            "grace_period": None,
            "soft_limit_inodes": None,
            "hard_limit_inodes": None,
            "enable_alarms": None,
            "entity": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_quota import VastQuota
        quota = VastQuota(module)

        existing = {"id": 20, "name": "team-quota", "hard_limit": 1099511627776}
        assert quota.needs_update(existing)


class TestVastQuotaUpdate:
    """Test quota update."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_update_quota(self, mock_get_client):
        """Updating a quota calls PATCH /api/quotas/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.patch.return_value = {
            "id": 20,
            "name": "team-quota",
            "hard_limit": 2199023255552,
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "team-quota",
            "path": "/data/team",
            "tenant_id": None,
            "soft_limit": None,
            "hard_limit": 2199023255552,
            "grace_period": None,
            "soft_limit_inodes": None,
            "hard_limit_inodes": None,
            "enable_alarms": None,
            "entity": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_quota import VastQuota
        quota = VastQuota(module)
        result = quota.update_resource({"id": 20, "name": "team-quota"})

        mock_client.patch.assert_called_once()
        call_data = mock_client.patch.call_args[1]["data"]
        assert call_data["hard_limit"] == 2199023255552
        assert result["id"] == 20
