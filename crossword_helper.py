"""
crossword board =  # the FILLER char is a no-go and spaces are empty slots for letters.
["cat",
 " n ",
 " t "]
"""

FILLER = '#'


def get_board() -> list:
    """Gets the board from the user."""
    board = []
    board_dim = int(input("Enter board width (integer >= 2): "))
    for r in range(board_dim):
        in_row = input("Enter the {}th row of letters (' ' are empty squares and '{}' are filled squares): "
                       .format(r + 1, FILLER))
        board.append(in_row)
    return board


def print_board(board: list) -> None:
    """Prints the board in a visually appealing way (better than printing a list lol)."""
    for row in board:
        for letter in row:
            print(letter, end=" ")
        print(end="\n")


def get_across(board: list, n: int) -> str:
    """Retrieves the nth across word on the board and returns the string (with empty spaces)."""
    all_row_words = []
    for row in board:
        row_words = row.split(FILLER)
        for word in row_words:  # Iterates through words and removes empty splits and single letters
            if len(word) > 1:
                all_row_words.append(word)
    if n - 1 >= len(all_row_words) or n <= 0:
        raise KeyError("Across number {} is out of bounds for all across words. {} across words total."
                       .format(n, len(all_row_words)))
    print(all_row_words)
    return all_row_words[n - 1]


def get_down(board: list, n: int) -> str:
    """Retrieves the nth down word on the board and returns the string (with empty spaces)."""


puzzle = get_board()
print_board(puzzle)
get_across(puzzle, 1)
