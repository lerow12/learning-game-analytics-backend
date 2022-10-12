import mysql.connector
import database_strings as dbs
"""Repackages events and stores them in mysql database"""
# Temporary Credentials. Replace with your own to test.
database_name = "NyingiDatabase"
host = "localhost"
user = "test"
password = "password"


def deleteDatabase(host, user, password, database_name):
    init_database = mysql.connector.connect(
        host=host,
        user=user,
        password=password
        )
    init_db_cursor = init_database.cursor()
    init_db_cursor.execute("DROP DATABASE IF EXISTS {};".format(database_name))
    init_db_cursor.close()


def createDatabase(host, user, password, database_name):
    init_database = mysql.connector.connect(
        host=host,
        user=user,
        password=password)
    init_db_cursor = init_database.cursor()
    init_db_cursor.execute("CREATE DATABASE {};".format(database_name))
    init_db_cursor.close()
    createTables(host, user, password, database_name)


def createTables(host, user, password, database_name):
    init_database = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name)
    init_db_cursor = init_database.cursor()
    query_list = [
        dbs.Create_BoardDif,
        dbs.Create_CardDif,
        dbs.Create_GameTable,
        dbs.Create_Player_Events]
    for query in query_list:
        init_db_cursor.execute(query)

# createDatabase(host, user, password, database_name)
# deleteDatabase(host, user, password, database_name)
