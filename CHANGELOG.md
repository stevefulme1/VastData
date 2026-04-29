# Changelog

All notable changes to the `vastdata.cluster` Ansible collection will be
documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-04-29

### Added

- Initial release with 46 modules covering the VAST Data REST API.
- **Identity & Access** (10 modules): `vast_user`, `vast_group`,
  `vast_nonlocal_user`, `vast_nonlocal_group`, `vast_user_key`,
  `vast_nonlocal_user_key`, `vast_api_token`, `vast_admin_role`,
  `vast_admin_realm`, `vast_admin_manager`.
- **Authentication** (5 modules): `vast_ldap`, `vast_active_directory`,
  `vast_nis`, `vast_saml_config`, `vast_local_provider`.
- **Storage** (6 modules): `vast_view`, `vast_view_policy`, `vast_volume`,
  `vast_quota`, `vast_folder_read_only`, `vast_protected_path`.
- **S3 / Object Storage** (3 modules): `vast_s3_policy`,
  `vast_s3_policy_attachment`, `vast_s3_lifecycle_rule`.
- **Data Protection** (6 modules): `vast_snapshot`, `vast_global_snapshot`,
  `vast_global_local_snapshot`, `vast_protection_policy`,
  `vast_replication_peer`, `vast_s3_replication_peer`.
- **Network** (5 modules): `vast_vip_pool`, `vast_dns`, `vast_bgp_config`,
  `vast_block_host`, `vast_block_host_mapping`.
- **QoS** (1 module): `vast_qos_policy`.
- **Multi-Tenancy** (5 modules): `vast_tenant`, `vast_tenant_encryption`,
  `vast_tenant_client_metrics`, `vast_user_tenant_data`, `vast_user_copy`.
- **Security** (1 module): `vast_encryption_group`.
- **Events** (2 modules): `vast_event_definition`,
  `vast_event_definition_config`.
- **Integration** (1 module): `vast_kafka_broker`.
- **System** (1 module): `vast_vms`.
- Shared `module_utils`: `vast_common`, `vast_client`, `vast_resource`,
  `vast_wait`.
- Documentation fragment: `vast_common`.
- CI/CD with GitHub Actions (lint, sanity, unit tests, certification).
- Example playbooks for storage, data protection, networking,
  authentication, and multi-tenancy.
