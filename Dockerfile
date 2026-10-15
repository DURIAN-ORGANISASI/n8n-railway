# Official n8n image. Pin the version for repeatable deployments.
# Upgrade prepared for MCP client setup (available since n8n 2.33.0).
# Before merging/deploying, back up PostgreSQL and test release notes.
ARG N8N_VERSION=2.43.5
FROM n8nio/n8n:${N8N_VERSION}
