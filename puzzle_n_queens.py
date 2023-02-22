"""
8x8 chess board n queens problem.
Inputs: Number of queens, range of queen movement, location of queens.
Goal state               Indices
0  0  1  0  0  0  0  0 | 00 01 02 03 04 05 06 07
0  0  0  0  0  1  0  0 | 10 11 12 13 14 15 16 17
0  0  0  0  0  0  0  1 | 20 21 22 23 24 25 26 27
1  0  0  0  0  0  0  0 | 30 31 32 33 34 35 36 37
0  0  0  1  0  0  0  0 | 40 41 42 43 44 45 46 47
0  0  0  0  0  0  1  0 | 50 51 52 53 54 55 56 57
0  0  0  0  1  0  0  0 | 60 61 62 63 64 65 66 67
0  1  0  0  0  0  0  0 | 70 71 72 73 74 75 76 77
Where 0 is an empty tile and 1 is a queen.
"""
from copy import deepcopy
import math
import random
BOARD = [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]

########## INPUTS ##########
# Change these to test the code on new input patterns
n_queens = 10
queen_range = 5
# This will change as queens move (initial indices from 1-8)
queen_locations = [[1, 7], [2, 4], [2, 5], [3, 8], [4, 1], [4, 6], [5, 5], [6, 2], [7, 2], [8, 3]]

for i, row in enumerate(queen_locations):  # Puts input in 0-7 index scale
    for j, col in enumerate(row):
        queen_locations[i][j] = col - 1


def print_stats(bd: list, nc: int, qcs: list, qls: list) -> None:
    """Prints the board."""
    print("  0 1 2 3 4 5 6 7")
    b = deepcopy(bd)
    for index, ql in enumerate(qls):
        b[ql[0]][ql[1]] = index + 1
    for index, r in enumerate(b):
        print(str(index) + " " + str(r).replace("[", "").replace("]", "").replace(",", "").replace("0", "-"))
    print("Total conflicts: {}".format(nc))
    for index, conflict in enumerate(qcs):
        print("Q{} = {}".format(index + 1, conflict), end="\t\t")
    print()
    for index, location in enumerate(qls):
        print("Q{} = {}".format(index + 1, location), end="\t")
    print()


def calc_conflicts(b: list, qls: list) -> (int, list):
    """The heuristic for calculating the number of conflicts on the board."""
    cons = 0
    q_con = []
    for q in qls:  # Checks each queen location with queen_range as the conflict
        curr_con = 0
        # Check row for conflicts within queen_range
        for in_r in range(q[1] - queen_range, q[1] + queen_range + 1):
            if in_r != q[1] and (0 <= in_r <= 7):
                curr_con += b[q[0]][in_r]
        # Check column for conflicts within queen_range
        for in_c in range(q[0] - queen_range, q[0] + queen_range + 1):
            if in_c != q[0] and (0 <= in_c <= 7):
                curr_con += b[in_c][q[1]]
        # Check diagonal tl to br
        for in_r, in_c in zip(range(q[1] - queen_range, q[1] + queen_range + 1),
                              range(q[0] - queen_range, q[0] + queen_range + 1)):
            if in_r != q[1] and (0 <= in_r <= 7) and in_c != q[0] and (0 <= in_c <= 7):
                curr_con += b[in_c][in_r]
        # Check diagonal tr to bl
        for in_r, in_c in zip(range(q[1] - queen_range, q[1] + queen_range + 1),
                              reversed(range(q[0] - queen_range, q[0] + queen_range + 1))):
            if in_r != q[1] and (0 <= in_r <= 7) and in_c != q[0] and (0 <= in_c <= 7):
                curr_con += b[in_c][in_r]
        q_con.append(curr_con)
        cons += curr_con
    cons /= 2  # Gets every queen conflict, so conflicts are detected twice
    return math.ceil(cons), q_con


class SearchTree:
    def __init__(self, bd, qls) -> None:
        self.board = deepcopy(bd)
        self.queen_locations = deepcopy(qls)
        self.conflicts, _ = calc_conflicts(self.board, self.queen_locations)
        self.nodes = []

    def add_node(self, bd, qls) -> None:
        self.nodes.append(SearchTree(bd, qls))

    def get_best_child(self):
        lowest = self.conflicts
        best_node = self.nodes[0]
        random.shuffle(self.nodes)
        for n in self.nodes:
            if n.conflicts <= lowest:
                lowest = n.conflicts
                best_node = n
        return best_node


# Place the queens on the board
board = deepcopy(BOARD)
for loc in queen_locations:
    board[loc[0]][loc[1]] = 1
num_conflicts, queen_conflicts = calc_conflicts(board, queen_locations)
print("--------------------------------------------------")
print("Initial state:")
print_stats(board, num_conflicts, queen_conflicts, queen_locations)

# Keep statistics as the hill climbing chooses future answers
state_transitions = 0
neighboring_states_viewed = 0
game_over = False
# Create a consistent list of all the possible spots for a queen to move
possible_locations = []
for i in range(8):
    for j in range(8):
        possible_locations.append([i, j])

while not game_over:
    state_transitions += 1
    next_search_tree = SearchTree(board, queen_locations)
    for qi, queen_loc in enumerate(queen_locations):
        for poss_loc in possible_locations:
            if poss_loc != queen_loc and board[poss_loc[0]][poss_loc[1]] == 0:
                neighboring_states_viewed += 1
                board[queen_loc[0]][queen_loc[1]] = 0  # Removes where the queen used to be
                board[poss_loc[0]][poss_loc[1]] = 1  # Adds where the queen is moved to
                queen_locations[qi] = poss_loc  # Updates the queens location
                next_search_tree.add_node(board, queen_locations)
                # Reverts the queen movement on the board and in the queen_locations
                board[queen_loc[0]][queen_loc[1]] = 1
                board[poss_loc[0]][poss_loc[1]] = 0
                queen_locations[qi] = queen_loc
    best_child = next_search_tree.get_best_child()
    board = best_child.board
    queen_locations = best_child.queen_locations
    num_conflicts, queen_conflicts = calc_conflicts(board, queen_locations)
    if num_conflicts == 0:
        game_over = True
        print("--------------------------------------------------")
        print("Solution state found.")
        print("State {}:".format(state_transitions))
        print_stats(board, num_conflicts, queen_conflicts, queen_locations)
    if state_transitions <= 4 and (game_over is not True):
        print("--------------------------------------------------")
        print("State {}:".format(state_transitions))
        print_stats(board, num_conflicts, queen_conflicts, queen_locations)
    if state_transitions == 60:
        game_over = True
        print("--------------------------------------------------")
        print("60 state transitions have occurred and no solution has been found. Giving up :(")
        print("State {}:".format(state_transitions + 1))
        print_stats(board, num_conflicts, queen_conflicts, queen_locations)

print("WARNING: The choice of the next best state is random (when there is a tie), "
      "there may be some variance in outputs from run to run!")
print("Total state transitions: {}".format(state_transitions))
print("Total neighboring states viewed: {}".format(neighboring_states_viewed))
