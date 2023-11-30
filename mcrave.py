from math import sqrt, log
import numpy as np
from copy import deepcopy
from random import choice, random
from time import time as clock

from mcts import Node, MonteCarloTreeSearch
from blokus.blokus_game import BlokusGame

"""Class for Monte Carlo Tree Search Variation: MC-RAVE."""

class RaveNode(Node):
    """Represents a board state and stores statistics for actions at that state.

    Attributes:
        Nsa: An integer for visit count.
        Wsa: A float for the total action value.
        Qsa: A float for the mean action value.
        Psa: A float for the prior probability of reaching this node.
        action: A tuple(row, column) of the prior move of reaching this node.
        children: A list which stores child nodes.
        child_psas: A vector containing child probabilities.
        parent: A TreeNode representing the parent node.
    """
    def __init__(self, parent=None, action=None):
        super(RaveNode, self).__init__(parent, action)

    @property
    def value(self, explore:float = 0.5, rave_const:float = 300) -> float:
        """
        Calculate the UCT value of this node relative to its parent, the parameter
        "explore" specifies how much the value should favor nodes that have
        yet to be thoroughly explored versus nodes that seem to have a high win
        rate.
        Currently explore is set to zero when choosing the best move to play so
        that the move with the highest win_rate is always chosen. When searching
        explore is set to EXPLORATION specified above.

        """
        if self.N == 0:
            return 0 if explore == 0 else float("inf")
        else:
            alpha = max(0, (rave_const - self.N) / rave_const)
            UCT = self.Q / self.N + explore * sqrt(2 * log(self.parent.N) / self.N)
            AMAF = self.Q_RAVE / self.N_RAVE if self.N_RAVE is not 0 else 0
            return (1 - alpha) * UCT + alpha * AMAF
    
    def add_child_node(self, action, psa=0):
        self.expanded += 1
        child_node = RaveNode(parent=self, action=action)
        self.children[child_node.action] = child_node
        return child_node
    
class MCRAVE(MonteCarloTreeSearch):
    def __init__(self, game: BlokusGame):
        self.game = game
        self.root = RaveNode()
        # self.run_time = 0
        # self.node_count = 0
        # self.num_rollouts = 0

    def set_game(self, game: BlokusGame):
        """
        Set the root_state of the tree to the passed gamestate, this clears all
        the information stored in the tree since none of it applies to the new
        state.
        """
        self.game = deepcopy(game)
        self.root = RaveNode()

    def move(self, move: int) -> None:
        """
        Make the passed move and update the tree appropriately
        """
        if move in self.root.children:
            child = self.root.children[move]
            child.parent = None
            self.root = child
            self.game.play_action(child.action)
            return
        
        # if for whatever reason the move is not in the children of
        # the root just throw out the tree and start over
        self.game.play_action(move)
        self.root = RaveNode()

    def search(self, time_budget: int) -> None:
        """
        search and update the search tree for a specifed
        amount of time in seconds
        """
        start_time = clock()
        num_rollouts = 0

        while clock() - start_time < time_budget:
            node, state = self.select_node()
            turn = state.current_player * -1
            outcome, p1_rave, p2_rave = self.roll_out(state)
            self.backup(node, turn, outcome, p1_rave, p2_rave)
            # num_rollouts += 1

    def select_node(self) -> tuple:
        return super().select_node()
    
    @staticmethod
    def rollout(state: BlokusGame) -> int:
        """
        Simulate a random game except that we play all known critical
        cells first, return the winning player and record critical cells at the end.
        """
        valid_moves = list(state.get_valid_moves(state.current_player))
        moves = []
        for idx, move in enumerate(valid_moves):
            if move == 1:
                moves.append(idx)
        # moves = state.moves()  # Get a list of all possible moves in current state of the game
        # count = 10
        count = 100
        while count > 0 and state.check_game_over(state.current_player)[1] == 0 and moves:
            # print("rollout moves:", len(moves))
            move = choice(moves)
            state.play_action(move)
            moves.remove(move)
            count -= 1

        p1_rave = []
        p2_rave = []


        return state.check_game_over(state.current_player)[1]
    