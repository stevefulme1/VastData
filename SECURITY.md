# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |
| < 1.0   | No        |

## Reporting a Vulnerability

If you discover a security vulnerability in this collection, please report
it responsibly. **Do not open a public GitHub issue.**

### How to Report

1. Email the maintainers at **sfulmer@redhat.com** with:
   - A description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

2. You will receive an acknowledgment within **48 hours**.

3. We will work with you to understand the issue, develop a fix, and
   coordinate disclosure.

### What to Expect

- **Acknowledgment**: Within 48 hours of report.
- **Assessment**: Within 5 business days we will confirm the vulnerability
  and its severity.
- **Fix**: A patch will be developed and tested privately.
- **Disclosure**: A new release will be published with the fix, and a
  security advisory will be issued via GitHub.

## Security Best Practices for Users

When using this collection:

- **Never commit VMS credentials** (passwords, API tokens) to version
  control.
- Use `no_log: true` on tasks that handle sensitive data.
- Prefer **API tokens** over username/password for automation.
- Use Ansible Vault to encrypt sensitive variables in playbooks.
- Set `validate_certs: true` (default) to verify VMS TLS certificates.
- Review VMS access policies to grant only the minimum permissions required.

## Sensitive Parameters

The following module parameters are marked `no_log` in the argument spec
and will not appear in Ansible logs:

- `vms_password` (common auth parameter)
- `api_token` (common auth parameter)
- `password` (`vast_user`, `vast_active_directory`, `vast_ldap`)
- `bind_password` (`vast_ldap`)
- `secret_key` (`vast_s3_replication_peer`)
- `sasl_password` (`vast_kafka_broker`)
- `snmp_community` (`vast_vms`)
