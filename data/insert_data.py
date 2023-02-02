import mysql.connector
from random import randint, choice
import csv

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="auditapp"
)

mycursor = mydb.cursor()

def insert_to_db(sql, data):
    mycursor.executemany(sql, data)
    mydb.commit()

def insert_regulators():
    sql = "INSERT INTO partner_regulator (id, regulator_name) VALUES (%s, %s)"
    val = []

    with open('regulators.csv', 'r') as csv_file:
        # reading the csv
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = []
        for row in csv_reader:
            id = row[0]
            name = row[1]
            val.append((id, name))
    # print(val)
    insert_to_db(sql, val)

def insert_industries():
    sql = "INSERT INTO partner_industry (id, industry_name) VALUES (%s, %s)"
    val = []

    with open('industries.csv', 'r') as csv_file:
        # reading the csv
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = []
        for row in csv_reader:
            id = row[0]
            name = row[1]
            val.append((id, name))
    print(val)
    insert_to_db(sql, val)

def insert_entities():
    sql = "INSERT INTO partner_entity (id, entity_name) VALUES (%s, %s)"
    val = []

    with open('entities.csv', 'r') as csv_file:
        # reading the csv
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = []
        for row in csv_reader:
            id = row[0]
            name = row[1]
            val.append((id, name))
    # print(val)
    insert_to_db(sql, val)

def insert_acts():
    sql = "INSERT INTO partner_act (id, entity_name) VALUES (%s, %s)"
    val = []

    with open('entities.csv', 'r') as csv_file:
        # reading the csv
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = []
        for row in csv_reader:
            id = row[0]
            name = row[1]
            val.append((id, name))
    # print(val)
    insert_to_db(sql, val)

def insert_task():
    sql = "INSERT INTO partner_task (task_name, task_estimated_days, task_auditing_standard, task_international_auditing_standard) VALUES (%s, %s, %s, %s)"
    val = []

    for i in range(1, 25):
        val.append(("Company Task {}".format(i), randint(1, 30), choice(["ISO", "OIS", "RIP"]), choice(["UNESCO", "WHO", "IETE"])))
    print(val)

    mycursor.executemany(sql, val)

def insert_task_activities():
    sql = "INSERT INTO partner_task_activity (task_id, activity_id) VALUES (%s, %s)"
    val = []

    for i in range(52, 75):
        val.append((i, 2))
    print(val)

    mycursor.executemany(sql, val)

# insert_task_activities()
# insert_entities()
# insert_industries()
# insert_regulators()
insert_acts()



print(mycursor.rowcount, "was inserted.")