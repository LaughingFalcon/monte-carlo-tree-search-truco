import random

def choose_move(mesa_de_jogo):
    moves = mesa_de_jogo.available_actions()
    return random.choice(moves)