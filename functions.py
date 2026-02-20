from enumerations import PlayerMoves
from enumerations import PlayerCode

def check_winner_state(state):
    if state.points_player >= 12:
        return PlayerCode.RANDOMPLAYER.name
    if state.points_mcts >= 12:
        return PlayerCode.MCTSPLAYER.name
    return None

def get_next_player(current_player):
    return PlayerCode.RANDOMPLAYER.name if current_player == PlayerCode.MCTSPLAYER.name else PlayerCode.MCTSPLAYER.name
