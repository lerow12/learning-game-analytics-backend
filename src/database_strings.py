
Create_Player_Events = "CREATE TABLE PlayerEvents\
(event_id INT AUTO_INCREMENT PRIMARY KEY, \
player_num INT NOT NULL, player_id INT, \
is_swap BIT NOT NULL, is_successful BIT, \
timestamp TIMESTAMP, play_time TIME, \
card_diff_id INT, board_diff_id INT, game_id INT, \
FOREIGN KEY (card_diff_id) REFERENCES CardDiff(card_diff_id), \
FOREIGN KEY (board_diff_id) REFERENCES BoardDiff(board_diff_id), \
FOREIGN KEY (game_id) REFERENCES GameTable(game_id));"

# hand is hand before play
Create_CardDif = "CREATE TABLE CardDiff\
(card_diff_id INT AUTO_INCREMENT PRIMARY KEY, \
hand VARCHAR(20), cards_used VARCHAR(20), \
cards_gained VARCHAR(20), player_num INT);"

# taken_matrix is taken state before play.
Create_BoardDif = "CREATE TABLE BoardDiff\
(board_diff_id INT AUTO_INCREMENT PRIMARY KEY, \
x INT, y INT, \
taken_matrix VARBINARY(256), player_num INT);"

Create_GameTable = "CREATE TABLE GameTable\
(game_id INT AUTO_INCREMENT PRIMARY KEY, \
board_area INT, max_value INT, computer_difficulty VARCHAR(10), \
game_name VARCHAR(32), board_state VARCHAR(256), winner INT, \
computer_hand VARCHAR(20), \
player_hand VARCHAR(20));"
