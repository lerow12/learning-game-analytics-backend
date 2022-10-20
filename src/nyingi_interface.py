"""Unpacks game events into objects"""

from math import isqrt
import re
import src.nyingi_event_structure as ne
import src.database_calls as dc
from json import loads as jsonLoad
from datetime import datetime

class SQLGameStart():
    def __init__(self):
        self.board_area = 0
        self.max_value = 0
        self.computer_difficulty = ""
        self.game_name = ""
        self.board_state = []
        self.winner = 0
        self.computer_hand = []
        self.player_hand = []
    def __str__(self) -> str:
        return f"{vars(self)}"

class SQLPlayerEvent():
    def __init__(self):
        self.player_num = 0
        self.player_id = -1
        self.is_swap = 0
        self.is_successful = 1
        self.timestamp = ""
        self.play_time = 0
        self.card_diff_id = 0
        self.board_diff_id = 0
        self.game_id = 0

class SQLBoardDiff():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.val = 0
        self.taken_matrix = []
        self.player_num = 0

event_classes = {
    0: ne.MetadataStruct,
    2: ne.GameStartStruct,
    3: ne.CardDrawnStruct,
    4: ne.BoardInitStruct,
    5: ne.PlyaerInputStruct,
    6: ne.PlayerSwapStruct,
    7: ne.PlayerMoveStruct,
    8: ne.GameOverStruct,
    9: ne.DeckRefreshStruct
}

event_types = {
    "game_start": 2,
    "card_draw": 3,
    "board_init": 4,
    "player_input": 5,
    "player_swap": 6,
    "player_move": 7,
    "game_over": 8,
    "deck_refresh": 9
}


def unpack_nyingi_events(events):
    global event_classes
    objects = []
    for event in events:
        class_type = event_classes[event.event_id]
        objects.append((event.event_id, event.timestamp, class_type(**jsonLoad(event.json_string))))
    rebuild_game(objects)


def rebuild_game(objects):
    gameStartEvents = []
    playerEvents = []
    for event in objects:
        eventType = event[0]
        if (eventType in [0, 2, 8, 3, 4]):
            gameStartEvents.append(event)
        if (eventType in [7, 3, 5, 2, 6]):
            playerEvents.append(event)
    game_structures = extractGames(gameStartEvents)
    game_ids = []
    for game in game_structures:
        game_ids.append(dc.save_game_table(game.board_area, game.max_value, game.computer_difficulty, game.game_name, game.board_state, game.winner, game.computer_hand, game.player_hand))
    player_events = extractPlayerEvents(playerEvents, game_ids)
    for player_event in player_events:
        dc.save_player_events(player_event.player_num, player_event.player_id, player_event.is_swap, player_event.is_successful, player_event.timestamp, player_event.play_time, 0, player_event.board_diff_id, player_event.game_id )

def extractGames(eventQueue):
    games = []
    # Fun fact: Lists evaluate to true in python while they are not empty!
    # This may be the worst piece of code I've ever written.
    currentGame = SQLGameStart() 
    inGame = False
    while(eventQueue):
        curEvent = eventQueue.pop(0)
        eventType = curEvent[0]
        eventObject = curEvent[2]
        eventTS = curEvent[1]
        if (eventType == 0):
            if (inGame):
                games.append(currentGame)
                currentGame = SQLGameStart() 
                currentGame.game_name = eventObject.game_name
            else:
                currentGame.game_name = eventObject.game_name
                inGame = True
        if (eventType == 2):
            currentGame.computer_difficulty = eventObject.difficulty 
            currentGame.board_area = eventObject.board_size[0] * eventObject.board_size[1]
            currentGame.max_value = eventObject.number_range[0] * eventObject.number_range[1]
            for x in range(7):
                playerDrawEvent = eventQueue.pop(0)
                if (playerDrawEvent[0]==3):
                    card_value = playerDrawEvent[2].card_value
                    if (card_value == "Prime"):
                        card_value = 'P'
                    elif (card_value == "Wild"):
                        card_value = 'W'
                    currentGame.player_hand.append(card_value)
                else:
                    # If we don't even draw all the cards the data can't possibly be that useful.
                    currentGame = SQLGameStart()
                computerDrawEvent = eventQueue.pop(0)
                if (computerDrawEvent[0]==3):
                    card_value = playerDrawEvent[2].card_value
                    if (card_value == "Prime"):
                        card_value = 'P'
                    elif (card_value == "Wild"):
                        card_value = 'W'
                    currentGame.computer_hand.append(card_value)
                else:
                    currentGame = SQLGameStart()
        if(eventType == 4):
            currentGame.board_state = eventObject.board_tiles
        if(eventType == 8):
            inGame = False
            currentGame.winner = eventObject.winner_num
            games.append(currentGame)
            currentGame = SQLGameStart()
    if(inGame):
        games.append(currentGame)
    return games
                

def extractPlayerEvents(eventQueue, game_ids):
    #Here there be dragons
    playerEvents = []
    activeEvent = SQLPlayerEvent()
    inEvent = False
    lastTimestamp = ""
    lastPlayerHand = []
    lastComputerHand = []
    currentBoardState = []
    board_vals = []
    game_id = 0
    board_size = 0
    
    while(eventQueue):
        curEvent = eventQueue.pop(0)
        eventType = curEvent[0]
        eventObject = curEvent[2]
        eventTS = curEvent[1]
        if (eventType == 2):
            lastTimestamp = eventTS
            board_size =  eventObject.board_size[0] * eventObject.board_size[1]
            currentBoardState = [0]*board_size
            game_id = game_ids.pop(0)
        if (eventType == 7):
            activeEvent.game_id = game_id
            activeEvent.is_swap = 0
            activeEvent.timestamp = convertToSQLTimestamp(eventTS)
            activeEvent.play_time = getTimestampDifference(lastTimestamp, eventTS)
            activeEvent.player_num = eventObject.player_num
            lastTimestamp=eventTS
            if (eventObject.is_successful == True):
                activeEvent.is_successful = 1
                diff = generateBoardDif(eventObject, currentBoardState, board_size)
                currentBoardState =   diff.taken_matrix
                board_diff_id = dc.save_board_diff(diff.x, diff.y, diff.taken_matrix, diff.player_num)
                activeEvent.board_diff_id = board_diff_id
            playerEvents.append(activeEvent)
            activeEvent = SQLPlayerEvent()
        if (eventType == 6):
            activeEvent.game_id = game_id
            activeEvent.is_swap = 1
            activeEvent.timestamp = convertToSQLTimestamp(eventTS)
            activeEvent.play_time = getTimestampDifference(lastTimestamp, eventTS)
            activeEvent.player_num = eventObject.player_num
            lastTimestamp=eventTS
            activeEvent.is_successful = 1
            playerEvents.append(activeEvent)
            activeEvent = SQLPlayerEvent()
    return playerEvents
            


def generateCardDif():
    pass

def generateBoardDif(play, last_board_state, board_size):
    diff = SQLBoardDiff()
    diff.x = play.square_id[0]
    diff.y = play.square_id[1]
    diff.player_num = play.player_num
    diff.taken_matrix = last_board_state.copy()
    offset = diff.y*isqrt(board_size)+diff.x
    diff.taken_matrix[offset] =1
    return diff

def getTimestampDifference(early, late):
    fmt = '%m/%d/%Y %I:%M:%S %p'
    earlystamp =  datetime.strptime(early, fmt)
    latestamp = datetime.strptime(late, fmt)
    time_elapsed = latestamp-earlystamp
    return time_elapsed

def convertToSQLTimestamp(time):
     fmt = '%m/%d/%Y %I:%M:%S %p'
     goal = '%Y-%m-%d %H:%M:%S'
     raw_time=datetime.strptime(time, fmt)
     return raw_time


