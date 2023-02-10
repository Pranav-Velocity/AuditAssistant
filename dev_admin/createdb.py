# DHomcPe4Ay
import mysql.connector
def createnewdatabase(dbname):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    port=3306,
    database="DHomcPe4Ay"
    )
    mycursor = mydb.cursor()

    sql = "CREATE DATABASE "+dbname

    mycursor.execute(sql)

