from math import sqrt, log
from copy import deepcopy
from queue import Queue
from random import choice
from time import time as clock

from blokus.blokus_game import BlokusGame

class Node:
    """Represents a board state and stores statistics for actions at that state.

    Attributes:
        Nsa: An integer for visit count.
        Q_RAVE (int): times this move has been critical in a rollout
        N_RAVE (int): times this move has appeared in a rollout
        Qsa: A float for the mean action value.
        action: A tuple(row, column) of the prior move of reaching this node.
        children: A list which stores child nodes.
        parent: A TreeNode representing the parent node.
        outcome (int): If node is a leaf, then outcome indicates
                       the winner, else None
    """
    def __init__(self, parent=None, action=None):
        """
        Initialize a new node with optional move and parent and initially empty
        children list and rollout statistics and unspecified outcome.

        """
        self.action = action
        self.parent = parent
        self.N = 0  # times this position was visited
        self.Q = 0  # average reward (wins-losses) from this position
        self.Q_RAVE = 0  # times this move has been critical in a rollout
        self.N_RAVE = 0  # times this move has appeared in a rollout
        self.children = {}
        self.outcome = 0

    def is_not_leaf(self):
        """Checks if a TreeNode is a leaf.

        Returns:
            A boolean value indicating if a TreeNode is a leaf.
        """
        if len(self.children) > 0:
            return True
        return False

    def expand_node(self, game):
        """Expands the current node by adding valid moves as children.

        Args:
            game: An object containing the game state.
        """
        # self.child_psas = deepcopy(psa_vector)
        # print("expand node")
        valid_moves = game.get_valid_moves(game.current_player)
        if valid_moves is None:
            return False
        for idx, move in enumerate(valid_moves):
            if move == 1:
                action = idx
                self.add_child_node(parent=self, action=action)
        return True
                
    def add_child_node(self, parent, action, psa=0.0):
        """Creates and adds a child Node to the current node.

        Args:
            parent: A Node which is the parent of this node.
            action: A tuple(row, column) of the prior move to reach this node.
        Returns:
            The newly created child Node.
        """

        child_node = Node(parent=parent, action=action)
        self.children[child_node.action] = child_node
        return child_node

    @property
    def value(self, explore: float = 0.5):
        """
        Calculate the UCT value of this node relative to its parent, the parameter
        "explore" specifies how much the value should favor nodes that have
        yet to be thoroughly explored versus nodes that seem to have a high win
        rate.
        Currently explore is set to 0.5.

        """
        # if the node is not visited, set the value as infinity. Nodes with no visits are on priority
        # (lambda: print("a"), lambda: print("b"))[test==true]()
        if self.N == 0:
            return 0 if explore == 0 else float('inf')
        else:
            return self.Q / self.N + explore * sqrt(2 * log(self.parent.N) / self.N)  # exploitation + exploration

class MonteCarloTreeSearch:
    """
    Basic no frills implementation of an agent that preforms MCTS for hex.
    Attributes:
        game: An object containing the game state.
        root (Node): Root of the tree search
        run_time (int): time per each run
        node_count (int): the whole nodes in tree
        num_rollouts (int): The number of rollouts for each search
        EXPLORATION (int): specifies how much the value should favor
                           nodes that have yet to be thoroughly explored versus nodes
                           that seem to have a high win rate.
    """

    def __init__(self, game: BlokusGame):
        self.game = game
        self.root = Node()
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0

    def search(self, time_budget: int) -> None:
        """
        Search and update the search tree for a
        specified amount of time in seconds.
        """
        start_time = clock()
        num_rollouts = 0

        # do until we exceed our time budget
        while clock() - start_time < time_budget:
            # print("rollouts: ", num_rollouts)
            # print(clock() - start_time)
            node, state = self.select_node()
            turn = state.current_player * -1
            outcome = self.roll_out(state)
            self.backup(node, turn, outcome)
            num_rollouts += 1
        run_time = clock() - start_time
        node_count = self.tree_size()
        self.run_time = run_time
        self.node_count = node_count
        self.num_rollouts = num_rollouts

    def select_node(self) -> tuple:
        """
        Select a node in the tree to preform a single simulation from.

        """
        node = self.root
        state = deepcopy(self.game)
        # print('MCTS BOARD')
        # state.print_board()

        # stop if we find reach a leaf node
        while node.is_not_leaf():
            # descend to the maximum value node, break ties at random
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value).value
            max_nodes = [n for n in node.children.values()
                         if n.value == max_value]
            node = choice(max_nodes)
            state.play_action(node.action)

            # if some child node has not been explored select it before expanding
            # other children
            if node.N == 0:
                return node, state

        # if we reach a leaf node generate its children and return one of them
        # if the node is terminal, just return the terminal node
        # node.expand_node(game=state)
        if node.expand_node(game=state) and len(node.children.values()) > 0:
            # print(len(node.children.values()))
            # print("expand")
            node = choice(list(node.children.values()))
            state.play_action(node.action)
        return node, state
    
    @staticmethod
    def roll_out(state: BlokusGame) -> int:
        """
        Simulate an entirely random game from the passed state and return the winning
        player.

        Args:
            state: game state

        Returns:
            int: winner of the game

        """
        # print("rollout")
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
        return state.check_game_over(state.current_player)[1]
    
    @staticmethod
    def backup(node: Node, turn: int, outcome: int) -> None:
        """
        Update the node statistics on the path from the passed node to root to reflect
        the outcome of a randomly simulated playout.

        Args:
            node:
            turn: winner turn
            outcome: outcome of the rollout

        Returns:
            object:

        """
        # print("backup")
        # Careful: The reward is calculated for player who just played
        # at the node and not the next player to play
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            reward = 0 if reward == 1 else 1

    def tree_size(self) -> int:
        """
        Count nodes in tree by BFS.
        """
        Q = Queue()
        count = 0
        Q.put(self.root)
        while not Q.empty():
            node = Q.get()
            count += 1
            for child in node.children.values():
                Q.put(child)
        return count
    
    def best_move(self) -> int:
        """
        Return the best move according to the current tree.
        Returns:
            best move in terms of the most simulations number unless the game is over
        """
        game_over, player = self.game.check_game_over(self.game.current_player)
        # print("bestmove", game_over, player)
        # print(self.game.current_player)
        # self.game.print_board()
        if game_over or len(self.root.children) == 0:
            return -1

        # choose the move of the most simulated node breaking ties randomly
        # print(len(self.root.children))
        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        bestchild = choice(max_nodes)
        return bestchild.action

    def move(self, move: int) -> None:
        """
        Make the passed move and update the tree appropriately. It is
        designed to let the player choose an action manually (which might
        not be the best action).
        Args:
            move:
        """
        # print("move: ", move)
        if move in self.root.children:
            child = self.root.children[move]
            child.parent = None
            self.root = child
            self.game.play_action(child.action)
            return

        # if for whatever reason the move is not in the children of
        # the root just throw out the tree and start over
        self.game.play_action(move)
        self.root = Node()