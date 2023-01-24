"""
3x3 mystic puzzle game.
Goal state: [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
1 2 3
4 5 6
7 8 0
"""
import numpy as np
import random

ALL_TILES = [1, 2, 3, 4, 5, 6, 7, 8, 0]
BOARD_SHAPE = [3, 3]

goal_state = np.reshape(ALL_TILES, BOARD_SHAPE).tolist()
random.shuffle(ALL_TILES)
start_state = np.reshape(ALL_TILES, BOARD_SHAPE).tolist()


def state_print(state: list) -> None:
    """Prints the state list."""
    for row in state:
        p = ""
        for tile in row:
            p += str(tile) + " "
        print(p)


print("Goal state:")
state_print(goal_state)
print("Start state:")
state_print(start_state)


class NonBinTree:

    def __init__(self, val):
        self.val = val
        self.nodes = []

    def add_node(self, val):
        self.nodes.append(NonBinTree(val))

    def __repr__(self):
        return f"NonBinTree({self.val}): {self.nodes}"


a = NonBinTree(0)
a.add_node(1)
a.add_node(3)
a.add_node(4)
a.nodes[2].add_node(2)

print(a)
# TODO: Limited breadth first search for the goal
# TODO: Custom heuristic addition (loss?!?!?!)
