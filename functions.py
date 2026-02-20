from enumerations import PlayerMoves
from enumerations import PlayerCode

# def available_actions(state):
#     if state.tah_trucando:
#         if state.truco[1] < 12:
#             return [PlayerMoves.CORRER.name, PlayerMoves.AUMENTAR.name, PlayerMoves.DESCER.name]
#         else:
#             return [PlayerMoves.CORRER.name, PlayerMoves.DESCER.name]

#     if state.next_player == PlayerCode.RANDOMPLAYER.name: 
#         actions = deepcopy(state.hand_player)
#     else:
#         actions = deepcopy(state.hand_mcts)
#     if state.truco[0] != state.next_player and state.truco[1] < 12 and state.points_mcts != 11 and state.points_player != 11:
#         actions.append(PlayerMoves.TRUCO.name)
#     random.shuffle(actions)
#     return actions

def check_winner_state(state):
    if state.points_player >= 12:
        return PlayerCode.RANDOMPLAYER.name
    if state.points_mcts >= 12:
        return PlayerCode.MCTSPLAYER.name
    return None

# def get_current_player(state):
#     return state.next_player

def get_next_player(current_player):
    return PlayerCode.RANDOMPLAYER.name if current_player == PlayerCode.MCTSPLAYER.name else PlayerCode.MCTSPLAYER.name
