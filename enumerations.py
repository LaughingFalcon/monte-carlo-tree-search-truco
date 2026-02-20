from enum import Enum

class PlayerCode(Enum):
    NOBODY = 0
    RANDOMPLAYER = 1
    MCTSPLAYER = 2

class PlayerMoves(Enum):
    TRUCO = '1'
    CORRER = '2'
    DESCER = '3'
    AUMENTAR = '4'