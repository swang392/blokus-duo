"""Base Game Class."""


class Game(object):
    """Represents the game board and its logic for a 2 player board game."""

    def __init__(self):
        """Initializes Game with the initial board state."""
        pass

    def clone(self):
        """Creates a deep clone of the game object.

        Returns:
            the cloned game object.
        """
        pass

    def play_action(self, action):
        """Plays an action on the game board.

        Args:
            action: A tuple in the form of (row, column).
        """
        pass

    def get_valid_moves(self, current_player):
        """Returns a list of moves along with their validity.

        Returns:
            A list containing moves in the form of (validity, row, column, ?).
        """
        pass

    def check_game_over(self, current_player):
        """Checks if the game is over and return a possible winner.

        There are 3 possible scenarios.
            a) The game is over and we have a winner.
            b) The game is over but it is a draw.
            c) The game is not over.

        Args:
            current_player: An integer representing the current player.

        Returns:
            A bool representing the game over state.
            An integer action value. (win: 1, loss: -1, draw: 0
        """
        pass

    def print_board(self):
        """Prints the board state."""
        pass
