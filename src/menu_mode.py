import time
import os
from sql_helper import print_querry


def main_menu(cnx):
    width = 50
    header = f"|{'Interactive Visualize.py Mode':^{width - 2}}|"
    menu_items = [
            "Show All Tables",
            "Run Querry",
            "Show Game By ID",
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
        os.system("cls" if os.name == "nt" else "clear")
        print_header()
        print_menu()
        user_input = input("\nSelect Option: ")

        user_option = len(menu_items)
        try:
            user_option = int(user_input)
        except:
            os.system("cls" if os.name == "nt" else "clear")
            print("Invalid Option")
            time.sleep(1)
            continue

        if user_option < 1 or user_option > len(menu_items):
            os.system("cls" if os.name == "nt" else "clear")
            print("Invalid Option")
            time.sleep(1)
            continue
    
        if user_option == len(menu_items):
            print("Exiting...")
            return
        
        os.system("cls" if os.name == "nt" else "clear")
        
        if user_option == 1:
            print_querry(cnx, "SHOW TABLES;")
        
        elif user_option == 2:
            querry = input("Enter a querry: ")
            if querry:
                print()
                if not print_querry(cnx, querry):
                    continue
            else:
                os.system("cls" if os.name == "nt" else "clear")
                print("Invalid Querry")
                time.sleep(1)
                continue
        
        elif user_option == 3:
            game_id = input("Enter a game id: ")

            try:
                game_id = int(game_id)
            except:
                os.system("cls" if os.name == "nt" else "clear")
                print("Invalid Game ID")
                time.sleep(1)
                continue
            
            game_querry = f"""
            SELECT board_area, max_value, computer_difficulty, game_name, board_state, winner
            FROM GameTable
            WHERE game_id={game_id}
            """
            if not print_querry(cnx, game_querry):
                continue

            print()

            event_querry = f"""
            SELECT PlayerEvents.player_num, is_swap, is_successful, timestamp, play_time, x, y,
            hand, cards_used, inputs, cards_gained
            FROM PlayerEvents LEFT JOIN BoardDiff
            ON PlayerEvents.board_diff_id=BoardDiff.board_diff_id
            JOIN CardDiff
            ON PlayerEvents.card_diff_id=CardDiff.card_diff_id
            WHERE PlayerEvents.game_id={game_id}
            """
            if not print_querry(cnx, event_querry):
                continue
        
        print("\n")
        input("Press enter to go back to the menu...")
        print("\n")

