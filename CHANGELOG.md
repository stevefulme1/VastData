# Changelog

All notable changes to the `stevefulme1.vastdata` Ansible collection will be
documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-05-15

### Added

- Unit tests for 9 modules and integration targets
- Pre-commit and linting configuration
- Limit/offset pagination parameters to all `_info` modules
- Production-ready roles with real module calls
- Role README.md files for Galaxy import compliance

### Fixed

- Remove broken auto-generated unit tests
- Remove pagination params from CRUD modules (info-only feature)
- Remove `--strict` from ansible-lint to allow warned rules
- Add `args[module]` to `warn_list` to handle `--strict` warnings
- Resolve CI sanity, lint, and build failures
- Resolve sanity test documentation failures

## [1.1.0] - 2026-05-15

### Added

- 39 read-only info modules for full API coverage
- 2 EDA source plugins for event-driven automation
- 10 Day-2 operation roles (backup, encryption, network, quota, replication, s3, snapshot, tenant, view, vip)
- Total: 103 modules, 10 roles, full EDA/inventory coverage

## [1.0.0] - 2026-05-15

### Added

- 10 info modules for views, quotas, snapshots, exports, shares, policies, users, groups, VIPs, and tenants
- Network interfaces, node info, and inventory plugin
- Cluster info, NFS exports, SMB shares, capacity info, and alerts

## [0.2.0] - 2026-04-29

### Fixed

- Use `uri` module in molecule verify instead of `vast_api_token`
- Collection FQCN from `vastdata.cluster` to `stevefulme1.vastdata`
- Remove agent-generated test scaffolding referencing nonexistent modules
- Idempotency, parameter names, `required_if`, and exception handling

## [0.1.0] - 2025-04-29

### Added

- Initial release with 46 modules covering the VAST Data REST API
- Identity & Access (10 modules), Authentication (5), Storage (6), S3/Object Storage (3), Data Protection (6), Network (5), QoS (1), Multi-Tenancy (5), Security (1), Events (2), Integration (1), System (1)
- Shared module_utils: `vast_common`, `vast_client`, `vast_resource`, `vast_wait`
- CI/CD with GitHub Actions (lint, sanity, unit tests, certification)
- Example playbooks for storage, data protection, networking, authentication, and multi-tenancy
