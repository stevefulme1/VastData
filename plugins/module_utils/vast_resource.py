"""Base resource helper for VAST Data Ansible modules."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module_utils: vast_resource
short_description: Base class for VAST Data resource management modules
description:
  - Provides VastResourceBase, an abstract base class that implements the
    standard create/update/delete lifecycle for VAST Data resources with
    built-in check mode support and change detection.
  - Includes convenience methods for REST operations (get by name/ID, create,
    update, delete) against the VAST VMS API. Subclasses set resource_path and
    override the resource lifecycle methods.
author:
  - Steve Fulmer (@stevefulme1)
"""

from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client import get_vast_client

try:
    from vastpy import RESTFailure
    HAS_VASTPY = True
except ImportError:
    HAS_VASTPY = False


class VastResourceBase:
    """Base class for VAST Data resource management modules.

    Subclasses must implement:
        - resource_path: the REST API path (e.g. "/api/views/")
        - get_resource(): retrieve current resource state
        - create_resource(): create a new resource
        - update_resource(): update an existing resource
        - delete_resource(): delete a resource
    """

    resource_path = None

    def __init__(self, module):
        self.module = module
        self.client = get_vast_client(module)
        self.check_mode = module.check_mode

    def get_resource(self):
        """Return the current resource dict or None if not found."""
        raise NotImplementedError

    def create_resource(self):
        """Create the resource and return it."""
        raise NotImplementedError

    def update_resource(self, resource):
        """Update the resource and return it."""
        raise NotImplementedError

    def delete_resource(self, resource):
        """Delete the resource."""
        raise NotImplementedError

    def needs_update(self, resource):
        """Check if resource attributes differ from desired state."""
        for key in self._updatable_attributes():
            desired = self.module.params.get(key)
            if desired is None:
                continue
            current = resource.get(key)
            if current != desired:
                return True
        return False

    def _updatable_attributes(self):
        """Return list of attribute names that can be updated."""
        return []

    def _get_by_name(self, name_field="name"):
        """Look up a resource by name using the list endpoint."""
        name = self.module.params.get(name_field)
        if not name:
            return None
        try:
            resources = self.client.get(self.resource_path)
            if isinstance(resources, list):
                for r in resources:
                    if r.get(name_field) == name:
                        return r
            return None
        except RESTFailure as exc:
            if exc.status == 404:
                return None
            raise

    def _get_by_id(self, resource_id):
        """Look up a resource by its ID."""
        try:
            return self.client.get("{0}{1}/".format(self.resource_path, resource_id))
        except RESTFailure as exc:
            if exc.status == 404:
                return None
            raise

    def _create(self, data):
        """POST to create a resource."""
        return self.client.post(self.resource_path, data=data)

    def _update(self, resource_id, data):
        """PATCH to update a resource."""
        return self.client.patch("{0}{1}/".format(self.resource_path, resource_id), data=data)

    def _delete(self, resource_id):
        """DELETE a resource."""
        return self.client.delete("{0}{1}/".format(self.resource_path, resource_id))

    def run(self):
        """Main entry point -- determine action and execute."""
        state = self.module.params.get("state", "present")
        resource = self.get_resource()

        if state == "absent":
            if resource is None:
                self.module.exit_json(changed=False)
                return
            if self.check_mode:
                self.module.exit_json(changed=True)
                return
            self.delete_resource(resource)
            self.module.exit_json(changed=True)
            return

        # state == present
        if resource is None:
            if self.check_mode:
                self.module.exit_json(changed=True)
                return
            resource = self.create_resource()
            self.module.exit_json(changed=True, resource=resource)
            return

        if self.needs_update(resource):
            if self.check_mode:
                self.module.exit_json(changed=True)
                return
            resource = self.update_resource(resource)
            self.module.exit_json(changed=True, resource=resource)
            return

        self.module.exit_json(changed=False, resource=resource)
