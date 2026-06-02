import csv

# =========================
# NODE DOUBLE LINKED LIST
# =========================
class StationNode:
    def __init__(self, name):
        self.name = name
        self.connected = []
        self.length = []
        self.status = []
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
        new_node = StationNode(name)

        if not self.head_station:
            self.head_station = new_node
            return
        
        temp = self.head_station
        while temp.next and temp.name != name:
            temp = temp.next

        if temp.name == name:
            temp.connected.append(connected)
            temp.length.append(length)
            temp.status.append(status)
            return
        else:
            temp.next = new_node
            new_node.prev = temp
            new_node.connected.append(connected)
            new_node.length.append(length)
            new_node.status.append(status)
            return

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
        while temp:
            if temp.name == old_name:
                temp.name = new_name
                print(f"Stasiun berhasil diupdate menjadi '{new_name}'!")
                return
            temp = temp.next
        print(f"GAGAL! Stasiun dengan nama '{old_name}' tidak ditemukan!")

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

                del temp
                print(f"Stasiun '{name}' berhasil dihapus!")
                return

            temp = temp.next

        print(f"GAGAL! Stasiun dengan nama '{name}' tidak ditemukan!")

    # SAVE TO FILE
    def save_to_file(self, filename="route.csv"):
        data = []
        temp = self.head_station

        while temp:
            data.append([temp.name, temp.connected, temp.length, temp.status])
            temp = temp.next

        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            for row in data:
                for i in range(len(row[1])):
                    writer.writerow([row[0], row[1][i], row[2][i], row[3][i]])
                

        print("Data berhasil disimpan!")

    # LOAD FROM FILE
    def load_from_file(self, filename="route_rombak.csv"):
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                header = next(reader, None)
                if header is None:
                    return print("File kosong!")
                
                file.seek(0)
                self.head_station = None
                for row in reader:
                    name = row[0]
                    connected = row[1]
                    length = row[2]
                    status = row[3]
                    self.add_station(name, connected, length, status)

            print("Data berhasil dimuat!")
        except FileNotFoundError:
            print("File belum ada!")
    
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
            print(f"Stasiun tersambung: {temp.connected}")
            print(f"Jarak antar stasiun: {temp.length}")
            print(f"Status stasiun: {temp.status}")
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
            return station2 in temp.connected
        else:
            print("Stasiun tidak ditemukan!")
            return False
        
    def add_route(self, name, connected = []):
        new_route = StationRoute(name, connected)

        if not self.head_route:
            self.head_route = new_route
            return

        temp = self.head_route
        while temp.next:
            temp = temp.next

        temp.next = new_route

# =========================
# MAIN PROGRAM
# =========================
def main():
    route = TrainRoute()
    all_stations = route.give_all_stations()
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
            name = input("Nama stasiun: ")
            while name in all_stations:
                if name.lower() == "batal":
                    print("Penambahan stasiun dibatalkan.")
                    break
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
                    connect_station = input("Masukan nama stasiun lain: ")
                    length = input("Masukan jarak antara stasiun: ")
                    list_connect_station.append(connect_station)
                    list_length_connected.append(length)
                    continue
                else:
                    route.add_station(name, list_connect_station, list_length_connected)
                    all_stations.append(name)
                    print("Stasiun berhasil dibuat!")
                    break

        elif choice == "2":
            route.show_stations()

        elif choice == "3":
            name = input("Nama stasiun: ")
            route.show_station(name)

        elif choice == "4":
            old = input("Stasiun lama: ")
            new = input("Stasiun baru: ")
            route.update_station(old, new)
            
        elif choice == "5":
            name = input("Nama stasiun: ")
            route.delete_station(name)

        elif choice == "6":
            route.save_to_file()
            
        elif choice == "7":
            nama_file = input("Nama file: ")
            route.load_from_file(nama_file)

        elif choice == "8":
            break

        elif choice == "9":
            name1 = input("Nama stasiun pertama: ")
            name2 = input("Nama stasiun kedua: ")
            if route.check_connection(name1, name2):
                print(f"Stasiun {name1} dan {name2} saling terhubung.")
            else:
                print(f"Stasiun {name1} dan {name2} tidak saling terhubung.")

        else:
            print("Input tidak valid!")


if __name__ == "__main__":
    main()
