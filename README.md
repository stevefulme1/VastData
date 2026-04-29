# VAST Data Ansible Collection

[![CI](https://github.com/stevefulme1/VastData/actions/workflows/ci.yml/badge.svg)](https://github.com/stevefulme1/VastData/actions/workflows/ci.yml)

Ansible Collection for managing VAST Data Storage Platform.
Provides 46 modules covering storage, authentication, data protection,
networking, multi-tenancy, security, monitoring, and system management.

## Requirements

| Dependency | Version |
|---|---|
| Python | >= 3.12 |
| ansible-core | >= 2.16.0 |
| VAST Python SDK (`vastpy`) | >= 1.0.0 |
| VAST Data Platform | >= 5.4.0 |

## Installation

```bash
ansible-galaxy collection install vastdata.cluster
```

Install the Python dependency:

```bash
pip install vastpy>=1.0.0
```

## Authentication

Configure VAST VMS credentials using one of the following methods:

1. **Username/password**: Provide `vms_user` and `vms_password` parameters
2. **API token**: Provide `api_token` parameter (takes precedence)
3. **Ansible Vault**: Encrypt credentials in a vault-protected vars file

All modules accept the common authentication parameters defined in the
`vastdata.cluster.vast_common` documentation fragment.

## Modules

### Identity & Access

| Module | Description |
|---|---|
| `vast_user` | Manage local users |
| `vast_group` | Manage local groups |
| `vast_nonlocal_user` | Manage non-local (directory-sourced) users |
| `vast_nonlocal_group` | Manage non-local groups |
| `vast_user_key` | Manage user access keys |
| `vast_nonlocal_user_key` | Manage keys for non-local users |
| `vast_api_token` | Create, rotate, and revoke API tokens |
| `vast_admin_role` | Manage administrator roles and permissions |
| `vast_admin_realm` | Configure administrator authentication realms |
| `vast_admin_manager` | Manage administrator manager settings |

### Authentication

| Module | Description |
|---|---|
| `vast_ldap` | Configure LDAP authentication providers |
| `vast_active_directory` | Configure Active Directory integration |
| `vast_nis` | Configure NIS authentication providers |
| `vast_saml_config` | Configure SAML single sign-on |
| `vast_local_provider` | Manage local authentication provider settings |

### Storage

| Module | Description |
|---|---|
| `vast_view` | Manage views (NFS/SMB/S3 multi-protocol exports) |
| `vast_view_policy` | Manage view access policies |
| `vast_volume` | Manage block storage volumes |
| `vast_quota` | Manage storage quotas |
| `vast_folder_read_only` | Set folder read-only flags |
| `vast_protected_path` | Configure protected paths for sensitive data |

### S3 / Object Storage

| Module | Description |
|---|---|
| `vast_s3_policy` | Manage S3 bucket policies |
| `vast_s3_policy_attachment` | Attach S3 policies to users and groups |
| `vast_s3_lifecycle_rule` | Manage S3 object lifecycle rules |

### Data Protection

| Module | Description |
|---|---|
| `vast_snapshot` | Create and manage local snapshots |
| `vast_global_snapshot` | Manage global (cross-cluster) snapshots |
| `vast_global_local_snapshot` | Manage global-local snapshot mappings |
| `vast_protection_policy` | Define protection and retention policies |
| `vast_replication_peer` | Configure native replication peers |
| `vast_s3_replication_peer` | Configure S3 replication peers |

### Network

| Module | Description |
|---|---|
| `vast_vip_pool` | Manage virtual IP pools |
| `vast_dns` | Configure DNS settings |
| `vast_bgp_config` | Configure BGP routing |
| `vast_block_host` | Manage block storage host entries |
| `vast_block_host_mapping` | Map block hosts to volumes |

### QoS & Performance

| Module | Description |
|---|---|
| `vast_qos_policy` | Manage Quality of Service policies |

### Multi-Tenancy

| Module | Description |
|---|---|
| `vast_tenant` | Manage tenants |
| `vast_tenant_encryption` | Configure per-tenant encryption controls |
| `vast_tenant_client_metrics` | Configure tenant client metrics collection |
| `vast_user_tenant_data` | Manage user-tenant data associations |
| `vast_user_copy` | Copy user accounts across tenants |

### Security & Encryption

| Module | Description |
|---|---|
| `vast_encryption_group` | Manage encryption group controls |

### Events & Monitoring

| Module | Description |
|---|---|
| `vast_event_definition` | Define event and alert rules |
| `vast_event_definition_config` | Configure event definition parameters |

### Integration

| Module | Description |
|---|---|
| `vast_kafka_broker` | Configure Kafka broker integration |

### System

| Module | Description |
|---|---|
| `vast_vms` | Manage VAST Management Server settings |

## Usage Examples

### Create a view with NFS and S3 access

```yaml
- name: Create a multi-protocol view
  vastdata.cluster.vast_view:
    vms_host: "vms.example.com"
    api_token: "{{ vault_vast_token }}"
    name: "ai-training-data"
    path: "/data/ai/training"
    protocols:
      - NFS
      - S3
    create_dir: true
    state: present
```

### Set up storage quotas

```yaml
- name: Apply a storage quota
  vastdata.cluster.vast_quota:
    vms_host: "vms.example.com"
    api_token: "{{ vault_vast_token }}"
    name: "team-alpha-quota"
    path: "/data/teams/alpha"
    hard_limit: 10995116277760  # 10 TiB
    soft_limit: 8796093022208   # 8 TiB
    grace_period: "7d"
    enable_alarms: true
    state: present
```

### Configure data protection

```yaml
- name: Create a protection policy
  vastdata.cluster.vast_protection_policy:
    vms_host: "vms.example.com"
    api_token: "{{ vault_vast_token }}"
    name: "daily-snapshots"
    clone_type: NATIVE_REPLICATION
    frames:
      - every: "1D"
        start_at: "00:00"
        keep_local: 7
        keep_remote: 30
    state: present

- name: Take a snapshot
  vastdata.cluster.vast_snapshot:
    vms_host: "vms.example.com"
    api_token: "{{ vault_vast_token }}"
    name: "pre-migration-snap"
    path: "/data/production"
    indestructible: true
    state: present
```

### Multi-tenant provisioning

```yaml
- name: Create a tenant
  vastdata.cluster.vast_tenant:
    vms_host: "vms.example.com"
    api_token: "{{ vault_vast_token }}"
    name: "team-alpha"
    posix_primary_provider: LDAP
    client_ip_ranges:
      - start_ip: "10.0.1.0"
        end_ip: "10.0.1.255"
    state: present
```

## Testing

Run linting and sanity checks:

```bash
pip install ansible-core>=2.16 ansible-lint yamllint flake8
yamllint -c .yamllint .
flake8 plugins/ --max-line-length=120 --ignore=E402,W503
ansible-lint --strict
```

Run sanity tests (must be checked out as `ansible_collections/vastdata/cluster/`):

```bash
ansible-test sanity --python 3.12 -v
```

Run unit tests:

```bash
pip install pytest vastpy
pytest tests/unit/ -v --tb=short
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write your module following the existing patterns in `plugins/modules/`
4. Add unit tests in `tests/unit/`
5. Run sanity and lint checks
6. Submit a pull request

## License

GNU General Public License v3.0 or later.

See [COPYING](COPYING) for the full license text.
