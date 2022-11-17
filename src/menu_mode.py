import time
import os
from sql_helper import print_querry
import matplotlib.pyplot as plt


def main_menu(cnx):
    width = 50
    header = f"|{'Interactive Visualize.py Mode':^{width - 2}}|"
    menu_items = [
            "Show All Tables",
            "Run Querry",
            "Show Game By ID",
            "Plot Avg. Play Time Vs. Square Number",
            "Exit"
        ]
    
    def print_header():
        print("+" + "-"*(width - 2) + "+")
        print(header)
        print("+" + "-"*(width - 2) + "+")
    
    def print_menu():
        for index, item in enumerate(menu_items):
            string = " "*(width//8) + f"{index + 1})  {item}"
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
        
        elif user_option == 4:
            querry = """
            SELECT play_time, cards_used, inputs
            FROM PlayerEvents JOIN CardDiff
            ON PlayerEvents.card_diff_id=CardDiff.card_diff_id
            WHERE is_swap=0
            """
            table = print_querry(cnx, querry)

            if table:
                headers, result = table
            else:
                continue

            # Flip the rows and collumns
            axis_data = {}
            
            # Calculate space number and total time to play
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
            plt.bar(list(axis_data.keys()), list(axis_data.values()), width=0.5, color='blue')
            plt.xlabel("Board Number")
            plt.ylabel("Average Play Time (seconds)")
            plt.show()
        
        print("\n")
        input("Press enter to go back to the menu...")
        print("\n")

