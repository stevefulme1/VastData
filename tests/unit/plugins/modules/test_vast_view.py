"""Unit tests for stevefulme1.vastdata.vast_view module."""

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


class TestVastViewCreate:
    """Test view creation."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_create_view(self, mock_get_client):
        """Creating a view calls POST /api/views/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 1,
            "name": "test-view",
            "path": "/data/test",
            "protocols": ["NFS"],
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "test-view",
            "path": "/data/test",
            "protocols": ["NFS"],
            "policy_id": None,
            "tenant_id": None,
            "alias": None,
            "bucket": None,
            "share": None,
            "nfs_interop_flags": None,
            "s3_versioning": None,
            "create_dir": True,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_view import VastView
        view = VastView(module)
        result = view.create_resource()

        mock_client.post.assert_called_once()
        call_data = mock_client.post.call_args[1]["data"]
        assert call_data["name"] == "test-view"
        assert call_data["path"] == "/data/test"
        assert result["id"] == 1


class TestVastViewDelete:
    """Test view deletion."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_delete_view(self, mock_get_client):
        """Deleting a view calls DELETE /api/views/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "test-view",
            "path": "/data/test",
            "state": "absent",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_view import VastView
        view = VastView(module)
        view.delete_resource({"id": 42, "name": "test-view"})

        mock_client.delete.assert_called_once_with("/api/views/42/")


class TestVastViewIdempotent:
    """Test idempotent behavior."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_no_change_needed(self, mock_get_client):
        """When view exists and matches, needs_update returns False."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "test-view",
            "path": "/data/test",
            "protocols": None,
            "policy_id": None,
            "tenant_id": None,
            "alias": None,
            "bucket": None,
            "share": None,
            "nfs_interop_flags": None,
            "s3_versioning": None,
            "create_dir": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_view import VastView
        view = VastView(module)

        existing = {
            "id": 1,
            "name": "test-view",
            "path": "/data/test",
            "protocols": ["NFS"],
        }
        assert not view.needs_update(existing)

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_update_needed(self, mock_get_client):
        """When s3_versioning differs, needs_update returns True."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "test-view",
            "path": "/data/test",
            "protocols": None,
            "policy_id": None,
            "tenant_id": None,
            "alias": None,
            "bucket": None,
            "share": None,
            "nfs_interop_flags": None,
            "s3_versioning": True,
            "create_dir": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_view import VastView
        view = VastView(module)

        existing = {
            "id": 1,
            "name": "test-view",
            "path": "/data/test",
            "s3_versioning": False,
        }
        assert view.needs_update(existing)
