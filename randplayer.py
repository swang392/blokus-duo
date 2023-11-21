from copy import deepcopy
# from queue import Queue
from random import choice
from time import time as clock

from blokus.blokus_game import BlokusGame

class RandomPlayer:
    def __init__(self, game: BlokusGame):
        self.game = game
    
    def choose_move(self, game):
        # state = deepcopy(game)
        # state.print_board()
        # if game.check_game_over(self.game.current_player)[0]: # if game ended
        #     return -1
        # valid_moves = state.get_valid_moves(state.current_player)
        valid_moves = game.get_valid_moves(game.current_player)
        if valid_moves is None:
            return -1
        moves = []
        for idx, move in enumerate(valid_moves):
            if move == 1:
                moves.append(idx)
                # action = idx
                # moves.
                # self.add_child_node(parent=self, action=action)
        # return True
        # print(moves)
        # if valid_moves is None:
        #     return -2
        print("random moves", len(moves))
        if len(moves) == 0:
            return -1
        move = choice(moves)
        return move
    
    def move(self, move: int):
        self.game.play_action(move)