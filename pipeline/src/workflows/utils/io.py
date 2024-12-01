import json
import csv

def load_list(file_path):
    with open(file_path, "r") as file:
        return file.read().splitlines()

def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def load_csv(file_path):
    with open(file_path, "r", newline="") as file:
        return csv.DictReader(file)


def save_list(file_path, data):
    with open(file_path, "w") as file:
        for entry in data:
            file.write(f"{entry}\n")

def save_csv(file_path, fieldnames, data):
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

def save_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def save_list_stream(stream, data):
    for entry in data:
        stream.write(f"{entry}\n")

def save_csv_stream(stream, fieldnames, data):
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

def save_json_stream(stream, data):
        json.dump(data, stream, indent=4)
