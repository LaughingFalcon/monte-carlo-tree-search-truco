from nodes import MCTSNode
from copy import deepcopy
import time

class MctsPlayer():
    def __init__(self, time):
        self.simulation_time = time

    def mcts_search(self, root_state):
        root = MCTSNode(deepcopy(root_state), player=None)

        # State precisa dar cartas aleatórias para o oponente para a simulação ser justa
        if len(root.state.card_mcts) != 0 and root.state.card_mcts[0] in root.state.known_deck:
            root.state.known_deck.remove(root.state.card_mcts[0])
        for i in range(len(root.state.hand_mcts)):
            root.state.hand_mcts[i] = root.state.known_deck[i]

        iterations = 0
        ts = time.time()
        # for i in range(iterations):
        while((time.time() - ts) < self.simulation_time):
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

    def choose_move(self, mesa_de_jogo):
        move = self.mcts_search(mesa_de_jogo)
        return move