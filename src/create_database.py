import mysql.connector
import database_strings as dbs 
"""Repackages events and stores them in mysql database"""
# Temporary Credentials. Replace with your own to test.
database_name = "NyingiDatabase"
host = "localhost"
user = "test"
password = "password"
nyingi_query_list = [
        dbs.Create_BoardDif,
        dbs.Create_CardDif,
        dbs.Create_GameTable,
        dbs.Create_Player_Events]


def delete_database(host, user, password, database_name):
    init_database = mysql.connector.connect(
        host=host,
        user=user,
        password=password
        )
    init_db_cursor = init_database.cursor()
    init_db_cursor.execute("DROP DATABASE IF EXISTS {};".format(database_name))
    init_db_cursor.close()


def create_database(host, user, password, database_name, query_list):
    init_database = mysql.connector.connect(
        host=host,
        user=user,
        password=password)
    init_db_cursor = init_database.cursor()
    init_db_cursor.execute("CREATE DATABASE {};".format(database_name))
    init_db_cursor.close()
    create_tables(host, user, password, database_name, query_list)


def create_tables(host, user, password, database_name, query_list):
    init_database = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name)
    init_db_cursor = init_database.cursor()
    for query in query_list:
        init_db_cursor.execute(query)

create_database(host, user, password, database_name, nyingi_query_list)
