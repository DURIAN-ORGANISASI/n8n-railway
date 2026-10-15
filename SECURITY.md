# Security policy

- Do not publish API keys, database passwords, `N8N_ENCRYPTION_KEY`, `.env` files, or screenshots that expose secrets.
- If a secret is accidentally committed, revoke/rotate it immediately. Deleting it in a later commit does not remove it from Git history.
- Keep the n8n editor behind its built-in owner login and do not share the public URL before completing the first owner setup.
- Keep PostgreSQL private to the Railway project; do not expose its TCP port to the public internet unless you have a specific secured need.
- Back up both the database and the encryption key before upgrades or migrations.
