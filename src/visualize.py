import mysql.connector
from mysql.connector import errorcode
import argparse


# Temp Creds
database_name = "NyingiDatabase"
host = "localhost"
user = "test"
password = "password"

def print_row(max_width, row):
    print("| ", end="")
    width = max_width
    for arg in row:
        print(f"{arg:^{width}} | ", end="")
    print()

"""Visualization tool"""

# Init Argument Parser
msg = "Learning Game Analytics Visualizer"
parser = argparse.ArgumentParser(description=msg)

# Add Optional Arguments
parser.add_argument("-q", "--querry", metavar = "SQL Querry", required = True, help = "Return SQL Querry Result")

# Read arguments from command line
args = parser.parse_args()

# Attempt to run SQL Querry
try:
    cnx = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name)
    db_cursor = cnx.cursor()
    db_cursor.execute(args.querry)
    result = db_cursor.fetchall()

    # Get the length of the longest cell in a row
    max_width = 0
    for row in result:
        max_width = max(max_width, max(list(map(len, (map(str, row))))))

    # Format print each row
    for row in result:
        print_row(max_width, row)

    db_cursor.close()

# Catch DB Exeptions
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

# Close DB
else:
    cnx.close()

