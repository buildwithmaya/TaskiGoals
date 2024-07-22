import mysql.connector
import MySQLdb
import pymysql

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE IF NOT EXISTS Tasks_app")

