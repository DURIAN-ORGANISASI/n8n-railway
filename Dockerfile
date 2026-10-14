FROM docker.n8n.io/n8nio/n8n:latest

# Railway injects PORT. n8n listens on this port.
ENV N8N_PORT=5678
EXPOSE 5678

# Official image already defines the correct non-root user and startup command.
