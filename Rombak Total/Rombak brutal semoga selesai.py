import csv
import os
import time

class Node:
    def __init__(self, kode, nama, kota):
        self.kode = kode
        self.nama = nama
        self.kota = kota
        self.prev = None
        self.next = None


class StackRiwayat:
    def __init__(self):
        self.data = []

    def push(self, perjalanan):
        self.data.append(perjalanan)

    def tampilkan(self):
        if len(self.data) == 0:
            print("\nRiwayat perjalanan masih kosong.")
            return

        print("\n=== RIWAYAT PERJALANAN TERAKHIR ===")
        nomor = 1

        for i in range(len(self.data) - 1, -1, -1):
            print(str(nomor) + ". " + self.data[i])
            nomor += 1


class RuteKereta:
    def __init__(self):
        self.head = None
        self.tail = None

    def kosong(self):
        return self.head is None

    def tambah_stasiun(self, kode, nama, kota, posisi = None):
        node_baru = Node(kode, nama, kota)
    
        if self.kosong():
            self.head = node_baru
            self.tail = node_baru
        elif posisi is not None:
            temp = self.head
            i = 1
            while i < posisi - 1 and temp.next is not None:
                temp = temp.next
                i += 1
            if temp == self.head and posisi == 1:
                node_baru.next = self.head
                self.head.prev = node_baru
                self.head = node_baru
            else:
                node_baru.next = temp.next
                temp.next.prev = node_baru
                temp.next = node_baru
                node_baru.prev = temp
        else:
            self.tail.next = node_baru
            node_baru.prev = self.tail
            self.tail = node_baru

    def kode_sudah_ada(self, kode):
        bantu = self.head
        while bantu is not None:
            if bantu.kode.lower() == kode.lower():
                return True
            bantu = bantu.next
        return False

    def cari_node(self, keyword):
        bantu = self.head
        while bantu is not None:
            if keyword.lower() == bantu.kode.lower() or keyword.lower() == bantu.nama.lower():
                return bantu
            bantu = bantu.next
        return None

    def tampil_maju(self):
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
            if kode_baru.lower() != node.kode.lower() and self.kode_sudah_ada(kode_baru):
                print("Kode sudah dipakai oleh stasiun lain. Kode tidak diubah.")
            else:
                node.kode = kode_baru

        if nama_baru != "":
            node.nama = nama_baru

        if kota_baru != "":
            node.kota = kota_baru

        print("\nData stasiun berhasil diubah.")

    def hapus_stasiun(self, keyword):
        node = self.cari_node(keyword)

        if node is None:
            print("\nStasiun tidak ditemukan.")
            return

        if node == self.head and node == self.tail:
            self.head = None
            self.tail = None
        elif node == self.head:
            self.head = node.next
            self.head.prev = None
        elif node == self.tail:
            self.tail = node.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        print("\nStasiun berhasil dihapus.")

    def cari_stasiun(self, keyword):
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
        if self.kosong():
            print("\nData stasiun masih kosong.")
            return

        daftar = []
        bantu = self.head

        while bantu is not None:
            daftar.append(bantu)
            bantu = bantu.next

        for i in range(len(daftar)):
            for j in range(0, len(daftar) - i - 1):
                if daftar[j].nama.lower() > daftar[j + 1].nama.lower():
                    daftar[j], daftar[j + 1] = daftar[j + 1], daftar[j]

        print("\n=== STASIUN URUT A-Z ===")
        for i in range(len(daftar)):
            print(str(i + 1) + ". " + daftar[i].kode + " - " + daftar[i].nama + " (" + daftar[i].kota + ")")

    def pilih_stasiun_awal(self):
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
        if self.kosong():
            print("\nData stasiun masih kosong.")
            return

        posisi = self.pilih_stasiun_awal()

        while True:
            print("\n=== SIMULASI PERJALANAN RED LINE ===")

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
                if posisi.next is None:
                    print("Kereta sudah berada di stasiun terakhir.")
                else:
                    asal = posisi.nama
                    tujuan = posisi.next.nama
                    print("Kereta bergerak dari " + asal + " ke " + tujuan)
                    riwayat.push(asal + " -> " + tujuan)
                    posisi = posisi.next

            elif pilih == 2:
                if posisi.prev is None:
                    print("Kereta sudah berada di stasiun pertama.")
                else:
                    asal = posisi.nama
                    tujuan = posisi.prev.nama
                    print("Kereta bergerak dari " + asal + " ke " + tujuan)
                    riwayat.push(asal + " -> " + tujuan)
                    posisi = posisi.prev

            elif pilih == 3:
                posisi = self.pilih_stasiun_awal()

            elif pilih == 4:
                break

    def simpan_csv(self, nama_file):
        with open(nama_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["kode", "nama", "kota"])

            bantu = self.head
            while bantu is not None:
                writer.writerow([bantu.kode, bantu.nama, bantu.kota])
                bantu = bantu.next

        print("\nData berhasil disimpan ke", nama_file)

    def baca_csv(self, nama_file):
        if not os.path.exists(nama_file):
            return

        with open(nama_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                kode = row["kode"]
                nama = row["nama"]
                kota = row["kota"]
                self.tambah_stasiun(kode, nama, kota)


def input_angka(pesan, batas_bawah, batas_atas):
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

# Function =========================================================================

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def wait(sec):
    time.sleep(sec)

def input_teks(pesan):
    while True:
        teks = input(pesan).strip()

        if teks != "":
            return teks
        else:
            print("Input tidak boleh kosong.")


def menu_admin(rute, nama_file):
    password = input("Masukkan password admin: ")

    if password != "admin":
        print("Password salah.")
        return
    clear_terminal()
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
            print("===== TAMBAH STASIUN BARU =====")
            posisi_index = input_angka("Masukkan posisi stasiun baru (1 untuk paling awal): ", 1, 1000)
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
            rute.ubah_stasiun(keyword)

        elif pilih == 6:
            clear_terminal()
            print("===== HAPUS STASIUN =====")
            keyword = input_teks("Masukkan kode/nama stasiun yang ingin dihapus: ")
            rute.hapus_stasiun(keyword)

        elif pilih == 7:
            rute.simpan_csv(nama_file)

        elif pilih == 8:
            break


def menu_pelanggan(rute, riwayat):
    clear_terminal()
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
            rute.tampil_maju()

        elif pilih == 2:
            rute.tampil_mundur()

        elif pilih == 3:
            keyword = input_teks("Masukkan kode/nama/kota stasiun: ")
            rute.cari_stasiun(keyword)

        elif pilih == 4:
            rute.urutkan_nama()

        elif pilih == 5:
            rute.simulasi_perjalanan(riwayat)

        elif pilih == 6:
            riwayat.tampilkan()

        elif pilih == 7:
            break


def main():
    nama_file = "stasiun.csv"

    rute = RuteKereta()
    riwayat = StackRiwayat()

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
            rute.simpan_csv(nama_file)
            print("Terima kasih sudah menggunakan program.")
            break


main()
