# n8n on Railway — Production-minded Starter

Repository starter untuk menjalankan **n8n di Railway**. Disiapkan untuk deployment dari GitHub, penggunaan PostgreSQL, persistent storage, keamanan dasar, dan panduan troubleshooting.

> **Penting:** repo ini menyiapkan konfigurasi aplikasi, bukan membuat project/service Railway secara otomatis. Setelah repo di-push ke GitHub, hubungkan repo ini sebagai service di Railway dan ikuti langkah di bawah. Jangan memasukkan API key, password, atau `N8N_ENCRYPTION_KEY` ke GitHub.

## Isi repository

- `Dockerfile` — memakai image resmi n8n.
- `railway.json` — kebijakan build/deploy Railway.
- `.env.example` — contoh variabel lokal (jangan gunakan password contoh untuk produksi).
- `docker-compose.yml` — opsi menjalankan lokal dengan PostgreSQL.
- `.gitignore` — mencegah file rahasia dan data lokal ikut ter-commit.
- `docs/RAILWAY_SETUP.md` — panduan deploy lengkap.
- `docs/SECURITY.md` — catatan keamanan, backup, dan pemulihan.

## Deploy ke Railway (ringkas)

1. Buat repository GitHub dari isi folder ini, misalnya `n8n-railway`.
2. Di Railway, buat project baru atau pilih project yang memang ingin dipakai.
3. Tambahkan service dari GitHub repo ini, branch `main`.
4. Tambahkan service database **PostgreSQL** di project yang sama. Sebaiknya gunakan nama service `Postgres` agar reference variables di bawah bisa langsung dipakai.
5. Buka service n8n → **Variables**, lalu salin satu blok variabel di bagian **Variabel Railway siap salin** di bawah.
6. Ganti nilai `N8N_ENCRYPTION_KEY` dengan secret acak milik deployment Anda sebelum menjalankan n8n.
7. Buka service n8n → **Settings / Networking** → generate domain publik jika domain belum tersedia.
8. Deploy, tunggu sampai berhasil, lalu buka domain n8n dan buat akun owner.

## Variabel Railway siap salin

Tambahkan seluruh blok ini ke **service n8n → Variables**. Blok ini mengasumsikan nama service PostgreSQL adalah `Postgres` dan domain publik sudah dibuat pada service n8n.

```env
N8N_PORT=${{PORT}}
N8N_PROTOCOL=https
N8N_HOST=${{RAILWAY_PUBLIC_DOMAIN}}
WEBHOOK_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}/
N8N_EDITOR_BASE_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}/

# WAJIB: ganti dengan secret acak unik dan simpan aman.
N8N_ENCRYPTION_KEY=REPLACE_WITH_YOUR_OWN_RANDOM_SECRET

GENERIC_TIMEZONE=Asia/Jakarta
TZ=Asia/Jakarta

DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=${{Postgres.PGHOST}}
DB_POSTGRESDB_PORT=${{Postgres.PGPORT}}
DB_POSTGRESDB_DATABASE=${{Postgres.PGDATABASE}}
DB_POSTGRESDB_USER=${{Postgres.PGUSER}}
DB_POSTGRESDB_PASSWORD=${{Postgres.PGPASSWORD}}
DB_POSTGRESDB_SCHEMA=public

N8N_DIAGNOSTICS_ENABLED=false
N8N_PERSONALIZATION_ENABLED=false
N8N_VERSION_NOTIFICATIONS_ENABLED=false
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=336
```

**Sebelum deploy, perhatikan:**

- Ganti `REPLACE_WITH_YOUR_OWN_RANDOM_SECRET` dengan secret acak kuat, misalnya hasil perintah `openssl rand -hex 32`. Jangan gunakan contoh itu apa adanya dan jangan commit secret ke GitHub.
- Jika nama service PostgreSQL bukan `Postgres`, ubah `Postgres` pada empat reference variables menjadi nama service database yang benar. Pastikan nama variabel (`PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`) memang tersedia di service PostgreSQL Railway Anda.
- Generate domain publik untuk service n8n sebelum mengandalkan `RAILWAY_PUBLIC_DOMAIN`. Jika Railway belum menyediakan domain tersebut, buat domain lewat **Settings → Networking → Generate Domain**, lalu redeploy.
- Jangan mengganti `N8N_ENCRYPTION_KEY` setelah credential n8n disimpan; perubahan key dapat membuat credential lama tidak dapat didekripsi.
- Jangan menaruh password, API key, atau secret sungguhan dalam file repository. Simpan semuanya di Railway Variables.

## Arsitektur yang direkomendasikan

`Browser → Railway public domain → n8n service → PostgreSQL`

Gunakan PostgreSQL Railway untuk database workflow dan credential metadata. Tambahkan persistent volume ke `/home/node/.n8n` bila mengikuti rekomendasi n8n/Railway untuk penyimpanan lokal tambahan. PostgreSQL tidak menggantikan kebutuhan backup file binary jika workflow menyimpan binary di filesystem.

## Variabel penting

Atur di Railway Variables, bukan di GitHub:

- `N8N_HOST` = domain Railway yang diberikan untuk service n8n, tanpa `https://`
- `N8N_PROTOCOL` = `https`
- `WEBHOOK_URL` = URL publik lengkap, contoh `https://nama-service.up.railway.app/`
- `N8N_EDITOR_BASE_URL` = URL publik lengkap yang sama
- `N8N_ENCRYPTION_KEY` = secret acak panjang dan permanen
- `DB_TYPE` = `postgresdb`
- `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_PORT`, `DB_POSTGRESDB_DATABASE`, `DB_POSTGRESDB_USER`, `DB_POSTGRESDB_PASSWORD` = nilai dari service PostgreSQL Railway
- `GENERIC_TIMEZONE` = `Asia/Jakarta`
- `TZ` = `Asia/Jakarta`

Jangan menyalin literal contoh dari `.env.example` ke produksi. Ambil kredensial database dari Railway PostgreSQL Variables/Connect panel.

## Upgrade

Image n8n dipasang dengan tag `latest` agar contoh sederhana tetap mudah diikuti. Untuk produksi, sebaiknya pin ke versi n8n tertentu yang sudah diuji, lalu lakukan upgrade terencana setelah backup. Baca changelog resmi sebelum upgrade.

## Dokumentasi

- Setup Railway: [`docs/RAILWAY_SETUP.md`](docs/RAILWAY_SETUP.md)
- Keamanan dan backup: [`docs/SECURITY.md`](docs/SECURITY.md)
- Dokumentasi n8n: https://docs.n8n.io/
- Railway: https://docs.railway.com/

## Lisensi

Starter configuration ini disediakan apa adanya. n8n memiliki lisensi dan ketentuan tersendiri; periksa dokumentasi resmi n8n sebelum penggunaan komersial.
