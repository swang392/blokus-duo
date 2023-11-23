"""Class to train the Neural Network."""
# import numpy as np

from config import CFG
from mcts import MonteCarloTreeSearch
from blokus.blokus_game import BlokusGame
from copy import deepcopy
from randplayer import RandomPlayer

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
        p1_score = 0
        p2_score = 0
        f = open("results/mcts_vs_random.txt", "w")
        f.write("MCTS vs. Random\n")
        print("MCTS vs. Random")
        # for i in range(CFG.num_iterations):
        for i in range(5):
            game = deepcopy(self.game)
            score = self.mcts_vs_random(game)
            print("Game", i+1, "score:", score)
            if score[1] > score[-1]:
                p1_score += 1
            elif score[1] < score[-1]:
                p2_score += 1
            else:
                p1_score += 0.5
                p2_score += 0.5
            f.write("Game " + str(i+1) + " score: " + str(score) + "\n")

        print("final score", p1_score, p2_score)
        f.write("Final score: " + str(p1_score) + " " + str(p2_score) + "\n")
        f.close()

    def mcts_vs_random(self, game: BlokusGame) -> dict:
        """Loop for each self-play game.

        Runs MCTS for each game state and plays a move based on the MCTS output.
        Stops when the game is over and prints out a winner.

        Args:
            game: An object containing the game state.
            training_data: A list to store self play states, pis and vs.
        """
        mcts = MonteCarloTreeSearch(game)
        randplayer = RandomPlayer(game)
        game_over = False
        # count = 0
        move = None
        # node = Node()
        while not game_over:
            if game.current_player == 1:
                if game.check_game_over(game.current_player)[0]: # if game ended
                    game_over = True
                    continue
                elif move == -1: # game over
                    # print("GAME OVER")
                    # game_over = True
                    print('player 1 passed')
                    # game.print_board(
                    print('score', game.score)
                    randmove = randplayer.choose_move(game)
                    if randmove == -1:
                        game_over = True
                    else:
                        print("JKKKKK move", randmove)
                        game.play_action(randmove)
                        game.current_player *= -1
                        
                    game.current_player *= -1
                    continue
                else:
                    mcts.search(time_budget=3)
                    move = mcts.best_move()
                    # print('MOVE:', move)
                    # game.play_action(move)
                    mcts.move(move)
            elif game.current_player == -1:
                if game.check_game_over(game.current_player)[0]: # if game ended
                    game_over = True
                    continue
                # if move == -1: # game over
                #     # print("GAME OVER")
                #     game_over = True
                # else:
                #     mcts.search(time_budget=3)
                #     move = mcts.best_move()
                #     # print('MOVE:', move)
                #     # game.play_action(move)
                #     mcts.move(move)
                move = randplayer.choose_move(game)
                # print("random move,", move)
                if move == -1: # pass
                    # print("GAME OVER")
                    # game_over = True
                    # game_over = True
                    print('player 2 passed')
                    game.print_board()
                    print('score', game.score)
                    game.current_player *= -1
                    continue
                # elif move == -2: #pass, game not over
                #     game_over = True
                else:
                    # mcts.play_action(move)
                    randplayer.move(move)
            game.print_board()
            print("current score", game.score)
            
        print('FINAL SCORES ARE ', game.score)
        return game.score
        game.print_board()
