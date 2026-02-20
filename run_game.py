import players.random_player as random_player
import players.human_player as human_player
from enumerations import PlayerCode
from truco_gen import Mesa
from nodes import MCTSNode
from copy import deepcopy
import functions
import argparse
import random
import time

def get_cmd_args():
    parser = argparse.ArgumentParser(description='MCTS Truco by Acauã')

    parser.add_argument('-t', '--time', default='1', type=int, help='Tempo, em segundos, que a MCTS terá para realizar as simulações')
    parser.add_argument('-s', '--simulations', type=int, help='Indica que vamos usar o usuário aleatório e a quantidade de jogos de teste')
    # parser.add_argument('-pn', '--player-name', help='Nome do jogador')
    parser.add_argument('-hm', '--hide-messages', action='store_true')

    return parser.parse_args()

def mcts_search(root_state, tempo=1):
    root = MCTSNode(deepcopy(root_state), player=None)

    # State precisa dar cartas aleatórias para o oponente para a simulação ser justa
    if len(root.state.card_player) != 0 and root.state.card_player[0] in root.state.known_deck:
        root.state.known_deck.remove(root.state.card_player[0])
    for i in range(len(root.state.hand_player)):
        root.state.hand_player[i] = root.state.known_deck[i]

    iterations = 0
    ts = time.time()
    # for i in range(iterations):
    while((time.time() - ts) < tempo):
        iterations+= 1
        # print(f"Iniciando nova simulação {i+1}/{iterations}")
        node = root

        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()

        if not node.is_terminal() and not node.is_fully_expanded():
            node = node.expand()

        winner = node.rollout()
        node.backpropagate(winner)
    # print(f'{iterations} interações')
    best = max(root.children, key=lambda c: c.visits)
    return best.action

def play_game(args):
    current_player = random.choice([PlayerCode.RANDOMPLAYER.name, PlayerCode.MCTSPLAYER.name])
    mesa_de_jogo = Mesa(current_player)
    
    if args.simulations is None:
        challenger = human_player
        max_jogos = 1
    else:
        challenger = random_player
        max_jogos = args.simulations
    
    jogos = 1
    mcts_ganhou = 0
    random_ganhou = 0
    while(jogos <= max_jogos):
        if not args.hide_messages:
            mesa_de_jogo.print_mesa(jogos)

        if current_player == PlayerCode.MCTSPLAYER.name:
            move = mcts_search(mesa_de_jogo, args.time)
            if not args.hide_messages:
                mesa_de_jogo.anunciar_movimento(move)
            mesa_de_jogo.play_cards(move, args.hide_messages)
        else:
            move = challenger.choose_move(mesa_de_jogo)
            if not args.hide_messages:
                mesa_de_jogo.anunciar_movimento(move)
            mesa_de_jogo.play_cards(move, args.hide_messages)

        current_player = mesa_de_jogo.next_player

        winner = functions.check_winner_state(mesa_de_jogo)
        if winner:
            if winner == PlayerCode.MCTSPLAYER.name:
                mcts_ganhou+= 1
            else:
                random_ganhou+= 1
            print(f"{winner} ganhou!!! Chupa que é de uva!")
            if not args.hide_messages:
                mesa_de_jogo.print_mesa(jogos)
            mesa_de_jogo = Mesa(current_player)
            jogos+= 1
            # return
        if not args.hide_messages:
            print('------------------------------------------------')
    
    print(f'\nVitórias MCTS: {mcts_ganhou}/{jogos-1} ({mcts_ganhou/(jogos-1)})')
    print(f'\nVitórias Random: {random_ganhou}/{jogos-1} ({random_ganhou/(jogos-1)})')

if __name__ == "__main__":
    play_game(get_cmd_args())