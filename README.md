# ShopEasy - E-commerce Application

Aplikasi e-commerce sederhana menggunakan Flask, Supabase, dan Xendit sebagai payment gateway. Aplikasi ini mengikuti alur pembelian profesional seperti Tokopedia/Shopee: checkout → order pending → bayar → webhook → update status paid.

# Deployed

link = https://ecommerce-flask-ewnu.onrender.com

## Fitur Utama

- **Produk**: Tampilan dan pencarian produk lengkap dengan filter
- **Keranjang Belanja**: Tambah/hapus produk ke keranjang
- **Otentikasi**: Login/register pengguna dengan sistem otentikasi Supabase
- **Alamat Pengiriman**: Manajemen alamat pengiriman untuk pengguna
- **Checkout**: Proses pembuatan order dengan pemilihan alamat
- **Pembayaran Xendit**: Integrasi pembayaran full-service dengan berbagai metode (VA, e-wallet, kartu kredit, dll.)
- **Webhook Handler**: Otomatisasi update status pembayaran setelah pembayaran sukses
- **Status Order**: Tampilan status pembayaran real-time (pending/paid/delivered)
- **Riwayat Order**: Tampilan daftar dan detail order pengguna

## Prasyarat

- Python 3.8+
- Node.js (untuk ngrok jika test webhook)
- Akun Supabase
- Akun Xendit

## Instalasi

1. Clone repository ini:
```bash
git clone <repository_url>
cd ecommerce-flask-supabase
```

2. Buat virtual environment dan instal dependensi:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

3. Buat file `.env` berdasarkan `.env.example`:
```bash
cp .env.example .env
```

4. Isi variabel lingkungan:
- `SUPABASE_URL`: URL proyek Supabase Anda
- `SUPABASE_ANON_KEY`: Anonymous key dari Supabase
- `SUPABASE_SERVICE_ROLE_KEY`: Service role key dari Supabase (untuk webhook)
- `XENDIT_SECRET_KEY`: Secret key dari Xendit
- `WEBHOOK_TOKEN`: Token verifikasi webhook dari dashboard Xendit (opsional)

## Konfigurasi Database

Jalankan skrip SQL dari `sql/ddl_rls.sql` di database Supabase Anda untuk membuat tabel dan RLS (Row Level Security).

## Menjalankan Aplikasi

```bash
python wsgi.py
```

Aplikasi akan berjalan di `http://127.0.0.1:8000`

## Testing Webhook

Karena Xendit tidak mendukung webhook untuk localhost, Anda perlu menggunakan ngrok:

1. Install ngrok: `npm install -g ngrok`
2. Jalankan ngrok: `ngrok http 8000`
3. Ambil URL public dari ngrok dan tambahkan `/api/webhook` sebagai endpoint webhook di dashboard Xendit
4. Pastikan `WEBHOOK_TOKEN` di `.env` sama dengan yang diatur di dashboard Xendit

## Struktur Proyek

```
├── app/                    # Kode aplikasi utama
│   ├── __init__.py        # Inisialisasi Flask app
│   ├── config.py          # Konfigurasi aplikasi
│   ├── extensions.py      # Ekstensi Flask
│   ├── routes/            # Route handlers
│   │   ├── __init__.py    # Registrasi semua blueprint
│   │   ├── main.py        # Route untuk halaman HTML
│   │   ├── products.py    # Route untuk produk
│   │   ├── cart.py        # Route untuk keranjang
│   │   ├── orders.py      # Route untuk order dan pembayaran
│   │   ├── auth.py        # Route untuk otentikasi
│   │   ├── admin.py       # Route untuk admin
│   │   └── address.py     # Route untuk alamat
│   ├── services/          # Business logic
│   │   ├── products_svc.py # Logika produk
│   │   └── orders_svc.py  # Logika order dan pembayaran
│   └── utils/             # Utility functions
│       ├── security.py    # Fungsi keamanan
│       └── validators.py  # Fungsi validasi
├── static/                # CSS, JS, gambar
├── templates/             # Template HTML
├── sql/                   # Skema database
├── requirements.txt       # Dependensi Python
├── .env.example           # Contoh file environment
├── .env                   # File environment (jangan di-commit)
├── wsgi.py               # Entry point aplikasi
├── UPDATE.md             # Dokumentasi pengembangan fitur pembayaran
└── README.md             # Dokumentasi ini
```

## Arsitektur Aplikasi

Aplikasi ini menggunakan arsitektur SPA (Single Page Application) sederhana di mana:

- Backend (Python Flask) menyediakan API endpoints
- Frontend (JavaScript SPA) mengelola tampilan halaman
- Supabase digunakan sebagai database dan otentikasi
- Xendit sebagai payment gateway

## Alur Pembayaran (Xendit Integration)

1. Pengguna checkout dari cart → order dibuat dengan status `pending`
2. Di halaman detail order, tombol "Bayar Sekarang" muncul
3. Klik tombol → buat invoice di Xendit → redirect ke halaman pembayaran Xendit
4. Pengguna selesai membayar di Xendit
5. Xendit kirim webhook ke `/api/webhook` dengan status pembayaran
6. Webhook handler update status order ke `paid` menggunakan service role key
7. Pengguna bisa melihat status pembayaran terbaru di halaman detail order

## Alur Pembayaran (Xendit Integration)

1. Pengguna checkout dari keranjang → order dibuat dengan status `pending`
2. Di halaman detail order, tombol "Bayar Sekarang" muncul
3. Klik tombol → buat invoice di Xendit → redirect ke halaman pembayaran Xendit
4. Pengguna selesai membayar di Xendit
5. Xendit kirim webhook ke `/api/webhook` dengan status pembayaran
6. Webhook handler update status order ke `paid` menggunakan service role key
7. Pengguna bisa melihat status pembayaran terbaru di halaman detail order

## Kontribusi

Silakan buat pull request untuk kontribusi perbaikan.
