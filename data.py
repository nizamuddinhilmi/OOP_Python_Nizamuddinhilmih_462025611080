"""
data.py
=======
Penyimpanan data sementara (in-memory) untuk prototipe.
Pada pengembangan lanjutan, modul ini bisa diganti dengan
akses ke database (mis. SQLite/PostgreSQL) tanpa mengubah models.py.
"""

from models import Buku

KATEGORI_LIST = ["Semua", "Fiksi", "Non-Fiksi", "Anak", "Sains", "Sejarah"]

# Daftar buku awal
buku_list = [
    Buku(1, "Jejak di Antara Musim", "Ratri Anindya", "Fiksi", 89000, 6, "813.6 / RAT"),
    Buku(2, "Ekonomi untuk Semua Orang", "Dr. Budi Santosa", "Non-Fiksi", 112000, 3, "330.1 / SAN"),
    Buku(3, "Petualangan Kancil Cerdik", "Sari Melati", "Anak", 55000, 10, "398.2 / MEL"),
    Buku(4, "Semesta dalam Genggaman", "Prof. Amir Fauzi", "Sains", 134000, 0, "523.1 / FAU"),
    Buku(5, "Catatan dari Batavia", "Herlambang W.", "Sejarah", 98000, 4, "959.8 / HER"),
    Buku(6, "Kopi, Kertas, dan Kita", "Dinda Puspa", "Fiksi", 76000, 8, "813.7 / PUS"),
    Buku(7, "Algoritma dalam Kehidupan", "Reza Wibawa", "Sains", 121000, 5, "005.1 / WIB"),
    Buku(8, "Dongeng Sebelum Tidur", "Nina Kartika", "Anak", 49000, 12, "398.5 / KAR"),
]


def get_buku_by_id(id_buku: int):
    for b in buku_list:
        if b.get_id() == id_buku:
            return b
    return None


def next_id() -> int:
    return max((b.get_id() for b in buku_list), default=0) + 1
