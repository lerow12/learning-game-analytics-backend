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

# Attempt to run SQL Querry
try:
  cnx = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name)
  db_cursor = cnx.cursor()
  db_cursor.execute(args.querry)
  for t in db_cursor:
    print(t)
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

