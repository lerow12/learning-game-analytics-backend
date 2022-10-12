
Create_Player_Events = "CREATE TABLE PlayerEvents\
(event_id INT AUTO_INCREMENT PRIMARY KEY, \
player_num INT NOT NULL, player_id INT, \
is_swap BIT NOT NULL, is_game_over BIT DEFAULT 0, \
timestamp TIMESTAMP, card_diff_id INT, board_diff_id INT, game_id INT, \
FOREIGN KEY (card_diff_id) REFERENCES CardDiff(card_diff_id), \
FOREIGN KEY (board_diff_id) REFERENCES BoardDiff(board_diff_id), \
FOREIGN KEY (game_id) REFERENCES GameTable(game_id));"

Create_CardDif = "CREATE TABLE CardDiff\
(card_diff_id INT AUTO_INCREMENT PRIMARY KEY, \
hand VARBINARY(7), cards_lost VARBINARY(7), \
cards_gained VARBINARY(7), player_num INT);"

Create_BoardDif = "CREATE TABLE BoardDiff\
(board_diff_id INT AUTO_INCREMENT PRIMARY KEY, \
x INT, y INT, val INT, board_state VARBINARY(256), \
taken_matrix VARBINARY(256), player_num INT);"

Create_GameTable = "CREATE TABLE GameTable\
(game_id INT AUTO_INCREMENT PRIMARY KEY, \
board_area INT, max_value INT, computer_difficulty VARCHAR(10), \
game_name VARCHAR(32), board_state VARBINARY(256), \
computer_hand VARBINARY(7), \
player_hand VARBINARY(7));"
