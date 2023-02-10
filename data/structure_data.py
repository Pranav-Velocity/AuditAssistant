import os
import csv

file_name = "entities.csv"
new_file_name = "new_entities.csv"

def read_csv():
    with open(file_name, 'r') as csv_file:
        # reading the csv
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = []
        index = 1
        for row in csv_reader:
            row = row[:2]
            row[0] = str(index)
            row[1] = str(row[1]).strip()
            index += 1
            data.append(row)
    return data


def write_csv(data):
    # opening the file in write mode
    with open(new_file_name, 'w', newline='') as csv_file:
        # writing to the csv
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in data:
            csv_writer.writerow(row)

write_csv(read_csv())