"""
3x3 tile sliding puzzle game.
Goal state: [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
1 2 3
4 5 6
7 8 0
Where 0 is the empty tile.
"""
from copy import deepcopy
import numpy as np
import random
import time

ALL_TILES = [1, 2, 3, 4, 5, 6, 7, 8, 0]
BOARD_SHAPE = [3, 3]
OPERATIONS = ["right", "left", "up", "down", 'r', 'l', 'u', 'd']  # Used in move_empty_tile
AVG_OPS_PER_TURN = 3
TREE_DEPTH = 10  # Generate AVG_OPS_PER_TURN**TREE_DEPTH amount of nodes (depending on board size, memory issues...)
if (BOARD_SHAPE[0] * BOARD_SHAPE[1]) != len(ALL_TILES):
    raise ValueError("Amount of tiles {} don't fill the board shape {}x{}."
                     .format(len(ALL_TILES), BOARD_SHAPE[0], BOARD_SHAPE[1]))
if (AVG_OPS_PER_TURN**TREE_DEPTH) >= 1e9:  # If nodes larger than 1 billion, print memory warning
    raise Warning("Generating {} nodes for the search tree. May run into memory issues."
                  .format(AVG_OPS_PER_TURN**TREE_DEPTH))

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
    new_state = deepcopy(state)  # Don't want to change the previous states in the search tree
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
    new_state[empty_loc[0]][empty_loc[1]] = state[move_loc[0]][move_loc[1]]
    new_state[move_loc[0]][move_loc[1]] = 0
    return new_state


def get_possible_moves(state: np.ndarray) -> list:
    """Gets the possible operations that can be performed on the state."""
    moves = []
    empty_loc = np.where(state == 0)
    empty_loc = [empty_loc[0][0], empty_loc[1][0]]
    if empty_loc[1] + 1 < BOARD_SHAPE[1]:  # Operation right
        moves.append(OPERATIONS[4])
    if empty_loc[1] - 1 >= 0:  # Operation left
        moves.append(OPERATIONS[5])
    if empty_loc[0] - 1 >= 0:  # Operation up
        moves.append(OPERATIONS[6])
    if empty_loc[0] + 1 < BOARD_SHAPE[0]:  # Operation down
        moves.append(OPERATIONS[7])
    return moves


# Play the game
play_game = input("\nWould you like to play a game?\n")
if play_game == "yes" or play_game == 'y':
    game_over = False
    player_state = start_state
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
          "\nLet's see how long a simple search tree can do it in!".format(player_time, move_count))


class NonBinTree:
    """A non binary tree class."""
    def __init__(self, val) -> None:
        self.val = val
        self.nodes = []

    def add_node(self, val) -> None:
        self.nodes.append(NonBinTree(val))

    def get_lowest_nodes(self) -> list:
        lowest_nodes = []
        for node in self.nodes:
            if len(node.nodes):  # If the node has children apply this method to them
                lowest_nodes += node.get_lowest_nodes()
            else:  # If no children, add the low node to the list
                lowest_nodes.append(node)
        return lowest_nodes

    def __repr__(self) -> str:
        return f"NonBinTree({self.val}): {self.nodes}"


# Use a search tree to calculate the quickest path to the solution
print("\nGenerating a tree with depth of {} (~{} nodes)...".format(TREE_DEPTH, AVG_OPS_PER_TURN**TREE_DEPTH))
start_time = time.time()
start_tree = NonBinTree(start_state)
total_nodes = 0
for depth in range(TREE_DEPTH):
    # Breadth first search... More like breadth first node creation! LOL
    print("Calculating the nodes at depth {}...".format(depth))
    if depth == 0:
        current_state = start_tree.val  # Depth = 0
        p_moves = get_possible_moves(current_state)
        for m in p_moves:
            next_state = move_empty_tile(current_state, m)
            start_tree.add_node(next_state)
            total_nodes += 1
    else:
        low_nodes = start_tree.get_lowest_nodes()
        for n in low_nodes:  # Depths >= 1
            current_state = n.val
            p_moves = get_possible_moves(current_state)
            for m in p_moves:
                next_state = move_empty_tile(current_state, m)
                n.add_node(next_state)
                total_nodes += 1
tree_time = (time.time() - start_time)
# print(start_tree)
print("It took {} seconds to generate a tree with a depth of {} and {} nodes."
      .format(tree_time, TREE_DEPTH, total_nodes))

# TODO: Breadth first search for the goal (get trace of moves when retrieving quickest goal state)
# TODO: Custom heuristic addition (loss?!?!?!)
