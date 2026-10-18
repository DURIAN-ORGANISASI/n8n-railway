<div align="center">

# n8n Railway Starter

**Deploy n8n + PostgreSQL on Railway with persistent storage, documented settings, and a cryptographically generated encryption key.**

<p>
  <a href="https://github.com/DURIAN-ORGANISASI/n8n-railway/actions/workflows/validate.yml"><img alt="Repository validation" src="https://img.shields.io/github/actions/workflow/status/DURIAN-ORGANISASI/n8n-railway/validate.yml?branch=main&amp;label=validation&amp;logo=githubactions&amp;logoColor=white"></a>
  <a href="LICENSE"><img alt="MIT License for this starter" src="https://img.shields.io/github/license/DURIAN-ORGANISASI/n8n-railway?label=starter%20license"></a>
  <img alt="Pinned n8n release" src="https://img.shields.io/badge/n8n-2.43.5-FF6D5A?logo=n8n&amp;logoColor=white">
  <img alt="Railway deployment" src="https://img.shields.io/badge/Deploy-Railway-0B0D0E?logo=railway&amp;logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&amp;logoColor=white">
</p>

<p><a href="README.md">🇮🇩 Bahasa Indonesia</a> · <a href="README.en.md">🇬🇧 English</a></p>

<p>
  <a href="#railway-deployment">Railway deployment</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#security-and-backups">Security &amp; backups</a> ·
  <a href="#troubleshooting">Troubleshooting</a> ·
  <a href="#sources-attribution-and-licensing">Sources &amp; license</a>
</p>

</div>

---

## Overview

This starter deploys **n8n and PostgreSQL as separate services in the same Railway project/environment**. The Dockerfile pins the n8n release to avoid silent upgrades. n8n data requires a Railway Volume.

> [!IMPORTANT]
> **The MIT license in this repository is not the license for n8n itself.** MIT covers this starter's own material to the extent included in the license; n8n Community Edition has its own upstream license. Read [Sources, attribution, and licensing](#sources-attribution-and-licensing) before use or redistribution.

## Architecture

![n8n and PostgreSQL deployment architecture on Railway](docs/architecture.svg)

<sub>A project-created conceptual diagram, not an official n8n or Railway screenshot.</sub>

## Railway deployment

### 1. **Create the project and PostgreSQL.**

On [Railway](https://railway.com/), create a project and choose **New → Database → PostgreSQL**. Wait until the database is healthy. Name the service `Postgres` and keep it in the same project/environment as n8n. Railway provides database reference variables automatically; **do not manually create or paste database variables**.

If you use a different database service name, update the `Postgres` namespace in the reference variables.

### 2. Prepare the GitHub repository.

Fork this repository or upload its contents to your GitHub account. Keep `Dockerfile` and `railway.json` at the repository root.

### 3. **Deploy n8n.**

In the same Railway project, choose **New → GitHub Repo** and select your repository. Leave **Root Directory** empty so Railway can find the build configuration.

### 4. Generate a domain and add a volume.

On the n8n service:

- Open **Settings → Networking → Generate Domain**. Use port `5678` if Railway asks for the target port.
- Add a **Volume** mounted at `/home/node/.n8n`.
- `N8N_HOST`, `N8N_EDITOR_BASE_URL`, and `WEBHOOK_URL` use the `RAILWAY_PUBLIC_DOMAIN` reference in the example.

### 5. Generate the encryption key and set variables.

Run one of the scripts from the repository root:

- Windows PowerShell: `.\scripts\generate-key.ps1`
- Linux/macOS: `sh scripts/generate-key.sh`

The script generates 32 random bytes encoded as hexadecimal. Store the output as a secret.

Paste the following block into **n8n service → Variables → Raw Editor**. Replace `REPLACE_WITH_YOUR_64_CHARACTER_HEX_KEY` with your generated key. **This block is for the n8n service only, not the PostgreSQL service.**

```dotenv
N8N_PORT=5678
N8N_PROTOCOL=https
N8N_HOST=${{RAILWAY_PUBLIC_DOMAIN}}
N8N_EDITOR_BASE_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
WEBHOOK_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
N8N_PROXY_HOPS=1
N8N_SECURE_COOKIE=true
N8N_ENCRYPTION_KEY=REPLACE_WITH_YOUR_64_CHARACTER_HEX_KEY
N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true

# Volume-permission workaround for this setup; runs the process as root.
RAILWAY_RUN_UID=0

DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=${{Postgres.PGHOST}}
DB_POSTGRESDB_PORT=${{Postgres.PGPORT}}
DB_POSTGRESDB_DATABASE=${{Postgres.PGDATABASE}}
DB_POSTGRESDB_USER=${{Postgres.PGUSER}}
DB_POSTGRESDB_PASSWORD=${{Postgres.PGPASSWORD}}

GENERIC_TIMEZONE=Asia/Jakarta
TZ=Asia/Jakarta
N8N_DIAGNOSTICS_ENABLED=false
N8N_PERSONALIZATION_ENABLED=false
N8N_VERSION_NOTIFICATIONS_ENABLED=false
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=168
```

Use **Railway reference variables** for the database instead of manually pasting credentials:

| n8n variable | Reference value |
| --- | --- |
| `DB_POSTGRESDB_HOST` | `${{Postgres.PGHOST}}` |
| `DB_POSTGRESDB_PORT` | `${{Postgres.PGPORT}}` |
| `DB_POSTGRESDB_DATABASE` | `${{Postgres.PGDATABASE}}` |
| `DB_POSTGRESDB_USER` | `${{Postgres.PGUSER}}` |
| `DB_POSTGRESDB_PASSWORD` | `${{Postgres.PGPASSWORD}}` |

The reference-value expressions are provided by Railway's variable system. Their namespace must match your PostgreSQL service name (the examples use `Postgres`).

> [!WARNING]
> `RAILWAY_RUN_UID=0` is a volume-permission workaround and runs the process as root. Use it only when needed for this volume setup and understand the increased privilege. Do not change this setting on an active service without testing volume permissions and preparing a rollback.

### 6. Deploy and verify.

Save the variables and redeploy n8n. Open the Railway domain and complete the owner-account setup promptly. Sign in and run a small test workflow. A successful image build alone does not prove that the service and database connection are healthy.

## Local Docker Compose variables

`n8n-service-variables.example.txt` is for the Railway n8n service. For local use, start from `.env.example`:

```bash
cp .env.example .env
sh scripts/generate-key.sh
```

Copy the generated key into `N8N_ENCRYPTION_KEY` in `.env`, set a strong `POSTGRES_PASSWORD`, then run:

```bash
docker compose -f docker-compose.local.yml up -d --build
```

Never commit `.env`; `.gitignore` excludes it.

## Security and backups

- **Protect the encryption key.** Stored n8n credentials depend on the same key. Losing the key can make stored credentials impossible to decrypt.
- **Back up before upgrades.** Back up PostgreSQL and keep the key separately before upgrading or migrating.
- **Test recovery.** Follow the [Railway PostgreSQL backup and restore guide](https://docs.railway.com/guides/postgres-backups-restores).
- **Keep the database private.** Service-to-service connections do not require a public PostgreSQL port.
- **Secure the editor and logs.** Complete owner setup, limit access, and redact passwords, encryption keys, connection strings, and tokens from shared logs or screenshots.
- **Review n8n licensing.** The MIT license for this starter does not change upstream n8n terms.

## Upgrading n8n

The release is pinned using `ARG N8N_VERSION` in `Dockerfile`, currently `2.43.5`. This is **not a claim that it is the latest release**. Before upgrading, read n8n release notes, back up PostgreSQL and the key, and test in a separate environment. Do not switch to `latest` without an upgrade and rollback procedure.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| PostgreSQL cannot connect | Confirm the database is healthy, in the same project/environment, named correctly, and its references are deployed. |
| Webhook uses the wrong URL | Check the public domain and `WEBHOOK_URL`, then redeploy. |
| `EACCES: permission denied` | Confirm the volume is mounted at `/home/node/.n8n`; review whether `RAILWAY_RUN_UID=0` is needed. |
| Stored credentials cannot be opened | Ensure `N8N_ENCRYPTION_KEY` matches the key used when those credentials were created. Do not change it casually. |
| Data disappears after redeploy | Check the n8n Railway Volume and PostgreSQL persistent storage. |
| Build succeeds but service is unhealthy | Check deployment logs, the `/healthz` health check, database connectivity, and missing variables. |

## Development and validation

From the repository root, run these static checks:

```bash
python scripts/validate-repo.py
python scripts/check_docs.py
python -m json.tool railway.json
```

These checks validate configuration files, local links, and SVG/XML syntax. They are **not** end-to-end tests of a live Railway account, database connection, n8n migrations, or external webhooks.

## Sources, attribution, and licensing

See [`docs/SOURCES.md`](docs/SOURCES.md) for technical references, diagram attribution, upstream licensing, and trademark notes.

- **Repository license:** [MIT License](LICENSE), for covered project material.
- **n8n license:** n8n Community Edition uses the [Sustainable Use License](https://docs.n8n.io/sustainable-use-license/) and related terms. Evaluate your own use case; do not assume all deployed software is licensed under MIT.
- **Third parties:** PostgreSQL, Docker, Railway, and n8n have their own terms and trademarks.

## Contributing

Issues and Pull Requests are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`SECURITY.md`](SECURITY.md). Do not upload environment files or logs containing secrets.

---

<sub>Independent community project; not affiliated with or endorsed by n8n, Railway, Docker, or PostgreSQL.</sub>
