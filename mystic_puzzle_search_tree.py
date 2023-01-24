"""
3x3 mystic puzzle game.
Goal state: [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
1 2 3
4 5 6
7 8 0
Where 0 is the empty tile.
"""
import numpy as np
import random
import time

ALL_TILES = [1, 2, 3, 4, 5, 6, 7, 8, 0]
BOARD_SHAPE = [3, 3]
OPERATIONS = ["right", "left", "up", "down", 'r', 'l', 'u', 'd']  # Used in move_empty_tile
if (BOARD_SHAPE[0] * BOARD_SHAPE[1]) != len(ALL_TILES):
    raise(ValueError("Amount of tiles {} don't fill the board shape {}x{}."
                     .format(len(ALL_TILES), BOARD_SHAPE[0], BOARD_SHAPE[1])))

# States
goal_state = np.reshape(ALL_TILES, BOARD_SHAPE)
random.shuffle(ALL_TILES)
start_state = np.reshape(ALL_TILES, BOARD_SHAPE)


def print_state(state: np.ndarray) -> None:
    """Prints the state list."""
    for row in state:
        p = ""
        for tile in row:
            p += str(tile) + " "
        print(p)


# Visualizing initial states
print("Goal state:")
print_state(goal_state)
print("Start state:")
print_state(start_state)


def move_empty_tile(state: np.ndarray, direction: str) -> np.ndarray:
    """Swaps the empty tile with the tile to its direction. Expects no boarder to the direction."""
    empty_loc = np.where(state == 0)
    empty_loc = [empty_loc[0][0], empty_loc[1][0]]
    if direction == OPERATIONS[0] or direction == OPERATIONS[4]:  # Operation right
        move_loc = [empty_loc[0], empty_loc[1] + 1]
    elif direction == OPERATIONS[1] or direction == OPERATIONS[5]:  # Operation left
        move_loc = [empty_loc[0], empty_loc[1] - 1]
    elif direction == OPERATIONS[2] or direction == OPERATIONS[6]:  # Operation up
        move_loc = [empty_loc[0] - 1, empty_loc[1]]
    elif direction == OPERATIONS[3] or direction == OPERATIONS[7]:  # Operation down
        move_loc = [empty_loc[0] + 1, empty_loc[1]]
    else:
        raise ValueError("Direction {} isn't allowed in moving the tile. Try: right, left, up, or down."
                         .format(direction))
    state[empty_loc[0]][empty_loc[1]] = state[move_loc[0]][move_loc[1]]
    state[move_loc[0]][move_loc[1]] = 0
    return state


# Play the game
game_over = False
player_state = start_state
print("Starting timer...")
start_time = time.time()
move_count = 0
while not game_over:
    player_move = None
    while player_move not in OPERATIONS:
        player_move = input("Move the empty tile which direction: ")
    player_state = move_empty_tile(player_state, player_move)
    move_count += 1
    print("Updated state:")
    print_state(player_state)
    if player_state.flatten().tolist() == goal_state.flatten().tolist():
        game_over = True
player_time = (time.time() - start_time)
print("Yay you won!\nIt took you {} seconds and {} moves."
      "\nLet's see how long a simple binary search tree can do it in!".format(player_time, move_count))


# class NonBinTree:
#
#     def __init__(self, val):
#         self.val = val
#         self.nodes = []
#
#     def add_node(self, val):
#         self.nodes.append(NonBinTree(val))
#
#     def __repr__(self):
#         return f"NonBinTree({self.val}): {self.nodes}"
#
#
# a = NonBinTree(0)
# a.add_node(1)
# a.add_node(3)
# a.add_node(4)
# a.nodes[2].add_node(2)
#
# print(a)
# TODO: Limited breadth first search for the goal
# TODO: Custom heuristic addition (loss?!?!?!)
