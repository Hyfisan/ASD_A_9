import csv

# =========================
# NODE DOUBLE LINKED LIST
# =========================
class StationNode:
    def __init__(self, name, connected):
        self.name = name
        self.connected = connected
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
    def add_station(self, name, connected = []):
        new_node = StationNode(name, connected)

        if not self.head_station:
            self.head_station = new_node
            return

        temp = self.head_station
        while temp.next:
            temp = temp.next

        temp.next = new_node
        new_node.prev = temp

    # READ
    def show_stations(self):
        temp = self.head_station
        while temp:
            print(temp.name, end=" <-> ")
            temp = temp.next
        print("None")

    # UPDATE
    def update_station(self, old_name, new_name):
        temp = self.head_station
        while temp:
            if temp.name == old_name:
                temp.name = new_name
                print("Stasiun berhasil diupdate!")
                return
            temp = temp.next
        print("Stasiun tidak ditemukan!")

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
                print("Stasiun berhasil dihapus!")
                return

            temp = temp.next

        print("Stasiun tidak ditemukan!")

    # SAVE TO FILE
    def save_to_file(self, filename="route.csv"):
        data = []
        temp = self.head_station

        while temp:
            data.append([temp.name, ",".join(temp.connected)])
            temp = temp.next

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        print("Data berhasil disimpan!")

    # LOAD FROM FILE
    def load_from_file(self, filename="route.csv"):
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                header = next(reader, None)
                first_row = next(reader, None)
                if header is None:
                    return print("File kosong!")
                if first_row is None:
                    return print("File kosong!")

                self.head_station = None
                for row in reader:
                    self.add_station(row[0], row[1].split(","))

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
        else:
            print("Stasiun tidak ditemukan!")
        
    def all_stations(self):
        stations = []
        temp = self.head_station
        while temp:
            stations.append(temp.name)
            temp = temp.next
        return stations
    
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
    route.load_from_file()
    all_stations = route.all_stations()

    while True:
        print("\n=== MENU RUTE KERETA API ===")
        print("1. Tambah Stasiun")
        print("2. Lihat Rute")
        print("3. Update Stasiun")
        print("4. Hapus Stasiun")
        print("5. Simpan ke File")
        print("6. Muat dari File")
        print("7. Keluar")
        print("8. Lihat Stasiun Tertentu")
        print("9. Tambah Rute")

        choice = input("Pilih menu: ")

        if choice == "1":
            name = input("Nama stasiun: ")
            while name in all_stations:
                print("Nama stasiun sudah ada!")
                name = input("Nama stasiun: ")
            list_connect_station = []
            while True:
                choice = input(f"Apakah stasiun {name} menyambung dengan stasiun lain? (y/n): ")
                if choice == "y":
                    connect_station = input("Masukan nama stasiun lain: ")
                    list_connect_station.append(connect_station)
                    continue
                else:
                    route.add_station(name, list_connect_station)
                    print("Stasiun berhasil dibuat!")
                    break

        elif choice == "2":
            route.show_stations()

        elif choice == "3":
            old = input("Stasiun lama: ")
            new = input("Stasiun baru: ")
            route.update_station(old, new)

        elif choice == "4":
            name = input("Nama stasiun: ")
            route.delete_station(name)

        elif choice == "5":
            route.save_to_file()

        elif choice == "6":
            route.load_from_file()

        elif choice == "7":
            break

        elif choice == "8":
            name = input("Nama stasiun: ")
            route.show_station(name)

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
