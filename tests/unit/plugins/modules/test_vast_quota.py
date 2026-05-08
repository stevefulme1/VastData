"""Unit tests for stevefulme1.vastdata.vast_quota module."""

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


class TestVastQuotaCreate:
    """Test quota creation."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_create_quota(self, mock_get_client):
        """Creating a quota calls POST /api/quotas/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 1,
            "name": "team_quota",
            "path": "/data/teams/engineering",
            "soft_limit": 5497558138880,
            "hard_limit": 10995116277760,
            "enable_alarms": True,
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "team_quota",
            "path": "/data/teams/engineering",
            "tenant_id": None,
            "soft_limit": 5497558138880,
            "hard_limit": 10995116277760,
            "grace_period": None,
            "soft_limit_inodes": None,
            "hard_limit_inodes": None,
            "enable_alarms": True,
            "entity": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_quota import VastQuota
        quota = VastQuota(module)
        result = quota.create_resource()

        mock_client.post.assert_called_once()
        call_data = mock_client.post.call_args[1]["data"]
        assert call_data["name"] == "team_quota"
        assert call_data["path"] == "/data/teams/engineering"
        assert call_data["soft_limit"] == 5497558138880
        assert result["id"] == 1


class TestVastQuotaDelete:
    """Test quota deletion."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_delete_quota(self, mock_get_client):
        """Deleting a quota calls DELETE /api/quotas/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "team_quota",
            "path": "/data/teams/engineering",
            "state": "absent",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_quota import VastQuota
        quota = VastQuota(module)
        quota.delete_resource({"id": 10, "name": "team_quota"})

        mock_client.delete.assert_called_once_with("/api/quotas/10/")


class TestVastQuotaIdempotent:
    """Test idempotent behavior."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_no_change_needed(self, mock_get_client):
        """When quota exists and matches, needs_update returns False."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "team_quota",
            "path": "/data/teams/engineering",
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

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_quota import VastQuota
        quota = VastQuota(module)

        existing = {
            "id": 1,
            "name": "team_quota",
            "path": "/data/teams/engineering",
            "soft_limit": 5497558138880,
            "hard_limit": 10995116277760,
        }
        assert not quota.needs_update(existing)

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_update_needed(self, mock_get_client):
        """When hard_limit differs, needs_update returns True."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "team_quota",
            "path": "/data/teams/engineering",
            "tenant_id": None,
            "soft_limit": None,
            "hard_limit": 21990232555520,
            "grace_period": None,
            "soft_limit_inodes": None,
            "hard_limit_inodes": None,
            "enable_alarms": None,
            "entity": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_quota import VastQuota
        quota = VastQuota(module)

        existing = {
            "id": 1,
            "name": "team_quota",
            "path": "/data/teams/engineering",
            "hard_limit": 10995116277760,
        }
        assert quota.needs_update(existing)

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_update_resource(self, mock_get_client):
        """Updating a quota calls PATCH /api/quotas/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.patch.return_value = {
            "id": 1,
            "name": "team_quota",
            "hard_limit": 21990232555520,
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "team_quota",
            "path": "/data/teams/engineering",
            "tenant_id": None,
            "soft_limit": None,
            "hard_limit": 21990232555520,
            "grace_period": None,
            "soft_limit_inodes": None,
            "hard_limit_inodes": None,
            "enable_alarms": None,
            "entity": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_quota import VastQuota
        quota = VastQuota(module)
        result = quota.update_resource({"id": 1, "name": "team_quota"})

        mock_client.patch.assert_called_once()
        assert result["hard_limit"] == 21990232555520
