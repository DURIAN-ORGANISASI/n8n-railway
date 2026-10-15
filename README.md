# n8n Railway Starter — PostgreSQL terlebih dahulu

Template komunitas untuk memasang satu instance **n8n** di Railway menggunakan **PostgreSQL Railway** dan penyimpanan persisten. Repo ini berisi konfigurasi deployment dan tutorial; bukan fork atau salinan source code n8n.

> **Urutan wajib:** buat service PostgreSQL di Railway terlebih dahulu, tunggu sampai database sehat, baru deploy service n8n dari repo ini. Repo ini tidak membuat service database di Railway secara otomatis.

> **Tentang variabel:** Railway otomatis menyediakan variabel database pada service PostgreSQL. Jangan membuat ulang variabel database di service PostgreSQL dan jangan menempelkan konfigurasi n8n di service database. File `n8n-service-variables.example.txt` hanya untuk service **n8n**; di dalamnya ada referensi ke variabel yang sudah disediakan oleh service PostgreSQL.

## Arsitektur

- **Postgres** — service database yang kamu tambahkan langsung di Railway. Menyimpan workflow, kredensial n8n yang terenkripsi, dan execution data.
- **n8n** — service dari repo GitHub ini. Terhubung ke Postgres melalui Railway Reference Variables.
- **Railway Volume** — dipasang pada `/home/node/.n8n` di service n8n untuk data lokal penting, termasuk file setting dan key yang digunakan oleh instance.
- **Tidak memakai Redis / queue mode** — setup ini sengaja dibuat sederhana untuk bot dan automasi pribadi/kecil. Jangan mengaktifkan queue mode kecuali menambahkan Redis dan worker sesuai dokumentasi n8n.

## Yang dibutuhkan

1. Akun GitHub.
2. Akun/proyek Railway dengan resource dan billing yang cukup untuk service n8n, PostgreSQL, dan volume.
3. Repo GitHub berisi file template ini.
4. Satu service PostgreSQL dan satu service n8n dalam **project serta environment Railway yang sama**.
5. Domain publik Railway untuk n8n dan `N8N_ENCRYPTION_KEY` unik yang disimpan aman.

---

# Tutorial pemasangan di Railway

## Tahap 1 — Buat project Railway

1. Login ke [Railway](https://railway.com/).
2. Buat **New Project**.
3. Gunakan satu environment yang sama untuk service database dan n8n (biasanya `production`).

## Tahap 2 — Tambahkan PostgreSQL terlebih dahulu (wajib)

1. Di canvas project Railway klik **New** atau tombol `+`.
2. Pilih **Database → PostgreSQL**.
3. Tunggu sampai service PostgreSQL selesai deploy dan berstatus **Healthy/Online**.
4. Pastikan nama service database adalah **`Postgres`** (huruf `P` besar), karena file variabel n8n mengacu pada nama tersebut. Bila Railway memberinya nama lain, ubah bagian nama service di referensi dalam file variabel n8n nanti.
5. Buka service **Postgres → Variables** hanya untuk memastikan variabel database bawaan Railway sudah tersedia. Railway membuatnya otomatis; **jangan membuat atau menempelkan variabel database secara manual**.
6. Biarkan PostgreSQL berada pada project dan environment yang sama dengan n8n. Untuk koneksi internal antarservice, jangan gunakan public TCP address jika tidak diperlukan.

Variabel bawaan seperti host, port, nama database, username, dan password dikelola oleh Railway di service PostgreSQL. n8n akan merujuk variabel tersebut dari servicenya sendiri pada tahap 6; n8n tidak akan membuat atau mengubah variabel sumber di PostgreSQL.

## Tahap 3 — Unggah repo ke GitHub

1. Unduh ZIP repo ini dan ekstrak di komputer.
2. Buat repository baru, misalnya `n8n-railway-starter`.
3. Unggah **isi folder** ke root repository. Pastikan `Dockerfile`, `railway.json`, dan `README.md` langsung berada di root, bukan di folder bertingkat lain.
4. Jangan unggah file `.env` yang berisi secret. `.env.example` hanya untuk uji lokal dan berisi placeholder.
5. Untuk repo publik, jangan pernah menaruh token Telegram, API key, password, atau encryption key sungguhan di GitHub.

## Tahap 4 — Deploy service n8n dari GitHub

1. Kembali ke **project Railway yang sama** dengan PostgreSQL.
2. Klik **New → GitHub Repo**.
3. Hubungkan akun GitHub apabila diminta, lalu pilih repo `n8n-railway-starter`.
4. Pastikan Root Directory kosong (root repo), sehingga Railway menemukan `Dockerfile` dan `railway.json`.
5. Tunggu proses build. Jika n8n sempat gagal start karena variabel/domain belum lengkap, lanjutkan pengaturan di bawah lalu redeploy.

Repo menggunakan image n8n resmi dengan versi dipatok agar versi tidak berubah diam-diam. Sebelum upgrade versi di `Dockerfile`, baca release notes dan lakukan backup database terlebih dahulu.

## Tahap 5 — Buat domain publik dan volume untuk n8n

Lakukan ini pada **service n8n**, bukan pada Postgres.

### Buat domain

1. Buka service n8n → **Settings → Networking**.
2. Klik **Generate Domain**.
3. Catat domain Railway berakhiran `.up.railway.app`. Jangan tulis `https://` saat menyalin domainnya ke `N8N_HOST`; file variabel akan menambahkan protokol untuk URL lainnya.

### Buat volume

1. Buka service n8n → **Volumes**.
2. Tambahkan volume dengan mount path tepat **`/home/node/.n8n`**.
3. Pilih ukuran sesuai penggunaan. Mulai dari 1 GB untuk penggunaan ringan dan tambah bila workflow menyimpan file/binary besar.
4. Jangan hapus volume saat redeploy. Volume membantu menyimpan data lokal tetapi bukan pengganti backup database.

## Tahap 6 — Atur variabel hanya pada service n8n

1. Buka folder repo lokal dan jalankan pembuat encryption key:

   **Windows PowerShell**

   ```powershell
   .\scripts\generate-key.ps1
   ```

   **Linux/macOS**

   ```bash
   sh scripts/generate-key.sh
   ```

2. Simpan hasil key di pengelola password atau tempat aman. Jangan unggah key ke repo publik.
3. Buka file **`n8n-service-variables.example.txt`** di repo.
4. Salin seluruh isi file tersebut ke **service n8n → Variables → Raw Editor** di Railway.
5. Ganti nilai placeholder encryption key dengan key yang baru dibuat.
6. Pastikan `Postgres` pada referensi variabel sesuai nama service database pada canvas Railway. Contohnya `${{Postgres.PGHOST}}` mengambil nilai `PGHOST` dari service `Postgres`.
7. Simpan/stage perubahan lalu tekan **Deploy** / redeploy service n8n.

**Jangan tempel isi `n8n-service-variables.example.txt` ke service Postgres.** File tersebut berisi konfigurasi aplikasi n8n dan referensi untuk membaca nilai database yang sudah disediakan Railway.

Jika Railway tidak dapat menyelesaikan referensi `${{Postgres...}}`, periksa nama service, project, dan environment. Jangan mengganti referensi itu dengan kata sandi atau host tebakan. Pilih referensi melalui autocomplete Railway bila tersedia.

## Tahap 7 — Verifikasi deployment

1. Buka **Deployments → View Logs** pada service n8n.
2. Tunggu sampai deployment berstatus **Successful/Healthy**.
3. Buka domain publik n8n yang dibuat di Tahap 5.
4. Pada instalasi baru, selesaikan formulir pembuatan owner. Lakukan sendiri sebelum membagikan URL kepada orang lain.
5. Buat workflow sederhana: **Manual Trigger → Edit Fields** (atau node sederhana lain), jalankan sekali, dan pastikan eksekusi sukses.
6. Baru setelah editor dan workflow sederhana berfungsi, pasang credential dan workflow Telegram/API.
7. Pada node trigger/webhook, pastikan URL yang ditampilkan menggunakan domain HTTPS Railway, bukan `localhost`.

## Checklist sebelum menyatakan selesai

- [ ] Service PostgreSQL dibuat lebih dahulu dan berstatus sehat.
- [ ] Service Postgres dan n8n berada di project dan environment yang sama.
- [ ] Nama service database cocok dengan referensi di file variabel n8n.
- [ ] Volume n8n terpasang di `/home/node/.n8n`.
- [ ] Domain publik n8n sudah dibuat.
- [ ] Variabel `n8n-service-variables.example.txt` ditempel hanya ke service n8n.
- [ ] Encryption key placeholder sudah diganti, dan key disimpan dengan aman.
- [ ] Service n8n berhasil deploy dan log tidak menunjukkan error koneksi database.
- [ ] Workflow uji berhasil dijalankan.

---

## Uji lokal (opsional)

Uji lokal tidak dibutuhkan untuk deploy Railway. Jika ingin mencobanya, diperlukan Docker Desktop/Engine dan Docker Compose.

1. Salin `.env.example` menjadi `.env`.
2. Ganti nilai `POSTGRES_PASSWORD` dengan password panjang dan acak.
3. Generate key memakai salah satu skrip pada folder `scripts`, lalu masukkan hasilnya ke `N8N_ENCRYPTION_KEY` di `.env`.
4. Jalankan:

   ```bash
   docker compose --env-file .env -f docker-compose.local.yml config
   docker compose --env-file .env -f docker-compose.local.yml up -d --build
   ```

5. Buka `http://localhost:5678` dan selesaikan pembuatan owner.
6. Untuk menghentikan layanan tanpa menghapus data:

   ```bash
   docker compose --env-file .env -f docker-compose.local.yml down
   ```

Jangan gunakan `down -v` kecuali memang ingin menghapus database dan semua data volume lokal.

## Validasi file repo

Jalankan dari root repo sebelum push:

```bash
python scripts/validate-repo.py
```

GitHub Actions juga menjalankan pemeriksaan statis saat push dan pull request. Tes statis tidak bisa membuktikan apakah akun Railway, resource, domain, atau database pada akunmu benar-benar siap.

## Troubleshooting

### `ENOTFOUND`, `password authentication failed`, atau error koneksi database

- Pastikan Postgres berstatus sehat dan berada di project serta environment yang sama dengan n8n.
- Pastikan nama service database sama persis dengan nama pada referensi `${{NamaService.PGHOST}}` dan variabel lainnya.
- Pastikan variabel koneksi ditaruh pada service n8n, bukan Postgres.
- Tunggu PostgreSQL selesai start, lalu redeploy service n8n.
- Jangan menempelkan public TCP URL sebagai host internal jika kedua service berada pada satu project Railway.

### `Application failed to respond` atau health check timeout

- Periksa runtime logs pada service n8n.
- Pastikan domain telah dibuat, volume terpasang, dan variabel n8n diterapkan.
- Periksa resource/memori project Railway.

### URL webhook Telegram salah atau masih `localhost`

- Pastikan `WEBHOOK_URL` dan `N8N_EDITOR_BASE_URL` merujuk domain Railway HTTPS.
- Pastikan pengaturan domain dan variabel sudah di-deploy setelah perubahan.
- Buka ulang node trigger dan salin URL yang ditampilkan n8n.

### Kredensial tidak dapat didekripsi setelah redeploy

- Pertahankan `N8N_ENCRYPTION_KEY` yang sama setelah menyimpan credential. Jangan buat key baru lalu timpa nilai lama pada instance yang sudah berisi credential.
- Simpan key di luar GitHub dan buat backup sebelum perubahan besar.
- Jika key lama hilang, pulihkan key/backup yang cocok sebelum mengubah database produksi.

### Workflow hilang setelah redeploy

- Pastikan n8n memakai Postgres dan logs mengonfirmasi koneksi sukses.
- Pastikan volume terpasang di `/home/node/.n8n`.
- Jika memindahkan instance lama dari SQLite ke PostgreSQL, gunakan prosedur migrasi/ekspor-impor terencana; mengganti variabel saja tidak memindahkan data lama.

## Backup dan upgrade

- Buat backup PostgreSQL dan simpan `N8N_ENCRYPTION_KEY` secara terpisah sebelum upgrade.
- Simpan backup di luar volume yang sama.
- Upgrade versi secara sengaja, baca release notes, dan uji sebelum production bila memungkinkan.
- Hindari queue mode tanpa Redis dan worker.

## Lisensi

File template, skrip, dan dokumentasi dalam repo ini memakai lisensi MIT. n8n memiliki lisensi sendiri, yaitu Sustainable Use License/fair-code; lisensi MIT pada template ini tidak mengganti lisensi n8n. Periksa syarat lisensi resmi jika hendak menawarkan n8n sebagai layanan ter-host kepada pihak lain.

## Referensi resmi

- Railway: <https://docs.railway.com/guides/n8n>
- Railway PostgreSQL: <https://docs.railway.com/databases/postgresql>
- Railway variables: <https://docs.railway.com/variables>
- Railway reference variables: <https://docs.railway.com/variables/reference>
- n8n environment variables: <https://docs.n8n.io/hosting/configuration/environment-variables/>
- n8n database configuration: <https://docs.n8n.io/hosting/configuration/environment-variables/database/>
