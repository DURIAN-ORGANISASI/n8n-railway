<div align="center">

# 🚀 n8n Railway Starter

**Deploy n8n + PostgreSQL di Railway.**

</div>

## Instalasi

### Tahap 1 — Buat project Railway
Buat project di [Railway](https://railway.com/). PostgreSQL dan n8n harus berada di project serta environment yang sama.

### Tahap 2 — Tambahkan PostgreSQL terlebih dahulu
1. Pilih **New → Database → PostgreSQL**.
2. Tunggu sampai database sehat/online.
3. Gunakan nama service **Postgres** agar cocok dengan variabel di bawah.

Railway membuat variabel database otomatis; **jangan membuat atau menempelkan variabel database secara manual**.

### Tahap 3 — Siapkan repo
Fork repo ini atau unggah isinya ke GitHub. Pastikan `Dockerfile` berada di root. Jangan unggah password atau key rahasia.

### Tahap 4 — Deploy service n8n dari GitHub
Di project yang sama, pilih **New → GitHub Repo**, lalu pilih repo ini. Biarkan Root Directory kosong.

### Tahap 5 — Buat domain dan volume
Pada **service n8n**:
1. **Settings → Networking → Generate Domain**.
2. Tambahkan volume dengan mount path `/home/node/.n8n`.

### Tahap 6 — Tempel variabel
Buat encryption key:
- **Windows:** `.\scripts\generate-key.ps1`
- **Linux/macOS:** `sh scripts/generate-key.sh`

Salin blok berikut ke **n8n → Variables → Raw Editor**. Ganti placeholder key. Blok ini hanya untuk service **n8n**, bukan Postgres.

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

Jika nama service database bukan `Postgres`, ubah namespace `Postgres` pada referensi database. Simpan encryption key dengan aman dan jangan menggantinya setelah membuat kredensial.

> `RAILWAY_RUN_UID=0` mengatasi izin volume pada setup ini, tetapi menjalankan proses sebagai root.

### Tahap 7 — Deploy
Simpan variabel, redeploy n8n, lalu buka domain Railway. Pastikan log menunjukkan n8n siap dan uji satu workflow sederhana.

## Troubleshooting
- **Database gagal tersambung:** periksa status Postgres, nama service, dan project/environment.
- **`EACCES: permission denied`:** pastikan volume terpasang di `/home/node/.n8n` dan `RAILWAY_RUN_UID=0` disetel.

**Backup:** simpan backup PostgreSQL dan `N8N_ENCRYPTION_KEY` secara terpisah sebelum upgrade.

[Dokumentasi Railway n8n](https://docs.railway.com/guides/n8n) · [Dokumentasi variabel n8n](https://docs.n8n.io/hosting/configuration/environment-variables/)
