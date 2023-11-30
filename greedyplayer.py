from random import choice
from copy import deepcopy
from blokus.blokus_game import BlokusGame

class GreedyPlayer:
    def __init__(self, game: BlokusGame):
        self.game = game
    
    def move(self, move: int):
        self.game.play_action(move)

    def get_moves(self, game) -> dict:
        """get all possible moves, returns a dict that is {move: payoff}"""
        valid_moves = game.get_valid_moves(game.current_player)
        if valid_moves is None:
            return -1
        moves = {}
        for idx, move in enumerate(valid_moves):
            if move == 1:
                moves[idx] = self.payoff(game, idx)
                # moves.append(idx)
        # print("random moves", len(moves))
        # print("moves", moves)
        return moves

    def choose_move(self, game: BlokusGame):
        """chooses the move with the highest payoff"""
        moves = self.get_moves(game)
        # print("moves", moves)
        if len(moves) == 0:
            return -1
        max_value = max(moves.values())
        max_keys = [k for k, v in moves.items() if v == max_value]
        res = choice(max_keys)
        # res = max(moves, key=moves.get)
        return res

    def payoff(self, game, move):
        return -1
    
class GreedyCorner(GreedyPlayer):
    """a grredy agent that aims to maximize the number of corners"""
    def __init__(self, game: BlokusGame):
        super().__init__(game)
    
    def payoff(self, game, move):
        """returns the payoff of the move"""
        # print("checking move", move)
        state = deepcopy(game)
        current_player = state.current_player
        current_corners = state.corners[current_player]
        var1 = len(current_corners)
        # print("current corners", current_corners, var1)
        state.play_action(move)
        new_corners = state.corners[current_player]
        var2 = len(new_corners)
        # print("new corners", new_corners, var2)
        # print("BLAH", var2 - var1)
        return var2 - var1


