"""Unit tests for stevefulme1.vastdata.vast_snapshot module."""

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


def _merge_params(extra):
    """Merge base args with extra params (Python 2.7 compatible)."""
    params = _base_args()
    params.update(extra)
    return params


class TestVastSnapshotCreate:
    """Test snapshot creation."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_create_snapshot(self, mock_get_client):
        """Creating a snapshot calls POST /api/snapshots/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 10,
            "name": "pre-migration",
            "path": "/data/prod",
            "indestructible": True,
        }

        module = MagicMock()
        module.params = _merge_params({
            "name": "pre-migration",
            "path": "/data/prod",
            "tenant_id": None,
            "expiration_time": None,
            "indestructible": True,
            "state": "present",
        })
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_snapshot import VastSnapshot
        snap = VastSnapshot(module)
        result = snap.create_resource()

        mock_client.post.assert_called_once()
        call_data = mock_client.post.call_args[1]["data"]
        assert call_data["name"] == "pre-migration"
        assert call_data["path"] == "/data/prod"
        assert call_data["indestructible"] is True
        assert result["id"] == 10


class TestVastSnapshotDelete:
    """Test snapshot deletion."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_delete_snapshot(self, mock_get_client):
        """Deleting a snapshot calls DELETE /api/snapshots/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = _merge_params({"name": "old-snap", "state": "absent"})
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_snapshot import VastSnapshot
        snap = VastSnapshot(module)
        snap.delete_resource({"id": 99, "name": "old-snap"})

        mock_client.delete.assert_called_once_with("/api/snapshots/99/")


class TestVastSnapshotCheckMode:
    """Test check mode behavior."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_check_mode_create(self, mock_get_client):
        """Check mode with no existing snapshot reports changed without creating."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []

        module = MagicMock()
        module.params = _merge_params({
            "name": "test-snap",
            "path": "/data/test",
            "tenant_id": None,
            "expiration_time": None,
            "indestructible": False,
            "state": "present",
        })
        module.check_mode = True

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_snapshot import VastSnapshot
        snap = VastSnapshot(module)
        snap.run()

        mock_client.post.assert_not_called()
        module.exit_json.assert_called_once()
        assert module.exit_json.call_args[1]["changed"] is True
