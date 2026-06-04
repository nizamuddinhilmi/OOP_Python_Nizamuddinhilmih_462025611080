class AlatPembayaran:
    def proses_bayar(self, jumlah):
        """Metode default di parent class (opsional, bisa juga jadi abstract)"""
        print(s"Memproses pembayaran sebesar Rp{jumlah} menggunakan alat pembayaran umum.")

class KartuKredit(AlatPembayaran):
    def __init__(self, nomor_kartu):
        self.nomor_kartu = nomor_kartu

    def proses_bayar(self, jumlah):
        biaya_admin = 2500
        total = jumlah + biaya_admin
        print(f"[Kartu Kredit - {self.nomor_kartu}]")
        print(f"  -> Memproses transaksi: Rp{jumlah}")
        print(f"  -> Dikenakan biaya admin: Rp{biaya_admin}")
        print(f"  -> Total tagihan ke kartu: Rp{total}\n")

class EWallet(AlatPembayaran):
    def __init__(self, nomor_hp):
        self.nomor_hp = nomor_hp

    
    def proses_bayar(self, jumlah):
        cashback = int(jumlah * 0.05)
        print(f"[E-Wallet - {self.nomor_hp}]")
        print(f"  -> Memproses transaksi: Rp{jumlah}")
        print(f"  -> Selamat! Anda mendapatkan cashback: Rp{cashback}\n")


class UangTunai:
    def proses_bayar(self, jumlah):
        print(f"[Uang Tunai]")
        print(f"  -> Membayar langsung secara tunai pas: Rp{jumlah}\n")



def jalankan_transaksi(objek_pembayaran, jumlah):
    """
    Fungsi mandiri di luar kelas.
    Fungsi ini tidak peduli apa tipe kelas dari 'objek_pembayaran'.
    Selama objek tersebut punya metode 'proses_bayar()', maka program akan jalan.
    """
    print(f"--- Memulai Transaksi Sebesar Rp{jumlah} ---")
    objek_pembayaran.proses_bayar(jumlah)




if __name__ == "__main__":
    dompet_cc = KartuKredit("4567-xxxx-xxxx-1234")
    dompet_digital = EWallet("0812-3456-7890")
    cash_di_tangan = UangTunai()

    jalankan_transaksi(dompet_cc, 150000)
    jalankan_transaksi(dompet_digital, 50000)
    
    jalankan_transaksi(cash_di_tangan, 20000)