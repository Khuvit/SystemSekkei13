# game_logic.py

ROWS, COLS = 8, 8

# Othello board (0: empty, 1: white, 2: black)
board = [[0] * COLS for _ in range(ROWS)]
board[3][3] = board[4][4] = 1  # White pieces (White = 1)
board[3][4] = board[4][3] = 2  # Black pieces (Black = 2)

# Convert board position to move notation (e.g., (3, 4) → "D4")
def get_move_notation(row, col):
    col_letters = "ABCDEFGH"
    return f"{col_letters[col]}{row+1}"

# Check if the move is valid (simplified, needs full Othello logic)
def is_valid_move(row, col, player):
    if board[row][col] != 0:
        return False  # Can't place on occupied spots
    # TODO: Implement Othello rule checking (flip logic)
    return True

# Place a piece and update board
def place_piece(row, col, player):
    if is_valid_move(row, col, player):
        board[row][col] = player  # Update board
        return get_move_notation(row, col)  # Return notation for ESP32
    return None  # Move was invalid
