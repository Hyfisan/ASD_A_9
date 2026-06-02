import csv
import os
import time

# ==============================================================================
# STRUKTUR DATA: DOUBLE LINKED LIST & STACK
# ==============================================================================

class Node:
    def __init__(self, kode, nama, kota):
        self.kode = kode        # Kode unik stasiun (misal: MBG)
        self.nama = nama        # Nama stasiun (misal: Mabang)
        self.kota = kota        # Kota lokasi stasiun
        self.prev = None        # Pointer ke stasiun sebelumnya
        self.next = None        # Pointer ke stasiun berikutnya 


class StackRiwayat:
    """Class untuk menyimpan riwayat simulasi perjalanan menggunakan konsep Stack (Tumpukan)."""
    def __init__(self):
        self.data = []

    def push_simulasi(self, daftar_perjalanan):
        # Simpan hanya jika ada minimal satu perpindahan
        if len(daftar_perjalanan) > 0:
            self.data.append(daftar_perjalanan)

    def tampilkan(self):
        # Menampilkan isi stack dari atas ke bawah (simulasi terbaru ke terlama)
        if len(self.data) == 0:
            print("\nRiwayat perjalanan masih kosong.")
            return

        print("\n=== RIWAYAT PERJALANAN PER SIMULASI ===")
        # Looping mundur dari indeks terakhir ke 0
        for i in range(len(self.data) - 1, -1, -1):
            nomor_simulasi_asli = i + 1

            print("\nSimulasi " + str(nomor_simulasi_asli) + ":")
            daftar_perjalanan = self.data[i]

            for j in range(len(daftar_perjalanan)):
             print("  " + str(j + 1) + ". " + daftar_perjalanan[j])

class RuteKereta:
    """Class Double Linked List untuk mengelola urutan stasiun kereta."""
    def __init__(self):
        self.head = None          # Stasiun paling awal
        self.tail = None          # Stasiun paling akhir

    def kosong(self):
        # Cek apakah rute masih kosong
        return self.head is None

    def tambah_stasiun(self, kode, nama, kota, posisi=None):
        # Menambah stasiun baru. Bisa di posisi tertentu atau di akhir (tail).
        node_baru = Node(kode, nama, kota)
    
        if self.kosong():
            # Jika kosong, head dan tail menunjuk ke node baru
            self.head = node_baru
            self.tail = node_baru
        elif posisi is not None:
            # Jika user meminta disisipkan di posisi tertentu
            temp = self.head
            i = 1
            # Cari posisi yang dituju
            while i < posisi - 1 and temp.next is not None:
                temp = temp.next
                i += 1
            
            # Sisip di paling depan
            if temp == self.head and posisi == 1:
                node_baru.next = self.head
                self.head.prev = node_baru
                self.head = node_baru
            # Sisip di paling belakang
            elif temp.next is None:
                temp.next = node_baru
                node_baru.prev = temp
                self.tail = node_baru
            # Sisip di tengah-tengah
            else:
                node_baru.next = temp.next
                temp.next.prev = node_baru
                temp.next = node_baru
                node_baru.prev = temp
        else:
            # Default: tambah di akhir rute (tail)
            self.tail.next = node_baru
            node_baru.prev = self.tail
            self.tail = node_baru

    def kode_sudah_ada(self, kode):
        # Validasi agar tidak ada stasiun dengan kode yang sama
        bantu = self.head
        while bantu is not None:
            if bantu.kode.lower() == kode.lower():
                return True
            bantu = bantu.next
        return False

    def cari_node(self, keyword):
        # Pencarian presisi untuk mendapatkan Node (berdasarkan kode atau nama)
        bantu = self.head
        while bantu is not None:
            if keyword.lower() == bantu.kode.lower() or keyword.lower() == bantu.nama.lower():
                return bantu
            bantu = bantu.next
        return None

    def tampil_maju(self):
        # Menelusuri dari Head ke Tail
        if self.kosong():
            print("\nData stasiun masih kosong.")
            return

        daftar_nama = []
        bantu = self.head
        while bantu is not None:
            daftar_nama.append(bantu.nama)
            bantu = bantu.next

        print("\nRute Maju Jakarta Kota - Bogor:")
        print(" <-> ".join(daftar_nama))

    def tampil_mundur(self):
        # Menelusuri dari Tail ke Head (memanfaatkan pointer prev)
        if self.kosong():
            print("\nData stasiun masih kosong.")
            return

        daftar_nama = []
        bantu = self.tail
        while bantu is not None:
            daftar_nama.append(bantu.nama)
            bantu = bantu.prev

        print("\nRute Balik Bogor - Jakarta Kota:")
        print(" <-> ".join(daftar_nama))

    def tampil_detail(self):
        # Menampilkan rincian setiap stasiun
        if self.kosong():
            print("\nData stasiun masih kosong.")
            return

        print("\n=== DATA STASIUN ===")
        bantu = self.head
        nomor = 1

        while bantu is not None:
            print(str(nomor) + ". " + bantu.kode + " - " + bantu.nama + " (" + bantu.kota + ")")
            bantu = bantu.next
            nomor += 1

    def ubah_stasiun(self, keyword):
        # Mengubah data di dalam node tertentu
        node = self.cari_node(keyword)

        if node is None:
            print("\nStasiun tidak ditemukan.")
            return

        print("\nData lama:")
        print("Kode :", node.kode)
        print("Nama :", node.nama)
        print("Kota :", node.kota)

        print("\nKosongkan input jika tidak ingin mengubah data.")
        kode_baru = input("Kode baru: ").strip().upper()
        nama_baru = input("Nama baru: ").strip()
        kota_baru = input("Kota baru: ").strip()

        if kode_baru != "":
            # Cek apakah kode baru bentrok dengan stasiun lain
            if kode_baru.lower() != node.kode.lower() and self.kode_sudah_ada(kode_baru):
                print("Kode sudah dipakai oleh stasiun lain. Kode tidak diubah.")
            else:
                node.kode = kode_baru

        if nama_baru != "":
            node.nama = nama_baru

        if kota_baru != "":
            node.kota = kota_baru

    def hapus_stasiun(self, keyword):
        # Menghapus node dari Double Linked List
        node = self.cari_node(keyword)

        if node is None:
            print("\nStasiun tidak ditemukan.")
            return

        # Kasus 1: Node adalah satu-satunya stasiun di list
        if node == self.head and node == self.tail:
            self.head = None
            self.tail = None
        # Kasus 2: Hapus head (paling awal)
        elif node == self.head:
            self.head = node.next
            self.head.prev = None
        # Kasus 3: Hapus tail (paling akhir)
        elif node == self.tail:
            self.tail = node.prev
            self.tail.next = None
        # Kasus 4: Hapus di tengah-tengah
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

    def cari_stasiun(self, keyword):
        # Pencarian menggunakan metode 'mengandung kata' (substring)
        if self.kosong():
            print("\nData stasiun masih kosong.")
            return

        bantu = self.head
        ditemukan = False

        print("\n=== HASIL PENCARIAN ===")

        while bantu is not None:
            if (keyword.lower() in bantu.kode.lower() or
                    keyword.lower() in bantu.nama.lower() or
                    keyword.lower() in bantu.kota.lower()):

                print("Kode :", bantu.kode)
                print("Nama :", bantu.nama)
                print("Kota :", bantu.kota)

                # Menampilkan relasi (stasiun sebelumnya & berikutnya)
                if bantu.prev is not None:
                    print("Sebelumnya :", bantu.prev.nama)
                else:
                    print("Sebelumnya : Tidak ada")

                if bantu.next is not None:
                    print("Berikutnya :", bantu.next.nama)
                else:
                    print("Berikutnya : Tidak ada")

                print("----------------------------")
                ditemukan = True

            bantu = bantu.next

        if not ditemukan:
            print("Stasiun tidak ditemukan.")

    def urutkan_nama(self):
        # Mengurutkan stasiun secara Alfabetis menggunakan Bubble Sort
        if self.kosong():
            print("\nData stasiun masih kosong.")
            return

        # Masukkan ke list sementara agar mudah disorting
        daftar = []
        bantu = self.head
        while bantu is not None:
            daftar.append(bantu)
            bantu = bantu.next

        # Algoritma Bubble Sort
        for i in range(len(daftar)):
            for j in range(0, len(daftar) - i - 1):
                if daftar[j].nama.lower() > daftar[j + 1].nama.lower():
                    # Tukar posisi
                    daftar[j], daftar[j + 1] = daftar[j + 1], daftar[j]

        print("\n=== STASIUN URUT A-Z ===")
        for i in range(len(daftar)):
            print(str(i + 1) + ". " + daftar[i].kode + " - " + daftar[i].nama + " (" + daftar[i].kota + ")")

    def pilih_stasiun_awal(self):
        # Mengatur titik awal untuk fitur simulasi perjalanan
        print("\nDaftar stasiun:")
        bantu = self.head
        nomor = 1

        while bantu is not None:
            print(str(nomor) + ". " + bantu.kode + " - " + bantu.nama)
            bantu = bantu.next
            nomor += 1

        while True:
            keyword = input("\nMasukkan kode atau nama stasiun awal: ").strip()

            if keyword == "":
                print("Input tidak boleh kosong.")
            else:
                posisi = self.cari_node(keyword)
                if posisi is not None:
                    return posisi
                else:
                    print("Stasiun tidak ditemukan. Coba masukkan kode/nama yang benar.")

    def simulasi_perjalanan(self, riwayat):
        # Berjalan-jalan menyusuri rute linked list ke depan atau ke belakang
        if self.kosong():
            print("\nData stasiun masih kosong.")
            return

        posisi = self.pilih_stasiun_awal()
        riwayat_simulasi = []

        while True:
            print("\n=== SIMULASI PERJALANAN ===")

            daftar_nama = []
            bantu = self.head
            while bantu is not None:
                daftar_nama.append(bantu.nama)
                bantu = bantu.next

            print("Rute:", " <-> ".join(daftar_nama))
            print("Posisi sekarang:", posisi.nama, "(" + posisi.kode + ")")
            print("1. Lanjut ke stasiun berikutnya")
            print("2. Kembali ke stasiun sebelumnya")
            print("3. Ganti stasiun awal / posisi")
            print("4. Selesai simulasi")

            pilih = input_angka("Pilih menu: ", 1, 4)

            if pilih == 1:
                # Pindah ke node selanjutnya (next)
                if posisi.next is None:
                    print("Kereta sudah berada di stasiun terakhir.")
                else:
                    asal = posisi.nama
                    tujuan = posisi.next.nama
                    print("Kereta bergerak dari " + asal + " ke " + tujuan)
                    riwayat_simulasi.append(asal + " -> " + tujuan)
                    posisi = posisi.next

            elif pilih == 2:
                # Pindah ke node sebelumnya (prev)
                if posisi.prev is None:
                    print("Kereta sudah berada di stasiun pertama.")
                else:
                    asal = posisi.nama
                    tujuan = posisi.prev.nama
                    print("Kereta bergerak dari " + asal + " ke " + tujuan)
                    riwayat_simulasi.append(asal + " -> " + tujuan)
                    posisi = posisi.prev

            elif pilih == 3:
                posisi = self.pilih_stasiun_awal()

            elif pilih == 4:
                # Akhiri simulasi dan simpan ke StackRiwayat
                if len(riwayat_simulasi) > 0:
                    riwayat.push_simulasi(riwayat_simulasi)
                    print("\nSimulasi selesai dan riwayat berhasil disimpan.")
                else:
                    print("\nSimulasi selesai tanpa perpindahan. Riwayat tidak disimpan.")
                break
            
# ==============================================================================
    # PENYIMPANAN DATA (FILE CSV)
    # ==============================================================================

    def simpan_csv(self, nama_file):
        # Menyimpan rute dari linked list kembali ke dalam file CSV
        with open(nama_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["kode", "nama", "kota"]) # Header tabel

            bantu = self.head
            while bantu is not None:
                writer.writerow([bantu.kode, bantu.nama, bantu.kota])
                bantu = bantu.next

        print("\nData berhasil disimpan ke", nama_file, "...")

    def baca_csv(self, nama_file):
        # Memuat rute ke dalam linked list dari file CSV
        if not os.path.exists(nama_file):
            return

        with open(nama_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                kode = row["kode"]
                nama = row["nama"]
                kota = row["kota"]
                self.tambah_stasiun(kode, nama, kota)

# ==============================================================================
# FUNGSI PEMBANTU (UTILITY)
# ==============================================================================

def input_angka(pesan, batas_bawah, batas_atas):
    """Validasi agar input selalu berupa angka dan berada dalam range pilihan menu."""
    while True:
        data = input(pesan)
        try:
            angka = int(data)
            if angka >= batas_bawah and angka <= batas_atas:
                return angka
            else:
                print("Pilihan harus dari", batas_bawah, "sampai", batas_atas)
        except ValueError:
            print("Input harus berupa angka.")


def get_all_stations(rute):
    """Mengambil seluruh kode stasiun yang ada di dalam rute."""
    semua_stasiun = []
    temp = rute.head
    while temp is not None:
        semua_stasiun.append(temp.kode)
        temp = temp.next
    return semua_stasiun

def clear_terminal():
    """Membersihkan layar terminal. Kompatibel dengan Windows (nt) maupun Linux/Mac."""
    os.system("cls" if os.name == "nt" else "clear")

def wait(sec):
    """Memberikan jeda waktu (delay)."""
    time.sleep(sec)

def input_teks(pesan):
    """Memaksa user agar tidak memberikan input kosong/hanya spasi."""
    while True:
        teks = input(pesan).strip()
        if teks != "":
            return teks
        else:
            print("Input tidak boleh kosong.")


# ==============================================================================
# MENU ANTARMUKA (INTERFACE)
# ==============================================================================

def menu_admin(rute, nama_file):
    """Menu khusus admin yang memiliki fungsi CRUD (Create, Read, Update, Delete)."""
    password = input("Masukkan password admin: ")

    if password != "admin":
        print("Password salah.")
        return
        
    clear_terminal()
    
    # Animasi loading sederhana
    i = 0
    j = 0
    while i < 2:
        while j < 4:
            print("Login berhasil. Masuk" + "." * j, end="\r")
            wait(0.5)
            j += 1
        i += 1
        j = 0
        clear_terminal()

    while True:
        print("\n=== MODE ADMIN ===")
        print("1. Tambah stasiun")
        print("2. Lihat rute maju")
        print("3. Lihat rute balik")
        print("4. Lihat detail stasiun")
        print("5. Ubah stasiun")
        print("6. Hapus stasiun")
        print("7. Simpan data")
        print("8. Kembali")

        pilih = input_angka("Pilih menu: ", 1, 8)

        if pilih == 1:
            clear_terminal()
            jumlah_stasiun = len(get_all_stations(rute))
            print("===== TAMBAH STASIUN BARU =====")
            # Admin bisa memilih lokasi sisipan stasiun berdasarkan urutan (1 hingga max+1)
            posisi_index = input_angka(f"Masukkan posisi stasiun baru (1-{jumlah_stasiun + 1}): ", 1, jumlah_stasiun + 1)
            kode = input_teks("Kode stasiun: ").upper()

            if rute.kode_sudah_ada(kode):
                print("Kode stasiun sudah ada.")
            else:
                nama = input_teks("Nama stasiun: ")
                kota = input_teks("Kota: ")
                rute.tambah_stasiun(kode, nama, kota, posisi_index)
                print("Menambahkan stasiun baru...")
                wait(2)
                clear_terminal()
                print("Stasiun berhasil ditambahkan.")
                wait(1)

        elif pilih == 2:
            clear_terminal()
            print("===== RUTE MAJU =====")
            rute.tampil_maju()
            input("\nTekan Enter untuk kembali ke menu.")

        elif pilih == 3:
            clear_terminal()
            print("===== RUTE BALIK =====")
            rute.tampil_mundur()
            input("\nTekan Enter untuk kembali ke menu.")

        elif pilih == 4:
            clear_terminal()
            print("===== DETAIL STASIUN =====")
            rute.tampil_detail()

        elif pilih == 5:
            clear_terminal()
            print("===== UBAH STASIUN =====")
            keyword = input_teks("Masukkan kode/nama stasiun yang ingin diubah: ")
            clear_terminal()
            rute.ubah_stasiun(keyword)
            print("Mengubah data stasiun...")
            wait(2)
            print("Data stasiun berhasil diubah.")
            wait(1)
            clear_terminal()

        elif pilih == 6:
            clear_terminal()
            print("===== HAPUS STASIUN =====")
            keyword = input_teks("Masukkan kode/nama stasiun yang ingin dihapus: ")
            rute.hapus_stasiun(keyword)
            print("Menghapus stasiun...")
            wait(2)
            print("Stasiun berhasil dihapus.")
            wait(1)
            clear_terminal()
        
        elif pilih == 7:
            # Eksplisit memanggil simpan ke CSV
            rute.simpan_csv(nama_file)
            wait(2)
            print("Data berhasil disimpan.")
            wait(1)
            clear_terminal()

        elif pilih == 8:
            break


def menu_pelanggan(rute, riwayat):
    """Menu untuk pengguna umum (baca/cari rute dan simulasi, tanpa hak edit rute)."""
    clear_terminal()
    
    # Animasi loading
    i = 0
    j = 0
    while i < 2:
        while j < 4:
            print("Loading" + "." * j, end="\r")
            wait(0.5)
            j += 1
        i += 1
        j = 0
        clear_terminal()
        
    while True:
        print("\n=== MODE PELANGGAN ===")
        print("1. Lihat rute maju")
        print("2. Lihat rute balik")
        print("3. Cari stasiun")
        print("4. Urutkan stasiun A-Z")
        print("5. Simulasi perjalanan")
        print("6. Lihat riwayat perjalanan")
        print("7. Kembali")

        pilih = input_angka("Pilih menu: ", 1, 7)

        if pilih == 1:
            clear_terminal()
            rute.tampil_maju()
            input("\nTekan Enter untuk kembali ke menu.")

        elif pilih == 2:
            clear_terminal()
            rute.tampil_mundur()
            input("\nTekan Enter untuk kembali ke menu.")

        elif pilih == 3:
            clear_terminal()
            keyword = input_teks("Masukkan kode/nama/kota stasiun: ")
            rute.cari_stasiun(keyword)
            input("\nTekan Enter untuk kembali ke menu.")
            
        elif pilih == 4:
            clear_terminal()
            rute.urutkan_nama()
            input("\nTekan Enter untuk kembali ke menu.")

        elif pilih == 5:
            clear_terminal()
            rute.simulasi_perjalanan(riwayat)
            input("\nTekan Enter untuk kembali ke menu.")

        elif pilih == 6:
            clear_terminal()
            riwayat.tampilkan()
            input("\nTekan Enter untuk kembali ke menu.")

        elif pilih == 7:
            clear_terminal()
            break

# ==============================================================================
# PROGRAM UTAMA (MAIN ROUTINE)
# ==============================================================================

def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    nama_file = "stasiun.csv"

    # Inisialisasi Objek (Double Linked List & Stack)
    rute = RuteKereta()
    riwayat = StackRiwayat()
    
    # Otomatis meload data dari CSV saat program baru dibuka
    rute.baca_csv(nama_file)

    while True:
        clear_terminal()
        print("\n=================================")
        print(" PROGRAM RUTE KERETA API")
        print("=================================")
        print("1. Mode Admin")
        print("2. Mode Pelanggan")
        print("3. Keluar")

        pilih = input_angka("Pilih menu: ", 1, 3)

        if pilih == 1:
            clear_terminal()
            menu_admin(rute, nama_file)

        elif pilih == 2:
            clear_terminal()
            menu_pelanggan(rute, riwayat)

        elif pilih == 3:
            # Memastikan data terakhir tersimpan sebelum program berhenti
            rute.simpan_csv(nama_file)
            print("Terima kasih sudah menggunakan program.")
            break

# Mengeksekusi program utama
main()