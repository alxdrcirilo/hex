import copy
from math import log, sqrt, inf
from random import choice

import numpy as np
from rich.console import Console
from rich.progress import track
from rich.table import Table


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

    def start(self, itermax: int, verbose: bool = False):
        root_node = Node(self.logic, self.root_state)

        for _ in track(range(itermax), description="MCTS:", total=itermax):
            node = root_node
            state = copy.deepcopy(self.root_state)
            self.turn_state = True

            # Select
            while node.untried_moves == [] and node.children != []:
                # Node is fully expanded and non-terminal
                uct_values = [self.select(child) for child in node.children]
                # TODO: is this correct?
                if all([value == inf for value in uct_values]):
                    node = choice(node.children)
                else:
                    node = node.children[np.argmax(uct_values)]

                x, y = node.move
                state[x][y] = self.turn[self.turn_state]
                self.next_turn()

            # Expand
            if node.untried_moves != []:
                x, y = choice(node.untried_moves)
                state[x][y] = self.turn[self.turn_state]
                node.untried_moves.remove((x, y))
                node.add_child(Node(self.logic, state, (x, y)))
                self.next_turn()

            # Playout
            # TODO: For some reason, self.logic.get_possible_moves(state) must be added
            while not self.logic.MCTS_GAME_OVER and self.logic.get_possible_moves(state):
                x, y = choice(self.logic.get_possible_moves(state))
                state[x][y] = self.turn[self.turn_state]

                for player in [1, 2]:
                    global winner
                    winner = self.logic.is_game_over(player, state, True)
                    if winner:
                        break

                self.next_turn()

            # Reset MCTS_GAME_OVER
            self.logic.MCTS_GAME_OVER = False

            # Backpropagation
            while node != None:
                win_value = 1 if winner is self.starting_player else 0

                node.wins += win_value
                node.visits += 1
                node = node.parent

            root_node.wins += win_value
            root_node.visits += 1

        # TODO: is this correct?
        # result = root_node.children[np.argmax([self.select(node) for node in root_node.children])].move
        result = root_node.children[np.argmax([node.visits for node in root_node.children])].move

        output = [(node.wins, node.visits, node.move) for node in root_node.children]
        if verbose:
            self.print_output(output, result)

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

        else:
            value = wi / ni + c * sqrt(log(Ni) / ni)

        return value

    def print_output(self, output, result):
        console = Console()

        table = Table(show_header=True, header_style="bold red")
        table.add_column("Wins", justify="center")
        table.add_column("Visits", justify="center")
        table.add_column("Move", justify="center")
        for row in output:
            if row[2] == result:
                w = "[cyan]" + str(row[0]) + "[/cyan]"
                v = "[cyan]" + str(row[1]) + "[/cyan]"
                m = "[cyan]" + str(row[2]) + "[/cyan]"
            else:
                w = str(row[0])
                v = str(row[1])
                m = str(row[2])
            table.add_row(w, v, m)

        console.print(table)
