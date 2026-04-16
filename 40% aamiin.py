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


# =========================
# DOUBLE LINKED LIST
# =========================
class TrainRoute:
    def __init__(self):
        self.head = None

    # CREATE
    def add_station(self, name, connected = []):
        new_node = StationNode(name, connected)

        if not self.head:
            self.head = new_node
            return

        temp = self.head
        while temp.next:
            temp = temp.next

        temp.next = new_node
        new_node.prev = temp

    # READ
    def show_route(self):
        temp = self.head
        while temp:
            print(temp.name, end=" <-> ")
            temp = temp.next
        print("None")

    # UPDATE
    def update_station(self, old_name, new_name):
        temp = self.head
        while temp:
            if temp.name == old_name:
                temp.name = new_name
                print("Stasiun berhasil diupdate!")
                return
            temp = temp.next
        print("Stasiun tidak ditemukan!")

    # DELETE
    def delete_station(self, name):
        temp = self.head

        while temp:
            if temp.name == name:

                if temp.prev:
                    temp.prev.next = temp.next
                else:
                    self.head = temp.next

                if temp.next:
                    temp.next.prev = temp.prev

                print("Stasiun berhasil dihapus!")
                return

            temp = temp.next

        print("Stasiun tidak ditemukan!")

    # SAVE TO FILE
    def save_to_file(self, filename="route.csv"):
        data = []
        temp = self.head

        while temp:
            data.append([temp.name])
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

                self.head = None
                for row in reader:
                    self.add_station(row[0])

            print("Data berhasil dimuat!")
        except FileNotFoundError:
            print("File belum ada!")
    
    def show_station(self, name):
        temp = self.head
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
        temp = self.head
        while temp:
            stations.append(temp.name)
            temp = temp.next
        return stations


# =========================
# MAIN PROGRAM
# =========================
def main():
    route = TrainRoute()

    while True:
        print("\n=== TRAIN ROUTE MENU ===")
        print("1. Tambah Stasiun")
        print("2. Lihat Rute")
        print("3. Update Stasiun")
        print("4. Hapus Stasiun")
        print("5. Simpan ke File")
        print("6. Load dari File")
        print("7. Keluar")
        print("8. Lihat Stasiun Tertentu")

        choice = input("Pilih menu: ")

        if choice == "1":
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
            route.show_route()

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

        else:
            print("Input tidak valid!")


if __name__ == "__main__":
    main()