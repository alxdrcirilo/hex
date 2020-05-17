import copy
from math import log, sqrt, inf
from random import choice

import numpy as np
from tqdm import tqdm


class Node(object):
    def __init__(self, logic, board, move=(None, None), wins=0, visits=0, children=None):
        # Save the #wins:#visited ratio
        self.state = board
        self.move = move
        self.wins = wins
        self.visits = visits
        self.children = children or []
        self.parent = None
        self.untried_moves = logic.get_possible_moves(board)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class MCTS:
    def __init__(self, board_state, logic, starting_player):
        self.root_state = copy.copy(board_state)
        self.state = copy.copy(board_state)
        self.logic = logic
        self.starting_player = starting_player
        self.players = [1, 2]
        self.players.remove(self.starting_player)
        self.other_player = self.players[0]
        self.turn = {True: self.starting_player, False: self.other_player}
        self.turn_state = True

    def start(self, itermax: int):
        root_node = Node(self.logic, self.root_state)
        for _ in tqdm(range(itermax)):
            node = root_node
            state = copy.copy(self.root_state)
            # Debug
            # print(node.untried_moves)

            # Select
            while node.untried_moves == [] and node.children != []:
                # Node is fully expanded and non-terminal
                uct_values = []
                for child in node.children:
                    uct_values.append(self.select(child))
                if all([value == 0 for value in uct_values]):
                    node = choice(node.children)
                else:
                    node = node.children[np.argmax(uct_values)]

            # Expand
            if node.untried_moves != []:
                x, y = choice(node.untried_moves)
                state[x][y] = self.turn[self.turn_state]
                node.untried_moves.remove((x, y))
                self.next_turn()
                node.add_child(Node(self.logic, state, (x, y)))

            # Playout
            while self.logic.get_possible_moves(state) != []:
                x, y = choice(self.logic.get_possible_moves(state))

                player = self.turn[self.turn_state]
                state[x][y] = player

                for player in [1, 2]:
                    winner = self.logic.is_game_over(player, state, True)

                self.next_turn()

                if winner:
                    # Reset MCTS_GAME_OVER
                    self.logic.MCTS_GAME_OVER = False
                    break

            # Backpropagation
            while node != None:
                win_value = 1 if winner is self.starting_player else -1

                node.wins += win_value
                node.visits += 1
                node = node.parent

            root_node.wins += win_value
            root_node.visits += 1

        result = root_node.children[np.argmax([node.visits for node in root_node.children])].move
        print([node.visits for node in root_node.children])
        for n in root_node.children:
            print(n.wins, n.visits)
        return result

    def next_turn(self):
        self.turn_state = not self.turn_state

    def select(self, node):
        # Constants
        c = sqrt(2)

        wi = node.wins
        Ni = node.parent.visits
        ni = node.visits

        # If node has not been visited yet
        if not Ni or not ni:
            value = inf
        # if not Ni:
        #     Ni = inf
        # if not ni:
        #     ni = inf

        else:
            value = wi / ni + c * sqrt(log(Ni) / ni)

        return value

    # def reset(self, board_state, move):
    #     self.state = copy.copy(board_state)
    #     x, y = move
    #     self.state[x][y] = self.turn[self.turn_state]
    #     self.logic.MCTS_GAME_OVER = False
    #     self.turn_state = True
