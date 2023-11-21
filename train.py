"""Class to train the Neural Network."""
# import numpy as np

from config import CFG
from mcts import MonteCarloTreeSearch
from blokus.blokus_game import BlokusGame
from copy import deepcopy


class Train(object):
    """Class with functions to train the Neural Network using MCTS.

    Attributes:
        game: An object containing the game state.
        net: An object containing the neural network.
    """

    def __init__(self, game):
        """Initializes Train with the board state and neural network."""
        self.game = game

    def start(self):
        """playing loop"""
        for i in range(CFG.num_iterations):
            print("Game", i+1)

            game = deepcopy(self.game)
            self.play_game(game)

    def play_game(self, game: BlokusGame):
        """Loop for each self-play game.

        Runs MCTS for each game state and plays a move based on the MCTS output.
        Stops when the game is over and prints out a winner.

        Args:
            game: An object containing the game state.
            training_data: A list to store self play states, pis and vs.
        """
        mcts = MonteCarloTreeSearch(game)

        game_over = False
        # count = 0
        move = None
        # node = Node()
        while not game_over:
            if move == -1: # game over
                # print("GAME OVER")
                game_over = True
            else:
                mcts.search(time_budget=3)
                move = mcts.best_move()
                # print('MOVE:', move)
                # game.play_action(move)
                mcts.move(move)
                # game.print_board()
                # print("current score", game.score)
            

        print('FINAL SCORES ARE ', game.score)
