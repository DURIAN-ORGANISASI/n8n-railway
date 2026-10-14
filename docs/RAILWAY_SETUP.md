# Panduan lengkap deploy n8n ke Railway

## 1. Siapkan repository GitHub

1. Buat repository baru bernama `n8n-railway`.
2. Upload seluruh isi starter ini ke root repository, sehingga `Dockerfile` dan `railway.json` berada langsung di root.
3. Pastikan repository tidak berisi `.env` asli, token API, credential, atau data workflow.
4. Gunakan branch `main`.

## 2. Buat project dan service

1. Masuk ke Railway.
2. Buat project baru (atau pilih project khusus yang memang ingin dipakai).
3. Tambahkan service dari GitHub repository `owner/n8n-railway`, branch `main`.
4. Railway akan membaca `railway.json` dan membangun `Dockerfile`.
5. Tambahkan service PostgreSQL resmi dari menu **New → Database → PostgreSQL** di project yang sama.

Jangan men-deploy database baru kalau project Anda sudah punya database yang memang ingin digunakan. Jangan menimpa atau menghapus service lama tanpa memastikan dampaknya.

## 3. Hubungkan PostgreSQL

Di service PostgreSQL, buka Variables/Connect dan salin nilai koneksi internal Railway. Gunakan hostname internal/private untuk koneksi antarlayanan dalam project yang sama, bukan public TCP proxy jika tidak dibutuhkan.

Set variabel berikut pada service n8n. Nama variabel referensi PostgreSQL Railway dapat berbeda tergantung UI; petakan nilai yang tersedia:

| Variabel n8n | Isi |
|---|---|
| `DB_TYPE` | `postgresdb` |
| `DB_POSTGRESDB_HOST` | hostname internal PostgreSQL |
| `DB_POSTGRESDB_PORT` | port PostgreSQL, biasanya `5432` |
| `DB_POSTGRESDB_DATABASE` | nama database |
| `DB_POSTGRESDB_USER` | username database |
| `DB_POSTGRESDB_PASSWORD` | password database |

Jangan menaruh password dalam file repository. Pastikan host, database, username, dan password berasal dari service PostgreSQL yang benar.

## 4. Atur variabel service n8n

Tambahkan pada **n8n → Variables**:

| Variabel | Nilai |
|---|---|
| `N8N_PORT` | `${{PORT}}` jika Railway menyediakan variable `PORT`; jika platform tidak mendukung reference itu, gunakan `5678` |
| `N8N_PROTOCOL` | `https` |
| `N8N_HOST` | hostname domain publik tanpa skema, misalnya `n8n-production.up.railway.app` |
| `WEBHOOK_URL` | URL publik lengkap dan diakhiri `/`, misalnya `https://n8n-production.up.railway.app/` |
| `N8N_EDITOR_BASE_URL` | URL publik lengkap, misalnya `https://n8n-production.up.railway.app/` |
| `N8N_ENCRYPTION_KEY` | secret acak kuat dan stabil |
| `GENERIC_TIMEZONE` | `Asia/Jakarta` |
| `TZ` | `Asia/Jakarta` |
| `N8N_DIAGNOSTICS_ENABLED` | `false` |
| `N8N_PERSONALIZATION_ENABLED` | `false` |
| `N8N_VERSION_NOTIFICATIONS_ENABLED` | `false` |
| `EXECUTIONS_DATA_PRUNE` | `true` |
| `EXECUTIONS_DATA_MAX_AGE` | `336` |

### Membuat encryption key

Buat nilai acak di komputer sendiri, misalnya:

```bash
openssl rand -hex 32
```

Salin hasilnya langsung ke Railway Variables. Jangan mengirimkan key itu di chat atau commit ke GitHub. **Jangan mengganti key setelah credential disimpan**, kecuali Anda paham proses migrasi/dekripsi credential; key yang berubah dapat membuat credential tersimpan tidak bisa didekripsi.

`N8N_HOST` harus sama dengan hostname domain yang benar-benar dibuat Railway. Perbarui `WEBHOOK_URL` dan `N8N_EDITOR_BASE_URL` jika domain berubah.

## 5. Domain dan port

1. Buka service n8n → **Settings / Networking**.
2. Generate domain Railway.
3. Masukkan hostname domain ke `N8N_HOST`.
4. Set `WEBHOOK_URL` dan `N8N_EDITOR_BASE_URL` ke URL HTTPS yang sama.
5. Pastikan port aplikasi cocok dengan port yang disediakan Railway dan `N8N_PORT`.
6. Redeploy setelah mengubah variables.

Jangan membuat domain publik untuk PostgreSQL. Hanya service n8n yang perlu domain publik kecuali ada kebutuhan khusus.

## 6. Persistent storage

Database PostgreSQL menyimpan workflow, user, dan metadata credential; persistent storage tetap penting untuk data lokal/binary yang disimpan di filesystem.

Jika menggunakan volume Railway untuk n8n, tambahkan volume pada service n8n dengan mount path:

`/home/node/.n8n`

Jangan mount volume ke path yang salah. Volume yang terpasang pada path baru atau berbeda tidak otomatis memindahkan data lama. Periksa panduan Railway dan n8n sebelum migrasi data. Buat backup sebelum mengubah mount path.

## 7. Verifikasi deployment

- Status deployment harus `SUCCESS`.
- Periksa runtime logs untuk error koneksi PostgreSQL, encryption key, atau port.
- Buka domain HTTPS dan selesaikan pembuatan owner account.
- Uji workflow sederhana secara manual.
- Buat webhook test dan production, lalu pastikan URL callback menggunakan domain HTTPS Railway.
- Uji ulang setelah restart service untuk memastikan data tetap ada.

## 8. Troubleshooting

### `connection refused` atau gagal koneksi PostgreSQL
- Pastikan service PostgreSQL sudah aktif.
- Pastikan host internal, port, database, user, dan password tepat.
- Jangan gunakan nama service sebagai host kecuali memang cocok dengan hostname internal yang ditampilkan Railway.

### Webhook masih memakai localhost atau URL salah
- Perbaiki `WEBHOOK_URL` dan `N8N_EDITOR_BASE_URL`.
- Pastikan domain `N8N_HOST` benar.
- Redeploy setelah perubahan.

### Aplikasi tidak bisa diakses
- Pastikan domain di-generate pada service n8n, bukan PostgreSQL.
- Periksa logs dan kecocokan port `N8N_PORT` dengan `PORT` yang disediakan Railway.
- Pastikan deployment terbaru benar-benar `SUCCESS`.

### Credential tidak bisa dibaca setelah redeploy
- Pastikan `N8N_ENCRYPTION_KEY` sama dengan key saat credential dibuat.
- Jangan membuat key baru setiap deployment.

### Data hilang setelah redeploy
- Pastikan n8n memakai PostgreSQL yang sama.
- Pastikan volume `/home/node/.n8n` masih terpasang jika dibutuhkan.
- Jangan menghapus volume/database sebelum backup dan verifikasi.

## 9. Catatan biaya dan kapasitas

Railway dan penggunaan n8n dapat menimbulkan biaya sesuai plan, resource, dan durasi berjalan. Pantau usage. Mulai dengan resource kecil lalu tingkatkan berdasarkan metrik dan beban workflow. Worker mode/queue mode merupakan arsitektur tambahan; jangan menambah Redis/worker tanpa memahami kebutuhan dan konfigurasi resmi n8n.

## 10. Upgrade terencana

Untuk produksi, gunakan versi n8n yang dipin dan diuji, bukan mengikuti `latest` tanpa kontrol. Sebelum upgrade:

1. Backup database dan file/binary yang relevan.
2. Baca release notes n8n.
3. Upgrade di waktu pemeliharaan.
4. Pantau logs dan uji workflow penting.
5. Siapkan prosedur rollback yang sesuai dengan versi database dan n8n.
