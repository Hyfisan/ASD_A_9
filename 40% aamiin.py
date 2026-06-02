import json
import os
import time

# =========================
# NODE DOUBLE LINKED LIST
# =========================
class StationNode: 
    def __init__(self, name):
        self.name = name
        # connected: dict -> {connected_name: {"length": <length>, "status": <status>}}
        self.connected = {}
        self.prev = None
        self.next = None

class StationRoute:
    def __init__(self, name, connected):
        self.name = name
        self.connected = connected
        self.next = None

# =========================
# DOUBLE LINKED LIST
# =========================
class TrainRoute:
    def __init__(self):
        self.head_station = None
        self.head_route = None

    # CREATE
    def add_station(self, name, connected, length, status = "Aktif"):
        # Cari stasiun yang sudah ada atau buat node baru
        if not self.head_station:
            new_node = StationNode(name)
            self.head_station = new_node
        else:
            temp = self.head_station
            while temp and temp.name != name:
                temp = temp.next
            
            if not temp:
                # Stasiun belum ada, buat node baru di akhir
                new_node = StationNode(name)
                temp = self.head_station
                while temp.next:
                    temp = temp.next
                temp.next = new_node
                new_node.prev = temp
            else:
                # Stasiun sudah ada, gunakan node yang sudah ada
                new_node = temp
        
        # Tambahkan koneksi ke stasiun
        if isinstance(connected, list):
            # Jika connected adalah list, loop untuk setiap koneksi
            for i, con_station in enumerate(connected):
                if con_station:  # Jika koneksi tidak kosong
                    if isinstance(length, list) and i < len(length):
                        length_val = length[i]
                    else:
                        length_val = length if not isinstance(length, list) else ""
                    new_node.connected[con_station] = {"length": length_val, "status": status}
        else:
            # Jika connected adalah single value
            if connected:
                new_node.connected[connected] = {"length": length, "status": status}

    # READ
    def show_stations(self):
        temp = self.head_station
        i = 1
        while temp:
            print(f"{i}. {temp.name}")
            i += 1
            temp = temp.next
        print("None")

    # UPDATE
    def update_station(self, old_name, new_name):
        temp = self.head_station
        found = False
        while temp:
            if temp.name == old_name:
                temp.name = new_name
                found = True
                break
            temp = temp.next

        if not found:
            print(f"GAGAL! Stasiun dengan nama '{old_name}' tidak ditemukan!")
            return

        # Update references in other nodes' connected dicts
        temp2 = self.head_station
        while temp2:
            if old_name in temp2.connected:
                temp2.connected[new_name] = temp2.connected.pop(old_name)
            temp2 = temp2.next

        print(f"Stasiun berhasil diupdate menjadi '{new_name}'!")

    # DELETE
    def delete_station(self, name):
        temp = self.head_station

        while temp:
            if temp.name == name:

                if temp.prev:
                    temp.prev.next = temp.next
                else:
                    self.head_station = temp.next

                if temp.next:
                    temp.next.prev = temp.prev

                # Remove references from other stations
                temp2 = self.head_station
                while temp2:
                    if name in temp2.connected:
                        del temp2.connected[name]
                    temp2 = temp2.next

                del temp
                print(f"Stasiun '{name}' berhasil dihapus!")
                return

            temp = temp.next

        print(f"GAGAL! Stasiun dengan nama '{name}' tidak ditemukan!")

    # SAVE TO FILE
    def save_to_file(self, filename="route.json"):
        data = {}
        temp = self.head_station

        while temp:
            data[temp.name] = temp.connected
            temp = temp.next

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        print("Data berhasil disimpan!")

    # LOAD FROM FILE
    def load_from_file(self, filename="route.json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not data:
                    return print("File kosong!")

                self.head_station = None
                for station_name, connections in data.items():
                    # Tambahkan stasiun tanpa koneksi dulu
                    self.add_station(station_name, [], [])
                    # Kemudian restore koneksinya
                    temp = self.head_station
                    while temp and temp.name != station_name:
                        temp = temp.next
                    if temp:
                        temp.connected = connections

            print("Data berhasil dimuat!")
        except FileNotFoundError:
            print("File belum ada!")
        except json.JSONDecodeError:
            print("File JSON tidak valid!")
    
    def show_station(self, name):
        temp = self.head_station
        found = False
        while found == False and temp:
            if temp.name == name:
                found = True
            else:
                temp = temp.next
        if found == True:
            print(f"Nama stasiun: {temp.name}")
            if temp.connected:
                print("Stasiun tersambung:")
                for c, info in temp.connected.items():
                    print(f" - {c}: Jarak={info.get('length','')}, Status={info.get('status','')}")
            else:
                print("Stasiun tersambung: None")
        else:
            print("Stasiun tidak ditemukan!")

    def give_all_stations(self):
        temp = self.head_station
        all_stations = []
        while temp:
            all_stations.append(temp.name)
            temp = temp.next
        return all_stations
    
    def check_connection(self, station1, station2):
        temp = self.head_station
        found = False
        while found == False and temp:
            if temp.name == station1:
                found = True
            else:
                temp = temp.next
        if found == True:
            return station2 in temp.connected.keys()
        else:
            print("Stasiun tidak ditemukan!")
            return False
        
    def add_route(self, name, connected=None):
        if connected is None:
            connected = []
        new_route = StationRoute(name, connected)

        if not self.head_route:
            self.head_route = new_route
            return

        temp = self.head_route
        while temp.next:
            temp = temp.next

        temp.next = new_route

# =========================
# ELSE FUNCTION
# =========================

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait(second):
    time.sleep(second)

# =========================
# MAIN PROGRAM
# =========================
def main():
    route = TrainRoute()
    route.load_from_file()

    while True:
        print("\n=== MENU RUTE KERETA API ===")
        print("1. Tambah Stasiun")
        print("2. Lihat Semua Stasiun")
        print("3. Lihat Stasiun Tertentu")
        print("4. Update Stasiun")
        print("5. Hapus Stasiun")
        print("6. Simpan ke File")
        print("7. Muat dari File")
        print("8. Keluar")
        print("9. Tambah Rute") #Bakal diupdate (belom bisa sepenuhnya)

        choice = input("Pilih menu: ")

        if choice == "1":

            print("Menambahkan stasiun baru.")
            name = input("Nama stasiun: (ketik batal jika ingin membatalkan) ").lower().capitalize()
            if name.lower() == "batal":
                    print("Penambahan stasiun dibatalkan.")
                    continue
            all_stations = route.give_all_stations()

            while name in all_stations:
                print(f"Stasiun '{name}' sudah ada! Masukan nama stasiun lain.")
                name = input("Nama stasiun: ").lower().capitalize()

                if name.lower() == "batal":
                    print("Penambahan stasiun dibatalkan.")
                    break
                
            list_connect_station = []
            list_length_connected = []
            while True:
                choice = input(f"Apakah stasiun {name} menyambung dengan stasiun lain? (y/n): ")

                if choice == "y":
                    connect_station = input("Masukan nama stasiun lain: ").lower().capitalize()
                    length = input("Masukan jarak antara stasiun: ")
                    if length and not length.isdigit():
                        print("Jarak harus berupa angka! Silakan masukkan kembali.")
                        continue
                    list_connect_station.append(connect_station)
                    list_length_connected.append(length)
                    continue

                elif choice == "n":
                    route.add_station(name, list_connect_station, list_length_connected)
                    print("Stasiun berhasil dibuat!")
                    break

                elif choice == "batal":
                    print("Penambahan stasiun dibatalkan.")
                    break

                else:
                    print("Masukkan jawaban valid! (y/n/batal)")

        elif choice == "2":
            route.show_stations()

        elif choice == "3":
            name = input("Nama stasiun: ").lower().capitalize()
            route.show_station(name)

        elif choice == "4":
            old = input("Stasiun lama: ").lower().capitalize()
            new = input("Stasiun baru: ").lower().capitalize()
            route.update_station(old, new)
            
        elif choice == "5":
            name = input("Nama stasiun: ").lower().capitalize()
            route.delete_station(name)

        elif choice == "6":
            route.save_to_file()
            
        elif choice == "7":
            nama_file = input("Nama file: ")
            route.load_from_file(nama_file)

        elif choice == "8":
            break

        elif choice == "9":
            name1 = input("Nama stasiun asal: ").lower().capitalize()
            name2 = input("Nama stasiun tujuan: ").lower().capitalize()
            if route.check_connection(name1, name2):
                route.add_route(f"{name1} - {name2}", [name1, name2])
                print("Rute berhasil dibuat!")
            else:
                print(f"Tidak ada koneksi langsung antara '{name1}' dan '{name2}'!")
            


if __name__ == "__main__":
    main()
