"""Unit tests for vastdata.cluster.plugins.module_utils.vast_resource."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch


CLIENT_PATH = "ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource"


class TestVastResourceBase:
    """Test base resource lifecycle management."""

    def _make_resource_class(self):
        """Create a concrete subclass for testing."""
        from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase

        class TestResource(VastResourceBase):
            resource_path = "/api/test/"

            def get_resource(self):
                return self._get_by_name()

            def create_resource(self):
                data = {"name": self.module.params["name"]}
                return self._create(data)

            def update_resource(self, resource):
                data = {
                    k: self.module.params[k]
                    for k in self._updatable_attributes()
                    if self.module.params.get(k) is not None
                }
                return self._update(resource["id"], data)

            def delete_resource(self, resource):
                self._delete(resource["id"])

            def _updatable_attributes(self):
                return ["description"]

        return TestResource

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_run_create(self, mock_get_client):
        """State=present with no existing resource triggers create."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {"id": 1, "name": "test"}

        module = MagicMock()
        module.params = {"name": "test", "state": "present", "description": None}
        module.check_mode = False

        cls = self._make_resource_class()
        resource = cls(module)
        resource.run()

        mock_client.post.assert_called_once_with("/api/test/", data={"name": "test"})
        module.exit_json.assert_called_once()
        assert module.exit_json.call_args[1]["changed"] is True

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_run_no_change(self, mock_get_client):
        """State=present with matching resource returns changed=False."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = [{"id": 1, "name": "test", "description": "existing"}]

        module = MagicMock()
        module.params = {"name": "test", "state": "present", "description": None}
        module.check_mode = False

        cls = self._make_resource_class()
        resource = cls(module)
        resource.run()

        mock_client.post.assert_not_called()
        module.exit_json.assert_called_once()
        assert module.exit_json.call_args[1]["changed"] is False

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_run_update(self, mock_get_client):
        """State=present with changed attributes triggers update."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = [{"id": 1, "name": "test", "description": "old"}]
        mock_client.patch.return_value = {"id": 1, "name": "test", "description": "new"}

        module = MagicMock()
        module.params = {"name": "test", "state": "present", "description": "new"}
        module.check_mode = False

        cls = self._make_resource_class()
        resource = cls(module)
        resource.run()

        mock_client.patch.assert_called_once_with(
            "/api/test/1/", data={"description": "new"},
        )
        module.exit_json.assert_called_once()
        assert module.exit_json.call_args[1]["changed"] is True

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_run_delete(self, mock_get_client):
        """State=absent with existing resource triggers delete."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = [{"id": 1, "name": "test"}]

        module = MagicMock()
        module.params = {"name": "test", "state": "absent", "description": None}
        module.check_mode = False

        cls = self._make_resource_class()
        resource = cls(module)
        resource.run()

        mock_client.delete.assert_called_once_with("/api/test/1/")
        module.exit_json.assert_called_once()
        assert module.exit_json.call_args[1]["changed"] is True

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_run_delete_nonexistent(self, mock_get_client):
        """State=absent with no existing resource returns changed=False."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []

        module = MagicMock()
        module.params = {"name": "test", "state": "absent", "description": None}
        module.check_mode = False

        cls = self._make_resource_class()
        resource = cls(module)
        resource.run()

        mock_client.delete.assert_not_called()
        module.exit_json.assert_called_once()
        assert module.exit_json.call_args[1]["changed"] is False

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_check_mode_create(self, mock_get_client):
        """Check mode returns changed=True without creating."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []

        module = MagicMock()
        module.params = {"name": "test", "state": "present", "description": None}
        module.check_mode = True

        cls = self._make_resource_class()
        resource = cls(module)
        resource.run()

        mock_client.post.assert_not_called()
        module.exit_json.assert_called_once()
        assert module.exit_json.call_args[1]["changed"] is True

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_check_mode_delete(self, mock_get_client):
        """Check mode returns changed=True without deleting."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = [{"id": 1, "name": "test"}]

        module = MagicMock()
        module.params = {"name": "test", "state": "absent", "description": None}
        module.check_mode = True

        cls = self._make_resource_class()
        resource = cls(module)
        resource.run()

        mock_client.delete.assert_not_called()
        module.exit_json.assert_called_once()
        assert module.exit_json.call_args[1]["changed"] is True


class TestNeedsUpdate:
    """Test the needs_update comparison logic."""

    def test_no_change(self):
        from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase

        module = MagicMock()
        module.params = {"description": None}

        resource = VastResourceBase.__new__(VastResourceBase)
        resource.module = module
        resource._updatable_attributes = lambda: ["description"]

        assert resource.needs_update({"description": "old"}) is False

    def test_change_detected(self):
        from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase

        module = MagicMock()
        module.params = {"description": "new"}

        resource = VastResourceBase.__new__(VastResourceBase)
        resource.module = module
        resource._updatable_attributes = lambda: ["description"]

        assert resource.needs_update({"description": "old"}) is True

    def test_same_value_no_change(self):
        from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase

        module = MagicMock()
        module.params = {"description": "same"}

        resource = VastResourceBase.__new__(VastResourceBase)
        resource.module = module
        resource._updatable_attributes = lambda: ["description"]

        assert resource.needs_update({"description": "same"}) is False
