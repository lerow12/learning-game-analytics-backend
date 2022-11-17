import mysql.connector
from mysql.connector import errorcode
import argparse
import matplotlib.pyplot as plt
from visualize_utilities.menu_mode import main_menu
from visualize_utilities.sql_helper import print_querry


# Temp Creds
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
parser.add_argument("-q", "--querry", metavar = "SQL Querry", help = "Return SQL Querry Result")

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
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit()


# Attempt to run SQL Querry
if args.querry:
    # Get headers and result from sql querry
    table = print_querry(cnx, args.querry)

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