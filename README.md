# Rak Baca (Python / Flask) — Website Pemesanan Buku Online

Versi **backend Python** dari final project **Pengembangan Website Pemesanan Buku Berbasis Online**
(Nizamuddin Hilmi Hasan — 462025611080). Halaman dirender di server menggunakan **Flask + Jinja2**,
dengan seluruh logika bisnis ditulis sebagai kelas-kelas Python murni.

## Struktur folder

```
rak-baca-flask/
├── app.py                 # routing Flask & logika utama
├── models.py               # kelas-kelas OOP (Pengguna, Buku, MetodePembayaran, Notifikasi, dst)
├── data.py                  # data awal katalog buku (in-memory)
├── requirements.txt
├── static/
│   └── css/style.css
└── templates/
    ├── base.html            # layout dasar (header, footer)
    ├── index.html            # katalog buku
    ├── cart.html              # keranjang belanja
    ├── checkout_select.html  # pilih metode pembayaran
    ├── checkout.html          # hasil pembayaran + kirim notifikasi
    └── admin.html              # panel admin (kelola stok & tambah buku)
```

## Cara menjalankan di VS Code

**1. Pastikan Python sudah terpasang** (cek dengan menjalankan `python --version` atau `python3 --version` di terminal).

**2. Buka folder proyek di VS Code**
`File → Open Folder...` → pilih folder `rak-baca-flask`.

**3. (Disarankan) Buat virtual environment**
Buka terminal di VS Code (`Ctrl+` `` ` ``), lalu jalankan:

```bash
python -m venv venv
```

Aktifkan:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

**4. Install dependency**

```bash
pip install -r requirements.txt
```

**5. Jalankan aplikasinya**

```bash
python app.py
```

Terminal akan menampilkan alamat seperti `http://127.0.0.1:5000` — buka alamat itu di browser.

Setiap kali kamu mengubah kode dan menyimpan file, jalankan ulang `python app.py`
(atau server akan otomatis reload karena `debug=True` di `app.py`).

## Pemetaan konsep OOP ke kode (`models.py`)

| Pilar OOP | Implementasi | Lokasi |
|---|---|---|
| **Encapsulation** | Atribut `Buku` diberi awalan `__` (private, name-mangling di Python). Stok hanya bisa diubah lewat `set_stok()` / `kurangi_stok()`. | `class Buku` |
| **Inheritance** | `Admin` dan `Pembeli` mewarisi `Pengguna` (id, nama, email). | `class Pengguna`, `class Admin`, `class Pembeli` |
| **Polymorphism** | `TransferBank` dan `EWallet` meng-*override* `proses_pembayaran()` dari `MetodePembayaran`; `NotifikasiEmail` dan `NotifikasiWhatsApp` meng-*override* `kirim()` dari `Notifikasi`. Dipanggil di `app.py` tanpa app.py tahu detail implementasinya. | `class TransferBank`, `class EWallet`, `class NotifikasiEmail`, `class NotifikasiWhatsApp` |
| **Abstraction** | `MetodePembayaran` dan `Notifikasi` dibuat dengan `abc.ABC` + `@abstractmethod` — tidak bisa diinstansiasi langsung, memaksa subclass menyediakan implementasi nyata. | `class MetodePembayaran(ABC)`, `class Notifikasi(ABC)` |

## Fitur yang sudah berjalan

- Katalog buku dengan filter kategori (query string) dan pencarian judul/penulis
- Keranjang belanja berbasis session (tambah, ubah jumlah)
- Checkout dua metode pembayaran (Transfer Bank / E-Wallet) — hasil berbeda sesuai kelas yang dipanggil
- Simulasi notifikasi konfirmasi (email / WhatsApp)
- Panel admin: lihat & ubah stok, tambah buku baru ke katalog

## Catatan penting

- **Data bersifat sementara** — semua data buku disimpan di memori Python (`data.py`). Data akan
  kembali ke kondisi awal setiap kali server (`python app.py`) di-restart.
- Belum ada database sungguhan, autentikasi login, payment gateway asli, atau pengiriman email/WA
  yang benar-benar terkirim — semuanya masih simulasi, sesuai cakupan proposal final project ini.

## Pengembangan lanjutan yang disarankan

- Ganti `data.py` dengan database (mis. SQLite via **SQLAlchemy**) agar data permanen.
- Tambahkan autentikasi (mis. **Flask-Login**) untuk membedakan sesi Admin vs Pembeli.
- Integrasikan payment gateway asli (mis. Midtrans/Xendit) di dalam method `proses_pembayaran()`.
- Integrasikan pengiriman email sungguhan (mis. **Flask-Mail**) dan WhatsApp API (mis. Fonnte) di
  dalam method `kirim()`.
