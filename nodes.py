from enumerations import PlayerCode
from truco_gen import Mesa
from copy import deepcopy
import functions
import random
import math

class MCTSNode:
    def __init__(self, state: Mesa, parent=None, action=None, player=None):
        self.state = state
        self.parent = parent
        self.action = action        
        self.player = player         
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self.untried_actions = state.available_actions()

    def is_terminal(self):
        return functions.check_winner_state(self.state) is not None or not self.state.available_actions()
    
    def is_fully_expanded(self):
        return len(self.untried_actions) == 0
    
    def expand(self):
        action = self.untried_actions.pop()
        new_state = deepcopy(self.state)

        player_to_move = self.state.next_player
        
        new_state.play_cards(action)
        
        new_state.last_move = action
        child = MCTSNode(new_state, parent=self, action=action, player=player_to_move)
        self.children.append(child)
        return child
    
    def best_child(self, c=1.4):
        for child in self.children:
            if child.visits == 0:
                return child
        
        def ucb(child):
            exploit = child.wins / child.visits
            explore = c * math.sqrt(math.log(self.visits) / child.visits)
            return exploit + explore

        return max(self.children, key=ucb)
    
    def rollout(self):
        state = deepcopy(self.state)

        while True:
            winner = functions.check_winner_state(state)
            if winner is not None:
                return winner
            actions = state.available_actions()
            if not actions:
                return None
            rand_move = random.choice(actions)
            state.play_cards(rand_move)
    
    def backpropagate(self, winner):
        self.visits += 1

        if self.player is not None:
            if winner is None:
                self.wins += 0.5
            elif winner == self.player:
                self.wins += 1.0

        if self.parent:
            self.parent.backpropagate(winner)