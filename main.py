"""File which starts the program"""
import argparse
import os

from blokus.blokus_game import BlokusGame
# from neural_net import NeuralNetworkWrapper 
from testing import Tester
# from human_player import Human_player

# Code to read command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--num_iterations",
                    help="Number of iterations.",
                    dest="num_iterations",
                    type=int,
                    default=100)

if __name__ == '__main__':
    """Initializes game state, ne ural network and the training loop"""
    arguments = parser.parse_args()

    # Replace CFG values with the values from the command line.
    num_iterations = arguments.num_iterations

    game = BlokusGame()

    tester = Tester(game)
    tester.start(num_iterations)