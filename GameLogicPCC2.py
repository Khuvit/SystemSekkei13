ROWS, COLS = 8, 8

# 0 = empty, 1 = white, 2 = black
board = [[0]*COLS for _ in range(ROWS)]

# Initial 4 pieces in the center
board[3][3] = board[4][4] = 1  # White
board[3][4] = board[4][3] = 2  # Black

def get_move_notation(row, col):
    col_letters = "ABCDEFGH"
    return f"{col_letters[col]}{row+1}"

def is_valid_move(row, col, player):
    if not (0 <= row < 8 and 0 <= col < 8):
        return False
    if board[row][col] != 0:
        return False

    opponent = 1 if player == 2 else 2
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        found_opponent = False

        # Must have at least one opponent piece next in that direction
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            found_opponent = True
        else:
            continue

        # Keep going in this direction until we find the player's piece or run out
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            r += dr
            c += dc

        # If we ended on the player's piece, we have a valid flip
        if found_opponent and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            return True

    return False

def place_piece(row, col, player):
    """
    Places a piece on the board if valid, and flips opponent pieces.
    Returns the move notation (e.g. "D3") if successful, or None if invalid.
    """
    if not is_valid_move(row, col, player):
        return None

    board[row][col] = player
    opponent = 1 if player == 2 else 2

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    # Flip stones in each valid direction
    for dr, dc in directions:
        r, c = row + dr, col + dc
        stones_to_flip = []

        # Gather opponent stones in a row
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            stones_to_flip.append((r, c))
            r += dr
            c += dc

        # If we end on our own piece, flip everything in stones_to_flip
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for flip_r, flip_c in stones_to_flip:
                board[flip_r][flip_c] = player

    return get_move_notation(row, col)

def has_valid_moves(player):
    for r in range(8):
        for c in range(8):
            if is_valid_move(r, c, player):
                return True
    return False

def check_game_end():
    if not has_valid_moves(1) and not has_valid_moves(2):
        # Count stones
        black = sum(row.count(2) for row in board)
        white = sum(row.count(1) for row in board)
        if black > white:
            return "Black wins!"
        elif white > black:
            return "White wins!"
        else:
            return "It's a draw!"
    return None
