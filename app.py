"""
app.py
======
Aplikasi web "Rak Baca" — pemesanan buku online.
Dibangun dengan Flask, mengikuti struktur OOP pada models.py.

Jalankan dengan:
    python app.py
"""

from flask import Flask, render_template, request, redirect, url_for, session

from models import Pembeli, TransferBank, EWallet, NotifikasiEmail, NotifikasiWhatsApp
from data import buku_list, KATEGORI_LIST, get_buku_by_id, next_id

app = Flask(__name__)
app.secret_key = "rak-baca-secret-key-ganti-jika-produksi"

# Pengguna contoh (mewakili Pembeli yang sedang login)
pembeli_aktif = Pembeli(101, "Tamu", "tamu@rakbaca.id")


def format_rupiah(n: int) -> str:
    return "Rp " + f"{n:,.0f}".replace(",", ".")


app.jinja_env.filters["rupiah"] = format_rupiah


# -----------------------------------------------------------
# Helper keranjang (disimpan di session, format: {id_buku: qty})
# -----------------------------------------------------------
def get_cart() -> dict:
    return session.setdefault("cart", {})


def cart_items():
    """Kembalikan list of dict {buku, qty, subtotal} dari isi session cart."""
    items = []
    for id_str, qty in get_cart().items():
        buku = get_buku_by_id(int(id_str))
        if buku:
            items.append({"buku": buku, "qty": qty, "subtotal": buku.get_harga() * qty})
    return items


def cart_total() -> int:
    return sum(item["subtotal"] for item in cart_items())


def cart_count() -> int:
    return sum(get_cart().values())


@app.context_processor
def inject_cart_info():
    """Membuat cart_count & cart_total tersedia otomatis di semua template."""
    return {"cart_count": cart_count(), "cart_total": cart_total()}


# -----------------------------------------------------------
# KATALOG
# -----------------------------------------------------------
@app.route("/")
def index():
    kategori_aktif = request.args.get("kategori", "Semua")
    q = request.args.get("q", "").strip().lower()

    hasil = [
        b for b in buku_list
        if (kategori_aktif == "Semua" or b.get_kategori() == kategori_aktif)
        and (q in b.get_judul().lower() or q in b.get_penulis().lower())
    ]

    return render_template(
        "index.html",
        buku_list=hasil,
        kategori_list=KATEGORI_LIST,
        kategori_aktif=kategori_aktif,
        q=request.args.get("q", ""),
    )


# -----------------------------------------------------------
# KERANJANG
# -----------------------------------------------------------
@app.route("/cart/add/<int:id_buku>", methods=["POST"])
def cart_add(id_buku):
    buku = get_buku_by_id(id_buku)
    cart = get_cart()
    if buku and buku.get_stok() > 0:
        current_qty = cart.get(str(id_buku), 0)
        if current_qty < buku.get_stok():
            cart[str(id_buku)] = current_qty + 1
            session.modified = True
    return redirect(request.referrer or url_for("index"))


@app.route("/cart/update/<int:id_buku>", methods=["POST"])
def cart_update(id_buku):
    delta = int(request.form.get("delta", 0))
    buku = get_buku_by_id(id_buku)
    cart = get_cart()
    key = str(id_buku)
    if key in cart and buku:
        new_qty = cart[key] + delta
        if new_qty <= 0:
            cart.pop(key)
        elif new_qty <= buku.get_stok():
            cart[key] = new_qty
        session.modified = True
    return redirect(url_for("cart_view"))


@app.route("/cart")
def cart_view():
    return render_template("cart.html", items=cart_items(), total=cart_total())


# -----------------------------------------------------------
# CHECKOUT — Polymorphism (MetodePembayaran)
# -----------------------------------------------------------
@app.route("/checkout", methods=["GET", "POST"])
def checkout_page():
    items = cart_items()
    if not items:
        return redirect(url_for("cart_view"))

    if request.method == "GET":
        return render_template("checkout_select.html", items=items, total=cart_total())

    metode = request.form.get("metode", "bank")
    total = cart_total()

    # --- pemanggilan polymorphic: objek berbeda, method sama ---
    instance = TransferBank() if metode == "bank" else EWallet()
    hasil_bayar = instance.proses_pembayaran(total)

    # --- kurangi stok lewat method milik kelas Buku (encapsulation) ---
    for item in items:
        item["buku"].kurangi_stok(item["qty"])

    pesan_konfirmasi = (
        f"Halo {pembeli_aktif.get_nama()}, pesananmu senilai "
        f"{format_rupiah(total)} di Rak Baca sudah kami terima dan sedang diproses."
    )

    session["last_pay_result"] = hasil_bayar
    session["last_pesan"] = pesan_konfirmasi
    session.pop("last_notif_result", None)
    session["cart"] = {}  # kosongkan keranjang
    session.modified = True

    return redirect(url_for("checkout_result"))


@app.route("/checkout/result")
def checkout_result():
    pay_result = session.get("last_pay_result")
    if not pay_result:
        return redirect(url_for("index"))
    return render_template(
        "checkout.html",
        pay_result=pay_result,
        notif_result=session.get("last_notif_result"),
    )


# -----------------------------------------------------------
# NOTIFIKASI — Abstraction + Polymorphism
# -----------------------------------------------------------
@app.route("/checkout/notify", methods=["POST"])
def checkout_notify():
    jenis = request.form.get("jenis", "email")
    pesan = session.get("last_pesan", "")

    # --- pemanggilan polymorphic: objek berbeda, method sama ---
    instance = NotifikasiEmail() if jenis == "email" else NotifikasiWhatsApp()
    hasil = instance.kirim(pesan)

    session["last_notif_result"] = hasil
    session.modified = True
    return redirect(url_for("checkout_result"))


# -----------------------------------------------------------
# ADMIN — Encapsulation demo (stok hanya via method)
# -----------------------------------------------------------
@app.route("/admin")
def admin():
    return render_template("admin.html", buku_list=buku_list)


@app.route("/admin/stock/<int:id_buku>", methods=["POST"])
def admin_stock(id_buku):
    delta = int(request.form.get("delta", 0))
    buku = get_buku_by_id(id_buku)
    if buku:
        if delta > 0:
            buku.set_stok(buku.get_stok() + delta)
        else:
            buku.kurangi_stok(abs(delta))
    return redirect(url_for("admin"))


@app.route("/admin/add", methods=["POST"])
def admin_add():
    judul = request.form.get("judul", "").strip()
    penulis = request.form.get("penulis", "").strip()
    kategori = request.form.get("kategori", "Fiksi")
    harga = int(request.form.get("harga") or 0)
    stok = int(request.form.get("stok") or 0)
    kode_rak = request.form.get("kode_rak", "").strip() or "000.0 / BRU"

    if judul and penulis and harga > 0:
        from models import Buku
        buku_list.append(Buku(next_id(), judul, penulis, kategori, harga, stok, kode_rak))

    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
