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
board = [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]

# INPUTS:
n_queens = 9
queen_range = 4
# This will change as queens move (initial indices from 1-8)
queen_locations = [[1, 7], [2, 4], [3, 8], [4, 1], [4, 6], [5, 5], [6, 2], [7, 2], [8, 3]]
for i, row in enumerate(queen_locations):  # Puts input in 0-7 index scale
    for j, col in enumerate(row):
        queen_locations[i][j] = col - 1

# Place the queens on the BOARD
for loc in queen_locations:
    board[loc[0]][loc[1]] = 1


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
    return cons, q_con


num_conflicts, queen_conflicts = calc_conflicts(board, queen_locations)
print("--------------------------------------------------")
print("Initial state:")
print_stats(board, num_conflicts, queen_conflicts, queen_locations)

# Keep statistics as the hill climbing chooses future answers
state_transitions = 0
neighboring_states_viewed = 0
failed_better = 0
game_over = False
# Creates a list of all possible places to move this queen (neighboring states)
possible_moves = []
for i in range(8):
    for j in range(8):
        possible_moves.append([i, j])

while not game_over:
    state_transitions += 1
    prev_conflicts = deepcopy(num_conflicts)
    prev_queen_conflicts = deepcopy(queen_conflicts)
    print("--------------------------------------------------")
    # Finds the queen with the most conflicts
    worst_queen_index = int(queen_conflicts.index(max(queen_conflicts)))
    worst_queen_loc = queen_locations[worst_queen_index]
    # Removes the worst queen from the board
    board[worst_queen_loc[0]][worst_queen_loc[1]] = 0
    # Initializes there is no best next state yet
    best_neighbor_board = None
    best_neighbor_queen_locations = None
    best_neighbor_num_conflicts = 1000000000  # Large because we want smaller number of conflicts
    for poss_loc in possible_moves:  # Iterates through neighboring states
        if board[poss_loc[0]][poss_loc[1]] == 0 and poss_loc != worst_queen_loc:  # If no queen in current space
            neighboring_states_viewed += 1
            # Moves the queen to the new possible location and calculates the number of conflicts
            board[poss_loc[0]][poss_loc[1]] = 1
            queen_locations[worst_queen_index] = poss_loc
            num_conflicts, _ = calc_conflicts(board, queen_locations)
            if best_neighbor_board is None:  # Gives the first state as the best neighbor state (for now at least)
                best_neighbor_board = deepcopy(board)
                best_neighbor_queen_locations = deepcopy(queen_locations)
                best_neighbor_num_conflicts = num_conflicts
            if num_conflicts < best_neighbor_num_conflicts:  # If best neighbor (least conflict neighbor)
                best_neighbor_board = deepcopy(board)
                best_neighbor_queen_locations = deepcopy(queen_locations)
                best_neighbor_num_conflicts = num_conflicts
            board[poss_loc[0]][poss_loc[1]] = 0  # Reset the board for the next state
    if best_neighbor_num_conflicts <= prev_conflicts:  # If better state found
        if best_neighbor_num_conflicts == prev_conflicts:  # Finds an equal state
            failed_better += 1
        else:  # Finds a better state
            failed_better = 0
        print("State {} (moved queen {}):".format(state_transitions, worst_queen_index + 1))
        best_neighbor_num_conflicts, queen_conflicts = calc_conflicts(best_neighbor_board,
                                                                      best_neighbor_queen_locations)
        print_stats(best_neighbor_board, best_neighbor_num_conflicts, queen_conflicts, best_neighbor_queen_locations)
    else:  # If all next states are worse
        print("Tried moving queen {}. No better or equal states found.".format(worst_queen_index + 1))
    if failed_better == 60:
        game_over = True
    if best_neighbor_num_conflicts == 0:
        game_over = True

print("--------------------------------------------------")
print("Total state transitions: {}".format(state_transitions))
print("Total neighboring states viewed: {}".format(neighboring_states_viewed))
