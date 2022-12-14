import mysql.connector
from mysql.connector import errorcode
import argparse
import matplotlib.pyplot as plt
import getpass as gp
from visualize_utilities.menu_mode import main_menu
from visualize_utilities.sql_helper import print_query
import database_strings as dbs
from create_database import create_database


# LOGIN CREDS NEED TO BE CHANGED TO YOUR DB
database_name = "NyingiDatabase"
host = "localhost"
user = "test"
password = "password"


"""Visualization tool"""

# Init Argument Parser
msg = "Learning Game Analytics Visualizer"
parser = argparse.ArgumentParser(description=msg)

# Add Optional Arguments
parser.add_argument("-p", "--plot", help = "Plot 2 Collumn SQL Table [Requires -q]", action = "store_true")
parser.add_argument("-q", "--query", metavar = "SQL Query", help = "Return SQL Query Result")

# Read arguments from command line
args = parser.parse_args()

# Attempt to open a database connection
try:
    cnx = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name)

# Catch DB Exeptions
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
        exit()
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        width = 55
        print("+" + "-"*(width - 2) + "+")
        print(f"|{'Create New Database':^{width - 2}}|")
        print("+" + "-"*(width - 2) + "+")
        
        database_name = "NyingiDatabase"
        host = input("Enter Host: ")
        user = input("Enter User: ")
        password = gp.getpass(prompt = "Enter password: ")

        nyingi_query_list = [
                dbs.Create_BoardDif,
                dbs.Create_CardDif,
                dbs.Create_GameTable,
                dbs.Create_Player_Events]
        try:
            create_database(host, user, password, database_name, nyingi_query_list)
            cnx = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database_name)
        except:
            print("ERROR: Failed to create DB")
    else:
        print(err)
        exit()


# Attempt to run SQL query
if args.query:
    # Get headers and result from sql query
    table = print_query(cnx, args.query)

    if table:
        headers, result = table
    else:
        exit()

    # Graph the first two collumns as an x and y plot
    if args.plot:
        # Flip the rows and collumns
        data = {}
        for index in range(len(result[0])):
            data[headers[index]] = [row[index] for row in result]
        
        for row in data.values():
            for index in range(len(row)):
                row[index] = str(row[index])
        
        # Plot the data
        plt.scatter(data[headers[0]], data[headers[1]])
        plt.xlabel(headers[0])
        plt.ylabel(headers[1])
        plt.show()

else:
    main_menu(cnx)

cnx.close()