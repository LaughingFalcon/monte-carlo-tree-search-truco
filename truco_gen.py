from enumerations import PlayerMoves
from enumerations import PlayerCode
from copy import deepcopy
import functions
import random

class Mesa():
    def __init__(self, next_player):
        self.deck_base = [
            'AE', '2E', '3E', '4E', '5E', '6E', '7E', 'JE', 'QE', 'KE',
            'AC', '2C', '3C', '4C', '5C', '6C', '7C', 'JC', 'QC', 'KC',
            'AP', '2P', '3P', '4P', '5P', '6P', '7P', 'JP', 'QP', 'KP',
            'AO', '2O', '3O', '4O', '5O', '6O', '7O', 'JO', 'QO', 'KO'
        ]
        self.known_deck = deepcopy(self.deck_base)
        random.shuffle(self.known_deck)

        self.o_vira = self.known_deck.pop()
        self.hand_mcts = [self.known_deck.pop(), self.known_deck.pop(), self.known_deck.pop()]
        self.hand_player = [self.known_deck[0], self.known_deck[1], self.known_deck[2]]
        random.shuffle(self.known_deck)

        self.card_mcts = []
        self.card_player = []
        self.descarte = []

        self.points_mcts = 0
        self.points_player = 0
        self.turns_points = []

        self.truco = ['', 0]
        self.tah_trucando = ''
        self.next_player = next_player
        self.player_que_comeca = next_player
        self.last_move = ''

    def print_mesa(self, turn):
        print(f'Partida {turn}')
        print(f'Pontuação:')
        print(f' Jogador: {self.points_player}')
        print(f' Máquina: {self.points_mcts}\n')

        print(f'Mão jogador:')
        for card in self.hand_player:
            print(f' {self.card_name_converter(card)}', end=' ')
        print()
        # print(f'Mão máquina:')
        # for card in self.hand_mcts:
        #     print(f' {self.card_name_converter(card)}', end=' ')
        # print()

        print(f'O vira:')
        print(f' {self.card_name_converter(self.o_vira)}\n')

        if len(self.card_mcts) > len(self.card_player):
            print(f'{PlayerCode.MCTSPLAYER.name} jogou um {self.card_name_converter(self.card_mcts[-1])} na mesa')
        if len(self.card_player) > len(self.card_mcts):
            print(f'{PlayerCode.RANDOMPLAYER.name} jogou um {self.card_name_converter(self.card_player[-1])} na mesa')

        for i in range(len(self.turns_points)):
            match(self.turns_points[i]):
                case PlayerCode.MCTSPLAYER.value:
                    print(f'{PlayerCode.MCTSPLAYER.name} fez a {i+1}a')
                case PlayerCode.RANDOMPLAYER.value:
                    print(f'{PlayerCode.RANDOMPLAYER.name} fez a {i+1}a')
                case _:
                    print(f'A {i+1}a empatou')
        print()
    
    def anunciar_movimento(self, move):
        match(move):
            case PlayerMoves.CORRER.name:
                print(f'{self.next_player} arregou')
            case PlayerMoves.TRUCO.name:
                print(f'{self.next_player} gritou o nome do jogo e quer TRUCO!!!')
            case PlayerMoves.AUMENTAR.name:
                print(f'{self.next_player} botou o pau na mesa e quer aumentar a aposta!')
            case PlayerMoves.DESCER.name:
                print(f'{self.next_player} quer pagar pra ver!')
                print(f'{self.tah_trucando} torna')
            case _:
                print(f'{self.next_player} tá jogando um {self.card_name_converter(move)}')
    
    def anunciar_pontuacao(self, isSimulation, player, points):
        if not isSimulation:
            print(f'{player} fez {points} pontos')
 
    def set_new_hands(self):
        self.known_deck = deepcopy(self.deck_base)
        random.shuffle(self.known_deck)

        self.o_vira = self.known_deck.pop()
        self.hand_mcts = [self.known_deck.pop(), self.known_deck.pop(), self.known_deck.pop()]
        self.hand_player = [self.known_deck[0], self.known_deck[1], self.known_deck[2]]

        self.card_mcts = []
        self.card_player = []
        self.descarte = []

        self.turns_points = []

        self.truco = ['', 0]
        self.tah_trucando = ''

        self.next_player = ''
        self.last_move = ''

        self.player_que_comeca = PlayerCode.RANDOMPLAYER.name if self.player_que_comeca == PlayerCode.MCTSPLAYER.name else PlayerCode.MCTSPLAYER.name
        self.next_player = self.player_que_comeca
    
    def card_name_converter(self, card):
        nome = f'{card[0]} ' 
        match(card[1]):
            case 'O':
                nome+= 'Ouros'
            case 'E':
                nome+= 'Espadas'
            case 'C':
                nome+= 'Copas'
            case 'P':
                nome+= 'Paus'
        return nome if len(card) == 2 else card

    def card_value_converter(self, card):
        converter = {
            '3O':9,
            '3E':9,
            '3P':9,
            '3C':9,
            '2E':8,
            '2P':8,
            '2C':8,
            '2O':8,
            'AO':7,
            'AE':7,
            'AC':7,
            'AP':7,
            'KE':6,
            'KO':6,
            'KC':6,
            'KP':6,
            'JE':5,
            'JO':5,
            'JC':5,
            'JP':5,
            'QC':4,
            'QP':4,
            'QE':4,
            'QO':4,
            '7E':3,
            '7C':3,
            '7P':3,
            '7O':3,
            '6P':2,
            '6E':2,
            '6C':2,
            '6O':2,
            '5E':1,
            '5C':1,
            '5O':1,
            '5P':1,
            '4P':0,
            '4C':0,
            '4E':0,
            '4O':0
        }
        value = converter[card]
        value_vira = converter[self.o_vira] if converter[self.o_vira] < 9 else -1
        manilha = 0
        if value == (value_vira + 1):
            match(card[1]):
                case 'O':
                    manilha = 10
                case 'E':
                    manilha = 11
                case 'C':
                    manilha = 12
                case 'P':
                    manilha = 13
        return value + manilha
    
    def play_cards(self, action, isSimulation = True):
        match(action):
            case PlayerMoves.TRUCO.name:
                if self.truco[0] == self.next_player or self.truco[1] >= 12:
                    print('Truco inválido')
                    raise Exception(f"Impossível pedir truco nessa situação: {self.truco[0]}:{self.truco[1]}")
                # print(f'{self.next_player} TÁ PEDINDO TRUUUUUCO!!!!!')
                self.truco = [self.next_player, self.truco[1] + 3]
                self.tah_trucando = self.next_player
                self.next_player = functions.get_next_player(self.next_player)

            case PlayerMoves.CORRER.name:
                self.truco = [self.next_player, self.truco[1] - 3]
                self.update_points(action, self.next_player, isSimulation)

            case PlayerMoves.AUMENTAR.name:
                self.truco = [self.next_player, self.truco[1] + 3]
                self.next_player = functions.get_next_player(self.next_player)

            case PlayerMoves.DESCER.name:
                self.next_player = self.tah_trucando
                self.tah_trucando = ''

            case _:
                if self.next_player == PlayerCode.MCTSPLAYER.name:
                    if action not in self.hand_mcts:
                        print('Eu não deveria ser um print')
                    self.card_mcts.append(action)
                    self.hand_mcts.remove(action)
                else:
                    if action not in self.hand_player:
                        print('Tem maneiras melhores de ver se tem um bug')
                    self.card_player.append(action)
                    self.hand_player.remove(action)
                self.update_points(action, self.next_player, isSimulation)

    def update_points(self, action, current_player, isSimulation = True):
        match(action):
            case PlayerMoves.CORRER.name:
                if current_player == PlayerCode.MCTSPLAYER.name:
                    self.points_player+= max(self.truco[1], 1)
                    self.anunciar_pontuacao(isSimulation, PlayerCode.RANDOMPLAYER.name, max(self.truco[1], 1))
                else:
                    self.points_mcts+= max(self.truco[1], 1)
                    self.anunciar_pontuacao(isSimulation, PlayerCode.MCTSPLAYER.name, max(self.truco[1], 1))
                self.set_new_hands()
            case _:
                if len(self.card_mcts) != len(self.card_player):
                    self.next_player = functions.get_next_player(self.next_player)
                    return
                power_mcts = self.card_value_converter(self.card_mcts[-1])
                power_player = self.card_value_converter(self.card_player[-1])
                if power_player > power_mcts:
                    self.turns_points.append(PlayerCode.RANDOMPLAYER.value)
                    self.next_player = PlayerCode.RANDOMPLAYER.name
                elif power_player < power_mcts:
                    self.turns_points.append(PlayerCode.MCTSPLAYER.value)
                    self.next_player = PlayerCode.MCTSPLAYER.name
                else:
                    self.turns_points.append(PlayerCode.NOBODY.value)

                if len(self.turns_points) == 1:
                    return
                match(self.turns_points[0] + self.turns_points[1]):
                    case 0:
                        if len(self.turns_points) == 2:
                            # print(f'Jogador {self.next_player} torna')
                            return
                        if self.turns_points[2] == 1:
                            self.points_player+= max(self.truco[1], 1)
                            self.anunciar_pontuacao(isSimulation, PlayerCode.RANDOMPLAYER.name, max(self.truco[1], 1))
                        elif self.turns_points[2] == 2:
                            self.points_mcts+= max(self.truco[1], 1)
                            self.anunciar_pontuacao(isSimulation, PlayerCode.MCTSPLAYER.name, max(self.truco[1], 1))
                        self.set_new_hands()
                    case 1:
                        self.points_player+= max(self.truco[1], 1)
                        self.anunciar_pontuacao(isSimulation, PlayerCode.RANDOMPLAYER.name, max(self.truco[1], 1))
                        self.set_new_hands()
                    case 2:
                        if self.turns_points[0] == 1:
                            self.points_player+= max(self.truco[1], 1)
                            self.anunciar_pontuacao(isSimulation, PlayerCode.RANDOMPLAYER.name, max(self.truco[1], 1))
                        else:
                            self.points_mcts+= max(self.truco[1], 1)
                            self.anunciar_pontuacao(isSimulation, PlayerCode.MCTSPLAYER.name, max(self.truco[1], 1))
                        self.set_new_hands()
                    case 3:
                        if len(self.turns_points) == 2:
                            # print(f'Jogador {self.next_player} torna')
                            return
                        match(self.turns_points[2]):
                            case 0:
                                if self.turns_points[0] == 1:
                                    self.points_player+= max(self.truco[1], 1)
                                    self.anunciar_pontuacao(isSimulation, PlayerCode.RANDOMPLAYER.name, max(self.truco[1], 1))
                                else:
                                    self.points_mcts+= max(self.truco[1], 1)
                                    self.anunciar_pontuacao(isSimulation, PlayerCode.MCTSPLAYER.name, max(self.truco[1], 1))
                            case 1:
                                self.points_player+= max(self.truco[1], 1)
                                self.anunciar_pontuacao(isSimulation, PlayerCode.RANDOMPLAYER.name, max(self.truco[1], 1))
                            case 0:
                                self.points_mcts+= max(self.truco[1], 1)
                                self.anunciar_pontuacao(isSimulation, PlayerCode.MCTSPLAYER.name, max(self.truco[1], 1))
                        self.set_new_hands()
                    case 4:
                        self.points_mcts+= max(self.truco[1], 1)
                        self.anunciar_pontuacao(isSimulation, PlayerCode.MCTSPLAYER.name, max(self.truco[1], 1))
                        self.set_new_hands()
                    case _:
                        print('E agora?')

    def available_actions(self):
        if self.tah_trucando:
            if self.truco[1] < 12:
                return [PlayerMoves.CORRER.name, PlayerMoves.AUMENTAR.name, PlayerMoves.DESCER.name]
            else:
                return [PlayerMoves.CORRER.name, PlayerMoves.DESCER.name]

        if self.next_player == PlayerCode.RANDOMPLAYER.name: 
            actions = deepcopy(self.hand_player)
        else:
            actions = deepcopy(self.hand_mcts)
        if self.truco[0] != self.next_player and self.truco[1] < 12 and self.points_mcts != 11 and self.points_player != 11:
            actions.append(PlayerMoves.TRUCO.name)
        random.shuffle(actions)
        return actions