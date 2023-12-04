"""Class to train the Neural Network."""
# import numpy as np

from mcts import MonteCarloTreeSearch
from blokus.blokus_game import BlokusGame
from copy import deepcopy
from randplayer import RandomPlayer
from greedyplayer import GreedyPlayer, GreedyCorner, GreedyCornerDiff, GreedyCombination

class Train(object):
    """Class with functions to train the Neural Network using MCTS.

    Attributes:
        game: An object containing the game state.
        net: An object containing the neural network.
    """

    def __init__(self, game):
        """Initializes Train with the board state and neural network."""
        self.game = game

    def start(self, num_iterations: int):
        """playing loop"""
        p1_win_score = 0
        p2_win_score = 0
        p1_win_margin = 0
        p2_win_margin = 0
        p1_score = 0
        p2_score = 0
        
        # f = open("results/mcts_vs_mcts_12.txt", "w")
        # f.write("MCTS vs. MCTS\n")
        # print("MCTS vs. MCTS")
        f = open("results/random_mcts.txt", "w")
        f.write("Random vs. MCTS\n")
        print("Random vs. MCTS")
        # f = open("results/mcts_random.txt", "w")
        # f.write("MCTS vs. Random\n")
        # print("MCTS vs. Random")
        for i in range(num_iterations):
            game = deepcopy(self.game)
            # score = self.mcts_vs_mcts(game, 12)
            # score = self.mcts_vs_random(game, 12)
            score = self.random_vs_mcts(game, 12)
            # score = self.random_vs_random(game)
            print("Game", i+1, "score:", score)
            if score[1] > score[-1]:
                p1_win_score += 1
                p1_win_margin += score[1] - score[-1]
            elif score[1] < score[-1]:
                p2_win_score += 1
                p2_win_margin += score[-1] - score[1]
            else:
                p1_win_score += 0.5
                p2_win_score += 0.5
            p1_score += score[1]
            p2_score += score[-1]
            f.write("Game " + str(i+1) + " score: " + str(score) + "\n")

        print("final win score", p1_win_score, p2_win_score)
        f.write("Final win score: " + str(p1_win_score) + " " + str(p2_win_score) + "\n")
        f.write("Average win margin: \n")
        if p1_win_score != 0:
            f.write("Player 1: " + str(p1_win_margin/p1_win_score) + "\n")
            print("Player 1: " + str(p1_win_margin/p1_win_score))
        if p2_win_score != 0:
            f.write("Player 2: " + str(p2_win_margin/p2_win_score) + "\n")
            print("Player 2: " + str(p2_win_margin/p2_win_score))
        print("average score", p1_score/num_iterations, p2_score/num_iterations)
        f.write("Average score: " + str(p1_score/num_iterations) + " " + str(p2_score/num_iterations) + "\n")
        f.close()
    
    def start_random_vs_random(self, num_iterations: int):
        p1_win_score = 0
        p2_win_score = 0
        p1_win_margin = 0
        p2_win_margin = 0
        p1_score = 0
        p2_score = 0

        f = open("results/random_vs_random.txt", "w")
        f.write("Random vs. Random\n")
        print("Random vs. Random")

        for i in range(num_iterations):
            game = deepcopy(self.game)
            score = self.random_vs_random(game)
            print("Game", i+1, "score:", score)
            if score[1] > score[-1]:
                p1_win_score += 1
                p1_win_margin += score[1] - score[-1]
            elif score[1] < score[-1]:
                p2_win_score += 1
                p2_win_margin += score[-1] - score[1]
            else:
                p1_win_score += 0.5
                p2_win_score += 0.5
            p1_score += score[1]
            p2_score += score[-1]
            f.write("Game " + str(i+1) + " score: " + str(score) + "\n")

        print("final win score", p1_win_score, p2_win_score)
        f.write("Final win score: " + str(p1_win_score) + " " + str(p2_win_score) + "\n")
        f.write("Average win margin: \n")
        if p1_win_score != 0:
            f.write("Player 1: " + str(p1_win_margin/p1_win_score) + "\n")
            print("Player 1: " + str(p1_win_margin/p1_win_score))
        if p2_win_score != 0:
            f.write("Player 2: " + str(p2_win_margin/p2_win_score) + "\n")
            print("Player 2: " + str(p2_win_margin/p2_win_score))
        print("average score", p1_score/num_iterations, p2_score/num_iterations)
        f.write("Average score: " + str(p1_score/num_iterations) + " " + str(p2_score/num_iterations) + "\n")
        f.close()

    def greedy_vs_random(self, game: BlokusGame) -> dict:
        """
        Loop for a self play game, where player 1 is Random and player 2 is greedy, corner maximization.
        """
        randplayer = RandomPlayer(game)
        greedyplayer = GreedyCombination(game)
        game_over = False
        move = None

        while not game_over:
            if game.check_game_over(game.current_player)[0]: # if game ended
                game_over = True
                continue
            elif game.current_player == 1:
                move = randplayer.choose_move(game)
                if move == -1:
                    game.current_player *= -1
                    continue
                else:
                    randplayer.move(move)
            elif game.current_player == -1:
                move = greedyplayer.choose_move(game)
                if move == -1:
                    game.current_player *= -1
                    continue
                else:
                    greedyplayer.move(move)
            # move = randplayer.choose_move(game)
            # if move == -1: # pass
            #     game.current_player *= -1
            #     continue
            # else:
            #     randplayer.move(move)
        print('FINAL SCORES ARE ', game.score)
        return game.score

    def mcts_vs_random(self, game: BlokusGame, time: int) -> dict:
        """
        Loop for a self play game, where player 1 is MCTS and player 2 is random.
        """
        mcts = MonteCarloTreeSearch(game)
        randplayer = RandomPlayer(game)
        game_over = False
        # count = 0
        move = None
        # node = Node()
        while not game_over:
            # game.print_board()
            if game.current_player == 1:
                if game.check_game_over(game.current_player)[0]: # if game ended
                    game_over = True
                    continue
                else:
                    mcts.search(time_budget=time)
                    move = mcts.best_move()
                    if move == -1:
                        #  elif move == -1: # game over
                        randmove = randplayer.choose_move(game)
                        if randmove == -1:
                            game_over = True
                        else:
                            game.play_action(randmove)
                            game.current_player *= -1
                            
                        game.current_player *= -1
                        continue
                    mcts.move(move)
            elif game.current_player == -1:
                if game.check_game_over(game.current_player)[0]: # if game ended
                    game_over = True
                    continue
                move = randplayer.choose_move(game)
                if move == -1: # pass
                    game.current_player *= -1
                    continue
                else:
                    randplayer.move(move)
        print('FINAL SCORES ARE ', game.score)
        game.print_board()
        return game.score
        # game.print_board()

    def random_vs_mcts(self, game: BlokusGame, time: int) -> dict:
        """
        Loop for a self play game, where P1 is a random player and P2 is MCTS.
        """
        mcts = MonteCarloTreeSearch(game)
        randplayer = RandomPlayer(game)
        game_over = False
        # count = 0
        move = None
        # node = Node()
        while not game_over:
            # game.print_board()
            if game.current_player == -1:
                if game.check_game_over(game.current_player)[0]: # if game ended
                    game_over = True
                    continue
                else:
                    mcts.search(time_budget=time)
                    move = mcts.best_move()
                    if move == -1:
                        randmove = randplayer.choose_move(game)
                        if randmove == -1:
                            game_over = True
                        else:
                            game.play_action(randmove)
                            game.current_player *= -1
                            
                        game.current_player *= -1
                        continue
                    mcts.move(move)
            elif game.current_player == 1:
                if game.check_game_over(game.current_player)[0]: # if game ended
                    game_over = True
                    continue
                move = randplayer.choose_move(game)
                if move == -1: # pass
                    game.current_player *= -1
                    continue
                else:
                    randplayer.move(move)
        # print(mcts.expanded)
        print("TREE SIZE", mcts.tree_size())
        print('FINAL SCORES ARE ', game.score)
        game.print_board()
        return game.score
        # game.print_board()

    def random_vs_random(self, game: BlokusGame) -> dict:
        """
        Loop for a self play game, where both players are random.
        """
        game_over = None
        move = None
        randplayer = RandomPlayer(game)
        while not game_over:
            if game.check_game_over(game.current_player)[0]: # if game ended
                game_over = True
                continue
            move = randplayer.choose_move(game)
            if move == -1: # pass
                game.current_player *= -1
                continue
            else:
                randplayer.move(move)
        print('FINAL SCORES ARE ', game.score)
        return game.score

    def greedy_vs_greedy(self, game:BlokusGame) -> dict:
        """
        Loop for a self play game, where both players are greedy.
        """
        game_over = None
        move = None
        greedyplayer = GreedyCombination(game)
        while not game_over:
            if game.check_game_over(game.current_player)[0]:
                game_over = True
                continue
            move = greedyplayer.choose_move(game)
            if move == -1:
                game.current_player *= -1
                continue
            else:
                greedyplayer.move(move)
            # game.print_board()
        print('FINAL SCORES ARE ', game.score)
        return game.score

    def mcts_vs_mcts(self, game: BlokusGame, time: int) -> dict:
        """
        Loop for a self play game, where both players are MCTS.
        """
        game_over = None
        move = None
        mcts = MonteCarloTreeSearch(game)
        randplayer = RandomPlayer(game)
        while not game_over:
            if game.check_game_over(game.current_player)[0]: # if game ended
                game_over = True
                continue
            # if move == -1:
            #     game_over = True
            else:
                mcts.search(time_budget=time)
                move = mcts.best_move()
                if move == -1:
                    randmove = randplayer.choose_move(game)
                    if randmove == -1:
                        game_over = True
                    else:
                        game.play_action(randmove)
                        game.current_player *= -1
                        
                    game.current_player *= -1
                    continue

                mcts.move(move)
        print('FINAL SCORES ARE ', game.score)
        return game.score