"""Defines game event objects"""
from typing import List
import json


class EventContainer(object):
    def _init_self(self, EVENTID: int, Timestamp: str,  jsonString: str):
        self.EVENTID = EVENTID
        self.Timestamp = Timestamp
        self.jsonString = jsonString


class MetadataStruct(object):
    def _init_self(self, Description: str, GameName: str):
        self.Description = Description
        self.GameName = GameName


class PlayerSwapStruct(object):
    def _init_self(self, Description: str, PlayerNum: int, SwappedCards: List):
        self.Description = Description
        self.PlayerNum = PlayerNum
        self.SwappedCards = SwappedCards


class PlayerMoveStruct(object):
    def _init_self(self, Description: str, PlayerNum: int, CardsPlayed: List, Successful: bool, SquareId: List):
        self.Description = Description
        self.PlayerNum = PlayerNum
        self.CardsPlayed = CardsPlayed
        self.Successful = Successful
        self.SquareId = SquareId


class CardDrawnStruct(object):
    def _init_self(self, Description: str, CardValue: str):
        self.Description = Description
        self.CardValue = CardValue


class GameOverStruct(object):
    def _init_self(self, Description: str, WinnerNum: int):
        self.Description = Description
        self.WinnerNum = WinnerNum


class GameStartStruct(object):
    def _init_self(self, Description: str, difficulty: str, BoardSize: List, numberRange: List):
        self.Description = Description
        self.difficulty = difficulty
        self.BoardSize = BoardSize
        self.numberRange = numberRange


class DeckRefreshStruct(object):
    def _init_self(self, Description: str):
        self.Description = Description


class PlyaerInputStruct(object):
    def _init_self(self, Description: str, Type: str, Value: str):
        self.Description = Description
        self.Type = Type
        self.Value = Value


class BoardInitStruct(object):
    def _init_self(self, Description: str, BoardTiles: List):
        self.Description = Description
        self.BoardTiles = BoardTiles
