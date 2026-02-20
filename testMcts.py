from enumerations import PlayerCode
from nodes import MCTSNode
from truco_gen import Mesa
from copy import deepcopy
import functions
import random
import time

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
    print(f'{iterations} interações')
    best = max(root.children, key=lambda c: c.visits)
    return best.action

def play_game():
    current_player = random.choice([PlayerCode.RANDOMPLAYER.name, PlayerCode.MCTSPLAYER.name])
    mesa_de_jogo = Mesa(current_player)
    
    print("MCTS Truco Demo")
    jogos = 1
    mcts_ganhou = 0
    random_ganhou = 0
    while(jogos <= 1):
        mesa_de_jogo.print_mesa(jogos)

        if current_player == PlayerCode.MCTSPLAYER.name:
            # print(f'Iniciando jogada de {current_player}')
            move = mcts_search(mesa_de_jogo)
            mesa_de_jogo.anunciar_movimento(move)
            mesa_de_jogo.play_cards(move, False)
            # mesa_de_jogo.play_cards(move)
        else:
            # print(f'Iniciando jogada de {current_player}')
            moves = mesa_de_jogo.available_actions()
            # selected_move = random.choice(moves)
            selected_move = ''
            while(selected_move not in moves):
                print('Escolha seu movimento')
                selected_move = input(f'{moves}: ')

            mesa_de_jogo.anunciar_movimento(selected_move)
            mesa_de_jogo.play_cards(selected_move, False)
            # mesa_de_jogo.play_cards(move)

        current_player = mesa_de_jogo.next_player

        winner = functions.check_winner_state(mesa_de_jogo)
        if winner:
            if winner == PlayerCode.MCTSPLAYER.name:
                mcts_ganhou+= 1
            else:
                random_ganhou+= 1
            print(f"{winner} ganhou!!! Chupa que é de uva!")
            mesa_de_jogo.print_mesa(jogos)
            mesa_de_jogo = Mesa(current_player)
            jogos+= 1
            # return
        print('------------------------------------------------')
    
    print(f'\nVitórias MCTS: {mcts_ganhou}/{jogos-1} ({mcts_ganhou/(jogos-1)})')
    print(f'\nVitórias Random: {random_ganhou}/{jogos-1} ({random_ganhou/(jogos-1)})')

if __name__ == "__main__":
    play_game()