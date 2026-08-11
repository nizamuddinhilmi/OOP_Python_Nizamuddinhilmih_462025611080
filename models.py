"""
models.py
=========
Kelas-kelas inti yang menerapkan empat pilar OOP sesuai proposal:
Encapsulation, Inheritance, Polymorphism, Abstraction.
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------
# INHERITANCE + ENCAPSULATION: Pengguna -> Admin / Pembeli
# ---------------------------------------------------------------
class Pengguna:
    """Parent class untuk semua jenis pengguna sistem."""

    def __init__(self, id_user: int, nama: str, email: str):
        self._id_user = id_user      # underscore = protected (encapsulation)
        self._nama = nama
        self._email = email

    def get_id(self) -> int:
        return self._id_user

    def get_nama(self) -> str:
        return self._nama

    def get_email(self) -> str:
        return self._email


class Admin(Pengguna):
    """Child class: pengelola toko buku."""

    def __init__(self, id_user: int, nama: str, email: str):
        super().__init__(id_user, nama, email)
        self.role = "admin"


class Pembeli(Pengguna):
    """Child class: pelanggan yang memesan buku."""

    def __init__(self, id_user: int, nama: str, email: str):
        super().__init__(id_user, nama, email)
        self.role = "pembeli"


# ---------------------------------------------------------------
# ENCAPSULATION: Buku — stok hanya boleh berubah lewat method
# ---------------------------------------------------------------
class Buku:
    """Merepresentasikan satu judul buku di katalog."""

    def __init__(self, id_buku: int, judul: str, penulis: str,
                 kategori: str, harga: int, stok: int, kode_rak: str):
        self.__id_buku = id_buku      # double underscore = private (name mangling)
        self.__judul = judul
        self.__penulis = penulis
        self.__kategori = kategori
        self.__harga = harga
        self.__stok = stok
        self.__kode_rak = kode_rak

    # --- getter (satu-satunya cara membaca data dari luar kelas) ---
    def get_id(self) -> int:
        return self.__id_buku

    def get_judul(self) -> str:
        return self.__judul

    def get_penulis(self) -> str:
        return self.__penulis

    def get_kategori(self) -> str:
        return self.__kategori

    def get_harga(self) -> int:
        return self.__harga

    def get_stok(self) -> int:
        return self.__stok

    def get_kode_rak(self) -> str:
        return self.__kode_rak

    # --- setter / mutator (satu-satunya cara mengubah stok) ---
    def set_stok(self, jumlah_baru: int) -> None:
        self.__stok = max(0, jumlah_baru)

    def kurangi_stok(self, jumlah: int = 1) -> bool:
        """Mengurangi stok saat transaksi berhasil. Return False jika stok kurang."""
        if self.__stok >= jumlah:
            self.__stok -= jumlah
            return True
        return False


# ---------------------------------------------------------------
# ABSTRACTION + POLYMORPHISM: MetodePembayaran
# ---------------------------------------------------------------
class MetodePembayaran(ABC):
    """Kelas abstrak — tidak bisa diinstansiasi langsung."""

    @abstractmethod
    def proses_pembayaran(self, total: int) -> str:
        ...


class TransferBank(MetodePembayaran):
    def proses_pembayaran(self, total: int) -> str:
        return (
            f"Metode: Transfer Bank\n"
            f"Silakan transfer Rp{total:,.0f}".replace(",", ".") +
            " ke Virtual Account BCA 8888-2201-xxxx.\n"
            f"Verifikasi dilakukan otomatis dalam 1x24 jam."
        )


class EWallet(MetodePembayaran):
    def proses_pembayaran(self, total: int) -> str:
        return (
            f"Metode: E-Wallet (QRIS)\n"
            f"Pindai kode QR untuk membayar Rp{total:,.0f}".replace(",", ".") +
            ".\nPembayaran terverifikasi secara instan."
        )


# ---------------------------------------------------------------
# ABSTRACTION + POLYMORPHISM: Notifikasi
# ---------------------------------------------------------------
class Notifikasi(ABC):
    """Kelas abstrak untuk pengiriman notifikasi ke pembeli."""

    @abstractmethod
    def kirim(self, pesan: str) -> str:
        ...


class NotifikasiEmail(Notifikasi):
    def kirim(self, pesan: str) -> str:
        return f"Email terkirim ke pembeli:\n\"{pesan}\""


class NotifikasiWhatsApp(Notifikasi):
    def kirim(self, pesan: str) -> str:
        return f"Pesan WhatsApp terkirim:\n\"{pesan}\""
