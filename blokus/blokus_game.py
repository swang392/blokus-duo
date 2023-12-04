from copy import deepcopy
import numpy as np
import copy
from blokus.piece import All_Pieces

from game import Game

invalid_moves = [line.strip() for line in open("invalid_moves.txt", 'r')]
invalid_moves = [int(x) for x in invalid_moves]

class BlokusGame(Game):
    """Class for Blokus Duo"""

    def __init__(self, n = 14):
        self.action_size = 17836
        self.invalid_moves = invalid_moves
        self.size = n 
        self.rounds = 0
        self.current_player = 1
        self.state = np.zeros((n,n), dtype = np.int8)
        self.pieces = {1: All_Pieces,
                      -1: All_Pieces
                        }
        self.score = {1: 0,
                      -1: 0}

        self.corners = { 1: set([(4, 4)]), 
                        -1: set([(self.size -5, self.size-5)])}
        
    def print_board(self):
        """prints current board"""
        print(self.state)

    def play_action(self, action):
        """given an action (numeric id), plays the action on the board"""
        action = self.translate_action(action)
        for (col, row) in action.points:
            self.state[col, row] = self.current_player
            self.score[self.current_player] += 1

        self.rounds += 1
        self.corners[self.current_player].update(self.update_corners(action))
        self.pieces[self.current_player] = self.remove_piece(action)
        self.corners[-self.current_player] = set([(i, j) for (i, j) in self.corners[-self.current_player] if self.state[i][j] == 0])

        self.current_player *= -1

    def heuristic(self, current_player):
        """returns the heuristic for the current player"""
        curr_corner = len(self.corners[current_player])
        opp_corner = len(self.corners[current_player * -1])
        corner_difference = curr_corner - opp_corner
        size = self.score[current_player] - self.score[current_player * -1]

        return corner_difference + 2 * size

    def get_valid_moves(self, current_player):
        """returns a list of valid moves for the current player"""
        all_moves = np.zeros(self.action_size, dtype = np.int8)
        list_of_legals = self.get_legal_moves(current_player)
        for i in list_of_legals:
            if i not in self.invalid_moves:
                all_moves[i] = 1


        return all_moves

    def check_game_over(self, current_player):
        """returns a boolean for whether the game is over and the winner of the game"""
        moves = []
        for player in [1, -1]:
            moves.extend(self.get_valid_moves(player))
            if sum(moves) > 0:
                return False, 0

        if sum(moves) > 0:
            return False, 0
        elif self.score[current_player] >= self.score[-current_player]:
            return True, 1
        else:
            return True, -1

    def remove_piece(self, piece):
        """
        removes piece from the current player's pieces
        """
        new_pieces = [s for s in self.pieces[self.current_player] if s.ID != piece.ID]
        return new_pieces   

    def update_corners(self, action):
        """
        Updates the available corners of a player.
        """
        new_corners = set()
        for c in action.corners:
            if (self.in_bounds(c) and (not self.overlap([c]))):
                new_corners.add(c)
        return new_corners

    def in_bounds(self, point):
        """
        Takes in a tuple and checks if it is in the bounds of the board.
        """
        return (0 <= point[0] <= (self.size - 1)) & (0 <= point[1] <= (self.size - 1))

    def overlap(self, move):
        """
        Returns a boolean for whether a move is overlapping any pieces that have already been placed on the board.
        """
        if False in [(self.state[i][j] == 0) for (i, j) in move]:
            return True
        else:
            return False

    def corner(self, player_label, move):
        """
        returns a boolean of if a move is cornering any pieces of the player proposing the move
        """
        validates = []
        for (i, j) in move:
            if self.in_bounds((i + 1, j + 1,)):
                validates.append((self.state[i + 1][j + 1] == player_label))
            if self.in_bounds((i - 1, j - 1)):
                validates.append((self.state[i - 1][j - 1] == player_label))
            if self.in_bounds((i + 1, j - 1,)):
                validates.append((self.state[i + 1][j - 1] == player_label))
            if self.in_bounds((i - 1, j + 1)):
                validates.append((self.state[i - 1][j + 1] == player_label))
        return True in validates
    
    def adj(self, player_label, move):
        """
        returns a boolean of if a move is adjacent to any pieces of the player proposing the move
        """
        validates = []
        for (i, j) in move:
            if self.in_bounds((i + 1, j)):
                validates.append((self.state[i + 1][j] == player_label))
            if self.in_bounds((i - 1, j)):
                validates.append((self.state[i - 1][j] == player_label))
            if self.in_bounds((i, j - 1)):
                validates.append((self.state[i][j - 1] == player_label))
            if self.in_bounds((i, j + 1)):
                validates.append((self.state[i][j + 1] == player_label))
        return True in validates

    def valid_move(self, action, player_label):
        if self.rounds < 2: # first actions haven't been done yet
            if ((False in [self.in_bounds(pt) for pt in action]) 
                or self.overlap(action) 
                or not (True in [(pt in self.corners[player_label]) for pt in action])):
                
                return False
            
            else:
                return True

        elif ((False in [self.in_bounds(pt) for pt in action])
              or self.overlap(action)
              or self.adj(player_label, action)
              or not self.corner(player_label, action)):
            return False

        else:
            return True

    def get_legal_moves(self, player_label):
        # print('WERE IN GET LEGAL MOVES')
        placements = []
        visited = []
        # Loop through every available corner.
        for cr in self.corners[player_label]:
            # Look through every piece offered. (This will be restricted according to certain algorithms.)
            for sh in self.pieces[player_label]:
                # Create a new shape so that the one in the player's list of shapes is not overwritten.
                try_out = copy.deepcopy(sh)
                # Loop over every potential refpt the piece could have.
                # for num in range(try_out.size):
                try_out.create(0, cr)
                # And every possible flip.
                for fl in try_out.flips:
                    temp_fl = copy.deepcopy(try_out)
                    temp_fl.flip(fl)
                    # And every possible orientation.
                    for rot in try_out.rots:
                        temp_rot = copy.deepcopy(temp_fl)
                        temp_rot.rotate(rot)
                        candidate = copy.deepcopy(temp_rot)
                        if fl == 'h':
                            f = 1
                        else:
                            f = 0
                        


                        if candidate.ID not in ['I5', 'I4','I3','I2']:
                            encoding = (cr[0] * 14 + cr[1]) * 91 + temp_rot.shift + (rot//90)*2 + f
                        else:
                            encoding = (cr[0] * 14 + cr[1]) * 91 + temp_rot.shift + (rot//90)*1 + f

                        if self.valid_move(candidate.points, player_label):
                            if not (set(candidate.points) in visited):
                                placements.append(encoding) 
                                visited.append(set(candidate.points))
        return placements


    def translate_action(self, input_number):
        position = input_number // 91
        input_number = input_number % 91
        if input_number < 8:
            piece = All_Pieces[0]
            rotation = input_number // 2
            fl = input_number % 2
        elif input_number < 16:
            piece = All_Pieces[1]
            rotation = (input_number % 8 )// 2
            fl = input_number % 2
        elif input_number < 24:
            piece = All_Pieces[2]
            rotation = (input_number % 8 )// 2
            fl = input_number % 2
        elif input_number < 32:
            piece = All_Pieces[3]
            rotation = (input_number % 8 )// 2
            fl = input_number % 2    
        elif input_number < 40:
            piece = All_Pieces[4]
            rotation = (input_number % 8 )// 2
            fl = input_number % 2
        elif input_number < 48:
            piece = All_Pieces[5]
            rotation = (input_number % 8 )// 2
            fl = input_number % 2
        elif input_number < 52:
            piece = All_Pieces[6]
            rotation = (input_number % 4 )// 2
            fl = input_number % 2
        elif input_number < 56:
            piece = All_Pieces[7]
            rotation = (input_number % 4 )// 2
            fl = input_number % 2
        elif input_number < 60:
            piece = All_Pieces[8]
            rotation = (input_number % 4 )// 2
            fl = input_number % 2
        elif input_number < 64:
            piece = All_Pieces[9]
            rotation = (input_number % 4 )// 2
            fl = input_number % 2
        elif input_number < 68:
            piece = All_Pieces[10]
            rotation = (input_number % 4 )// 2
            fl = input_number % 2
        elif input_number < 72:
            piece = All_Pieces[11]
            rotation = (input_number % 4 )// 2
            fl = input_number % 2
        elif input_number < 76:
            piece = All_Pieces[12]
            rotation = (input_number % 4 )// 2
            fl = input_number % 2
        elif input_number < 80:
            piece = All_Pieces[13]
            rotation = (input_number % 4 )// 2
            fl = input_number % 2
        elif input_number < 82:
            piece = All_Pieces[14]
            rotation = input_number % 2 
            fl = 0
        elif input_number < 84:
            piece = All_Pieces[15]
            rotation = input_number % 2 
            fl = 0
        elif input_number < 86:
            piece = All_Pieces[16]
            rotation = input_number % 2 
            fl = 0
        elif input_number < 88:
            piece = All_Pieces[17]
            rotation = 0 
            fl = 0
        elif input_number < 89:
            piece = All_Pieces[18]
            rotation = 0 
            fl = 0
        elif input_number < 90:
            piece = All_Pieces[19]
            rotation = 0 
            fl = 0
        elif input_number < 91:
            piece = All_Pieces[20]
            rotation = 0 
            fl = 0

        position_x = int(position // 14)
        position_y = position % 14
        if fl == 0: 
            fl = "None" 
        else: fl = "h"
        piece.create(0, (position_x, position_y))
        piece.flip(fl)
        piece.rotate(90 * rotation)
        
        return piece