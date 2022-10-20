"""Defines game event objects"""
from typing import List


class EventContainer(object):
    def __init__(self, EVENTID: int, Timestamp: str,  jsonString: str):
        self.event_id = EVENTID
        self.timestamp = Timestamp
        self.json_string = jsonString


class MetadataStruct(object):
    def __init__(self, Description: str, GameName: str):
        self.description = Description
        self.game_name = GameName


class PlayerSwapStruct(object):
    def __init__(self, Description: str, PlayerNum: int, SwappedCards: List):
        self.description = Description
        self.player_num = PlayerNum
        self.swapped_cards = SwappedCards


class PlayerMoveStruct(object):
    def __init__(self, Description: str, PlayerNum: int, CardsPlayed: List,
                 Successful: bool, SquareID: List):
        self.description = Description
        self.player_num = PlayerNum
        self.cards_played = CardsPlayed
        self.is_successful = Successful
        self.square_id = SquareID


class CardDrawnStruct(object):
    def __init__(self, Description: str, CardValue: str):
        self.description = Description
        self.card_value = CardValue


class GameOverStruct(object):
    def __init__(self, Description: str, WinnerNum: int):
        self.description = Description
        self.winner_num = WinnerNum


class GameStartStruct(object):
    def __init__(self, Description: str, difficulty: str, BoardSize: List,
                 numberRange: List):
        self.description = Description
        self.difficulty = difficulty
        self.board_size = BoardSize
        self.number_range = numberRange


class DeckRefreshStruct(object):
    def __init__(self, Description: str):
        self.description = Description


class PlyaerInputStruct(object):
    def __init__(self, Description: str, Type: str, Value: str):
        self.description = Description
        self.type = Type
        self.value = Value


class BoardInitStruct(object):
    def __init__(self, Description: str, BoardTiles: List):
        self.description = Description
        self.board_tiles = BoardTiles
