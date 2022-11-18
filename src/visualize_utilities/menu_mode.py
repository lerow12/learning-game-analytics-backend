import time
import os
import getpass as gp
from visualize_utilities.sql_helper import print_query
from create_database import delete_database
import subprocess as sp
import database_strings as dbs


def main_menu(cnx):
    width = 55
    header = f"|{'Interactive Visualize.py Mode':^{width - 2}}|"
    menu_items = [
            "Show All Tables",
            "Run Query",
            "Show Game By ID",
            "Plot DB Avg. Play Time Vs. Square Number",
            "Plot DB Frequency of Cards Used",
            "Plot DB Frequency of Cards Swapped",
            "Plot DB Wins vs Difficulty",
            "Delete DB",
            "Exit"
        ]
    
    def print_header():
        print("+" + "-"*(width - 2) + "+")
        print(header)
        print("+" + "-"*(width - 2) + "+")
    
    def print_menu():
        for index, item in enumerate(menu_items):
            string = " "*(width//8) + f"{index + 1})" + " "*(2 - ((index + 1) // 10)) + f"{item}"
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
        
        # OPTION 1
        if user_option == 1:
            print_query(cnx, "SHOW TABLES;")
        
        # OPTION 2
        elif user_option == 2:
            query = input("Enter a query: ")
            if query:
                print()
                if not print_query(cnx, query):
                    continue
            else:
                os.system("cls" if os.name == "nt" else "clear")
                print("Invalid Query")
                time.sleep(1)
                continue
        
        # OPTION 3
        elif user_option == 3:
            game_id = input(f"Enter a game id: ")

            try:
                game_id = int(game_id)
            except:
                os.system("cls" if os.name == "nt" else "clear")
                print("Invalid Game ID")
                time.sleep(1)
                continue
            
            query = """
            SELECT game_id
            FROM GameTable
            GROUP BY game_id
            """
            table = print_query(cnx, query)

            if table:
                _, result = table
            else:
                continue

            game_ids = set()
            [game_ids.add(row[0]) for row in result]

            if game_id not in game_ids:
                os.system("cls" if os.name == "nt" else "clear")
                print("Invalid Game ID")
                time.sleep(1)
                continue

            os.system("cls" if os.name == "nt" else "clear")
            print(f"Game_ID = {game_id}\n")
            
            game_query = f"""
            SELECT board_area, max_value, computer_difficulty, game_name, board_state, winner
            FROM GameTable
            WHERE game_id={game_id}
            """
            if not print_query(cnx, game_query):
                continue

            print()

            event_query = f"""
            SELECT PlayerEvents.player_num, is_swap, is_successful, timestamp, play_time, x, y,
            hand, cards_used, inputs, cards_gained
            FROM PlayerEvents LEFT JOIN BoardDiff
            ON PlayerEvents.board_diff_id=BoardDiff.board_diff_id
            JOIN CardDiff
            ON PlayerEvents.card_diff_id=CardDiff.card_diff_id
            WHERE PlayerEvents.game_id={game_id}
            """
            if not print_query(cnx, event_query):
                continue
        
        # OPTION 4
        elif user_option == 4:
            query = """
            SELECT play_time, cards_used, inputs
            FROM PlayerEvents JOIN CardDiff
            ON PlayerEvents.card_diff_id=CardDiff.card_diff_id
            WHERE is_swap=0 AND PlayerEvents.player_num=1 AND is_successful=1
            """
            table = print_query(cnx, query)

            if table:
                headers, result = table
            else:
                continue

            # Store axis data
            axis_data = {}
            
            # Calculate space number and total time to play per number
            for data in result:
                cards = data[1].split(" ")
                if data[2]:
                    input_cards = data[2].split(" ")
                    for input_card in input_cards:
                        cards.append(input_card)
                number = 1
                for card in cards:
                    try:
                        number *= int(card)
                    except:
                        pass
                number = str(number)
                if number in axis_data:
                    axis_data[number][0] += data[0].total_seconds()
                    axis_data[number][1] += 1
                else:
                    axis_data[number] = [data[0].total_seconds(), 1]
            
            # Calculate average time to play
            for key, value in axis_data.items():
                axis_data[key] = value[0] / value[1]

            # Plot the data
            plot_list = ["python3", "visualize_utilities/sql_helper.py"]
            plot_list.append(str(list(axis_data.keys())))
            plot_list.append(str(list(axis_data.values()))) 
            plot_list.append("Board Number") 
            plot_list.append("Average Play Time (seconds)")
            plot_list.append("Avg. Play Time Vs. Board Number")
            plot_list.append("bar")

            sp.Popen(plot_list)

        # OPTION 5
        elif user_option == 5:
            query = """
            SELECT cards_used
            FROM PlayerEvents JOIN CardDiff
            ON PlayerEvents.card_diff_id=CardDiff.card_diff_id
            WHERE PlayerEvents.player_num=1 AND is_swap=0
            """
            table = print_query(cnx, query)

            if table:
                _, result = table
            else:
                continue
            
            # Store axis data
            axis_data = {}

            for data in result:
                cards = data[0].split(" ")
                for card in cards:
                    if card in axis_data:
                        axis_data[card] += 1
                    else:
                        axis_data[card] = 1
            
            # Plot the data
            plot_list = ["python3", "visualize_utilities/sql_helper.py"]
            plot_list.append(str(list(axis_data.keys())))
            plot_list.append(str(list(axis_data.values()))) 
            plot_list.append("Frequency") 
            plot_list.append("Card Value")
            plot_list.append("Frequency of Played Cards")
            plot_list.append("barh")

            sp.Popen(plot_list)
        
        # OPTION 6
        elif user_option == 6:
            query = """
            SELECT cards_used
            FROM PlayerEvents JOIN CardDiff
            ON PlayerEvents.card_diff_id=CardDiff.card_diff_id
            WHERE PlayerEvents.player_num=1 AND is_swap=1
            """
            table = print_query(cnx, query)

            if table:
                _, result = table
            else:
                continue
            
            # Store axis data
            axis_data = {}

            for data in result:
                cards = data[0].split(" ")
                for card in cards:
                    if card in axis_data:
                        axis_data[card] += 1
                    else:
                        axis_data[card] = 1
            
            # Plot the data
            plot_list = ["python3", "visualize_utilities/sql_helper.py"]
            plot_list.append(str(list(axis_data.keys())))
            plot_list.append(str(list(axis_data.values()))) 
            plot_list.append("Frequency") 
            plot_list.append("Card Value")
            plot_list.append("Frequency of Swapped Cards")
            plot_list.append("barh")

            sp.Popen(plot_list)

        # OPTION 7
        elif user_option == 7:
            query = """
            SELECT computer_difficulty, COUNT(*)
            FROM GameTable
            WHERE winner=1
            GROUP BY computer_difficulty
            """
            table = print_query(cnx, query)

            if table:
                _, result = table
            else:
                continue

            # Store axis data
            axis_data = {}

            for data in result:
                axis_data[data[0]] = data[1]
            
            # Plot the data
            plot_list = ["python3", "visualize_utilities/sql_helper.py"]
            plot_list.append(str(list(axis_data.keys())))
            plot_list.append(str(list(axis_data.values()))) 
            plot_list.append("Computer Difficulty") 
            plot_list.append("Player Wins")
            plot_list.append("Wins Vs. Difficulty")
            plot_list.append("bar")

            sp.Popen(plot_list)
        
        # OPTION 8
        elif user_option == 8:
            database_name = "NyingiDatabase"
            host = input("Enter Host: ")
            user = input("Enter User: ")
            password = gp.getpass(prompt = "Enter password: ")

            cnx.close()
            try:
                delete_database(host, user, password, database_name)
            except:
                print("ERROR: Incorrect credentials")
            print("Exiting...")
            return

        
        print("\n")
        input("Press enter to go back to the menu...")
        print("\n")

