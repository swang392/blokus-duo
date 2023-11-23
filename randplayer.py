from random import choice

from blokus.blokus_game import BlokusGame

class RandomPlayer:
    def __init__(self, game: BlokusGame):
        self.game = game
    
    def choose_move(self, game):
        valid_moves = game.get_valid_moves(game.current_player)
        if valid_moves is None:
            return -1
        moves = []
        for idx, move in enumerate(valid_moves):
            if move == 1:
                moves.append(idx)
        print("random moves", len(moves))
        if len(moves) == 0:
            return -1
        move = choice(moves)
        return move
    
    def move(self, move: int):
        self.game.play_action(move)