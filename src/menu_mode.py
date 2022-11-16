import mysql.connector
import time
from print_helper import get_max_widths, print_row


def main_menu(cnx):
    width = 50
    header = f"|{'Interactive Visualize.py Mode':^{width - 2}}|"
    menu_items = [
            "Show All Tables",
            "Exit"
        ]
    
    def print_header():
        print("+" + "-"*(width - 2) + "+")
        print(header)
        print("+" + "-"*(width - 2) + "+")
    
    def print_menu():
        for index, item in enumerate(menu_items):
            string = " "*(width//4) + f"{index + 1})  {item}"
            print(f"{string:{width}}")

    while(True):
        print_header()
        print_menu()
        user_input = input("\nSelect Option: ")

        user_option = len(menu_items)
        try:
            user_option = int(user_input)
        except:
            print("\n\nInvalid Option")
            time.sleep(1)
            print("\n")
            continue

        if user_option < 1 or user_option > len(menu_items):
            print("\n\nInvalid Option")
            time.sleep(1)
            print("\n")
            continue
    
        if user_option == len(menu_items):
            print("Exiting...")
            return
        
        elif user_option == 1:
            db_cursor = cnx.cursor()
            db_cursor.execute("SHOW TABLES;")

            # Get results and headers
            headers = [header[0] for header in db_cursor.description]
            result = db_cursor.fetchall()

            print("\n")

            # Get the length of the longest cell in a collumn and store it in max_widths
            max_widths = get_max_widths(headers, result)
            
            # Format print the collumn headers
            print_row(max_widths, headers, header=True)

            # Format print each row
            for row in result:
                print_row(max_widths, row)

            db_cursor.close()
            print("\n")
            input("Press enter to go back to the menu...")
            print("\n")

