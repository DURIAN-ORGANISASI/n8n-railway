# Security policy

This repository is a deployment starter, not a managed or monitored hosting service. Operators are responsible for n8n, Railway, database access, backups, and secret retention.

## Do not disclose secrets

Never publish or commit:

- `N8N_ENCRYPTION_KEY`, API keys, access tokens, or cookies.
- PostgreSQL passwords, connection strings, Railway credentials, or session data.
- Real `.env` files, unredacted deployment logs, or screenshots containing private identifiers.

If a secret is committed, revoke or rotate it immediately. Removing it in a later commit does not remove it from Git history.

## Secure the deployment

- Complete n8n owner-account setup and restrict access to the editor URL.
- Keep PostgreSQL private to the Railway project; do not expose the database port publicly without a specific, secured requirement.
- Keep a protected copy of `N8N_ENCRYPTION_KEY` separate from the database backup. A database backup alone may not be sufficient to recover encrypted credentials.
- Back up PostgreSQL before upgrading n8n and test recovery using the [Railway PostgreSQL backup/restore guide](https://docs.railway.com/guides/postgres-backups-restores).
- Limit who can view or change Railway variables, volumes, and deployment logs.
- The current template includes `RAILWAY_RUN_UID=0` as a volume-permission workaround. This runs the process as root; understand the increased privilege and test alternatives before removing or changing it.
- Keep n8n pinned to an explicit release. Review upstream release notes and test upgrades separately from production.

## Report a vulnerability

Do not include exploit payloads or secrets in a public issue. If GitHub private vulnerability reporting is enabled for this repository, use it. Otherwise, create a public issue asking for a private reporting channel without disclosing sensitive details.

## Upstream policy and licenses

The root MIT license for this starter does not supersede n8n's own license or terms, Railway's terms, or any third-party obligations. Review the official [n8n Sustainable Use License](https://docs.n8n.io/sustainable-use-license/) and [Railway security/storage guidance](https://docs.railway.com/volumes) for your use case.
