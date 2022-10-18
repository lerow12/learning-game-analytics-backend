from src.database import *


def test_create_database():
    create_database(host, user, password, database_name, nyingi_query_list)
    delete_database(host, user, password, database_name)
