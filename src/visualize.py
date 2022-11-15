import mysql.connector
from mysql.connector import errorcode
import argparse


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
parser.add_argument("-q", "--querry", metavar = "SQL Querry", required = True, help = "Return SQL Querry Result")

# Read arguments from command line
args = parser.parse_args()


def print_row(max_width, row, header=False):
    """Prints a database table row with each cell the max_width size"""
    print("| ", end="")
    for arg in row:
        print(f"{arg:^{max_width}} | ", end="")
    print()
    if header:
        for _ in range((max_width + 3) * len(row) + 1):
            print("-", end="")
        print()


# Attempt to run SQL Querry
try:
    cnx = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name)
    db_cursor = cnx.cursor()
    db_cursor.execute(args.querry)

    # Get results and headers
    headers = [header[0] for header in db_cursor.description]
    result = db_cursor.fetchall()

    # Get the length of the longest cell in a row
    max_width = 0
    for header in headers:
        max_width = max(max_width, len(header))
    for row in result:
        max_width = max(max_width, max(list(map(len, (map(str, row))))))
    
    # Format print the collumn headers
    print_row(max_width, headers, header=True)

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

