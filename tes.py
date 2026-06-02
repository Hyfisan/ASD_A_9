import csv

def load_from_file(filename="route_rombak.csv"):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        if header is None:
            return print("File kosong!")
        
        file.seek(0)
        for row in reader:
            name = row[0]
            connected = row[1].split(",")
            length = row[2].split(",")
            status = row[3].split(",")
            print(name, connected, length, status)

load_from_file()