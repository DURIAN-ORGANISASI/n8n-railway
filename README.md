<div align="center">

# 🚀 n8n Railway Starter

**Panduan ringkas deploy n8n + PostgreSQL di Railway.**

[Mulai instalasi](#instalasi) · [Variabel n8n](./n8n-service-variables.example.txt) · [Troubleshooting](#troubleshooting)

</div>

---

Repo ini berisi template untuk menjalankan **n8n** di Railway dengan **PostgreSQL** dan penyimpanan persisten.

> **Penting:** Buat PostgreSQL lebih dulu. Pasang volume pada service n8n. Tempel variabel aplikasi hanya ke service n8n—bukan ke PostgreSQL. Jangan pernah menyimpan password atau encryption key asli di GitHub.

## Instalasi

### Tahap 1 — Buat project Railway

1. Login ke [Railway](https://railway.com/) dan buat project.
2. Gunakan project dan environment yang sama untuk PostgreSQL dan n8n.

### Tahap 2 — Tambahkan PostgreSQL terlebih dahulu

1. Klik **New → Database → PostgreSQL**.
2. Tunggu sampai status database sehat/online.
3. Biarkan nama service **Postgres** agar cocok dengan referensi variabel di file contoh. Jika namanya berbeda, sesuaikan referensinya nanti.
4. Railway membuat variabel koneksi database secara otomatis; **jangan membuat atau menempelkan variabel database secara manual**.

### Tahap 3 — Siapkan repo GitHub

1. Fork repo ini atau unggah isinya ke repository GitHub milikmu.
2. Pastikan `Dockerfile`, `railway.json`, dan README berada di root repo.
3. Jangan unggah file berisi secret.

### Tahap 4 — Deploy service n8n dari GitHub

1. Kembali ke project Railway yang sama.
2. Klik **New → GitHub Repo**, lalu pilih repo n8n ini.
3. Biarkan **Root Directory** kosong.
4. Tunggu service dibuat. Pengaturan variabel dan penyimpanan ada di langkah berikutnya.

### Tahap 5 — Buat domain dan volume

Pada **service n8n**:

1. Buka **Settings → Networking → Generate Domain**.
2. Buka **Volumes**, tambahkan volume dengan mount path persis:
   `/home/node/.n8n`
3. Jangan hapus volume saat redeploy. Volume bukan pengganti backup PostgreSQL.

### Tahap 6 — Atur variabel n8n

1. Buat encryption key di komputer:
   - **Windows PowerShell:** `.\scripts\generate-key.ps1`
   - **Linux/macOS:** `sh scripts/generate-key.sh`
2. Buka file [`n8n-service-variables.example.txt`](./n8n-service-variables.example.txt), lalu salin seluruh isinya ke **service n8n → Variables → Raw Editor**.
3. Ganti `REPLACE_WITH_YOUR_64_CHARACTER_HEX_KEY` dengan key yang dibuat tadi.
4. Pastikan namespace `Postgres` di referensi variabel sama persis dengan nama service database.
5. Simpan key di tempat aman. Jangan mengganti key pada instance yang sudah menyimpan kredensial.

**Catatan volume:** Template menggunakan `RAILWAY_RUN_UID=0` untuk mengatasi masalah izin akses volume pada setup ini. Ini membuat proses berjalan sebagai root, sehingga ada trade-off keamanan.

### Tahap 7 — Deploy dan uji

1. Simpan variabel dan redeploy service n8n.
2. Buka **Deployments → View Logs**. Pastikan deployment sukses dan n8n siap menerima koneksi.
3. Buka domain Railway, lalu buat akun owner n8n.
4. Coba jalankan workflow sederhana sebelum memasang credential atau workflow produksi.

## Troubleshooting

- **Database tidak tersambung:** pastikan PostgreSQL sehat, keduanya di project/environment yang sama, dan nama service cocok dengan referensi variabel.
- **`EACCES: permission denied`:** pastikan volume terpasang di `/home/node/.n8n` dan variabel `RAILWAY_RUN_UID=0` disetel.
- **Domain tidak merespons:** periksa runtime logs, domain, variabel, dan status deployment.
- **Kredensial tidak bisa dibuka:** pastikan menggunakan `N8N_ENCRYPTION_KEY` yang sama seperti saat kredensial dibuat.

## Uji lokal (opsional)

Untuk uji lokal, dibutuhkan Docker. Salin `.env.example` menjadi `.env`, isi nilainya, lalu jalankan:

```bash
docker compose --env-file .env -f docker-compose.local.yml up -d --build
```

Buka `http://localhost:5678`. Jangan unggah file `.env` ke GitHub.

## Backup dan lisensi

Backup database PostgreSQL dan simpan `N8N_ENCRYPTION_KEY` secara terpisah sebelum upgrade. Template ini memakai lisensi MIT; n8n memiliki lisensinya sendiri. Periksa ketentuan lisensi n8n jika digunakan untuk menyediakan layanan ter-host kepada pihak lain.

## Referensi

- [Panduan n8n di Railway](https://docs.railway.com/guides/n8n)
- [Variabel Railway](https://docs.railway.com/variables)
- [Konfigurasi environment variable n8n](https://docs.n8n.io/hosting/configuration/environment-variables/)
