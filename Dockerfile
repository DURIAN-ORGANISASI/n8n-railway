# Official n8n image. Pin the version for repeatable deployments.
# Before upgrading, back up PostgreSQL and test release notes.
ARG N8N_VERSION=2.32.6
FROM n8nio/n8n:${N8N_VERSION}
