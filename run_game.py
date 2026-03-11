import players.random_player as random_player
import players.human_player as human_player
from players.mcts_player import MctsPlayer
from players.mcts_double import MctsPlayer as MctsDouble
from enumerations import PlayerCode
from truco_gen import Mesa
import functions
import argparse
import random

def get_cmd_args():
    parser = argparse.ArgumentParser(description='MCTS Truco by Acauã')

    parser.add_argument('-t', '--time', default='1', type=int, help='Tempo, em segundos, que a MCTS terá para realizar as simulações.')
    parser.add_argument('-s', '--simulations', type=int, help='Quantidade de jogos de teste. Ssuário aleatório será utilizado neles.')
    parser.add_argument('-md', '--mcts-double', action='store_true', help='Indica que usaremos o usuário MCTS nos testes.')
    # parser.add_argument('-pn', '--player-name', help='Nome do jogador')
    parser.add_argument('-hm', '--hide-messages', action='store_true')

    return parser.parse_args()

def play_game(args):
    current_player = random.choice([PlayerCode.CHALLENGERPLAYER.name, PlayerCode.MCTSPLAYER.name])
    mesa_de_jogo = Mesa(current_player)

    mcts_killer = MctsPlayer(args.time)
    if args.simulations is None:
        challenger = human_player
        max_jogos = 1
    else:
        challenger = MctsDouble(args.time) if args.mcts_double else random_player
        max_jogos = args.simulations
    
    jogos = 1
    mcts_ganhou = 0
    random_ganhou = 0
    while(jogos <= max_jogos):
        if not args.hide_messages:
            mesa_de_jogo.print_mesa(jogos)

        if current_player == PlayerCode.MCTSPLAYER.name:
            move = mcts_killer.choose_move(mesa_de_jogo)
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
    print(f'\nVitórias Desafiante: {random_ganhou}/{jogos-1} ({random_ganhou/(jogos-1)})')

if __name__ == "__main__":
    play_game(get_cmd_args())