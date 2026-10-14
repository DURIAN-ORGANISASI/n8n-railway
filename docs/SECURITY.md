# Keamanan, backup, dan pemulihan

## Secrets

- Simpan API key, OAuth secret, database password, dan `N8N_ENCRYPTION_KEY` di Railway Variables atau secret manager.
- Jangan commit `.env` berisi secret.
- Batasi akses collaborator Railway dan GitHub.
- Rotasi token jika pernah terpublikasi, dan perbarui token di sistem yang menggunakannya.
- Gunakan HTTPS domain Railway untuk akses editor dan webhook.

## Akses editor

- Aktifkan owner account dan gunakan password kuat.
- Jangan membagikan URL editor beserta credential.
- Hindari mengekspos service internal/database secara publik.
- Tinjau community nodes sebelum memasang; node pihak ketiga dapat menjalankan kode.

## Backup

Rencanakan backup terjadwal untuk:
1. PostgreSQL database n8n.
2. Volume `/home/node/.n8n` jika menyimpan binary/file lokal atau konfigurasi penting.
3. `N8N_ENCRYPTION_KEY` secara terpisah dan aman.

Backup database tanpa encryption key yang benar dapat membuat credential tersimpan tidak dapat dipulihkan. Backup file saja tidak menggantikan backup PostgreSQL. Uji restore di lingkungan terpisah secara berkala.

## Pemulihan

1. Siapkan PostgreSQL target.
2. Pulihkan backup database yang sesuai.
3. Pasang file/binary backup jika digunakan.
4. Set `N8N_ENCRYPTION_KEY` yang sama.
5. Set URL/host sesuai domain target.
6. Jalankan n8n dan verifikasi workflow serta credential.

Jangan menghapus service, database, atau volume lama sampai restore berhasil diverifikasi.
