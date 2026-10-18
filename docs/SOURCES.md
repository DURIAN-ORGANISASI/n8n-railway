# Sources, attribution, and licensing

This repository is a deployment starter for running the official n8n container with PostgreSQL on Railway. The references below describe upstream products; they do not imply endorsement or affiliation.

## Official technical references

- [Railway guide: Self-host n8n](https://docs.railway.com/guides/n8n) — deployment, domain, webhook URL, and PostgreSQL references.
- [Railway variables](https://docs.railway.com/variables) and [variable reference syntax](https://docs.railway.com/variables/reference) — service variables and cross-service references such as `${{Postgres.PGHOST}}`.
- [Railway volumes](https://docs.railway.com/volumes) — persistent storage, mount paths, and permission behavior.
- [Railway PostgreSQL backups and restores](https://docs.railway.com/guides/postgres-backups-restores) — backup and recovery planning.
- [n8n Docker installation](https://docs.n8n.io/hosting/installation/docker/) — official container deployment.
- [n8n environment variables](https://docs.n8n.io/hosting/configuration/environment-variables/) — configuration reference.
- [n8n security environment variables](https://docs.n8n.io/hosting/configuration/environment-variables/security/) — security-related configuration, including encryption.
- [n8n Sustainable Use License](https://docs.n8n.io/sustainable-use-license/) and [n8n licensing FAQ](https://support.n8n.io/article/can-i-use-your-license-for-my-use-case) — licensing terms for the upstream n8n software.
- [Docker documentation](https://docs.docker.com/) — container concepts and behavior.
- [GitHub repository licensing guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) — license-file guidance.

## Project files and generated assets

- `Dockerfile` selects the upstream `n8nio/n8n` image and pins the release using `N8N_VERSION`.
- `scripts/generate-key.ps1` and `scripts/generate-key.sh` use platform cryptographic random-number generators to create a 32-byte hexadecimal encryption key.
- `docs/architecture.svg` is a diagram created for this repository. It is a documentation illustration, not an official Railway or n8n screenshot.

## License scope and trademarks

The root [`LICENSE`](../LICENSE) applies to this repository's own template material, scripts, and documentation to the extent covered by that license. It does **not** relicense the upstream n8n image or PostgreSQL, grant rights to third-party trademarks, or override platform terms.

n8n's self-hosted software uses its own Sustainable Use License (and other terms may apply to particular editions or use cases). Read the current [n8n license](https://docs.n8n.io/sustainable-use-license/) and [license FAQ](https://support.n8n.io/article/can-i-use-your-license-for-my-use-case) before commercial use or redistribution. Railway, Docker, PostgreSQL, and n8n names and marks belong to their respective owners. This independent starter is not affiliated with or endorsed by them.
