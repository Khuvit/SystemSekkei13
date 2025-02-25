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

def is_valid_move(row, col, player):
    if row < 0 or row >= 8 or col < 0 or col >= 8:
        return False  # 盤外には置けない
    if board[row][col] != 0:
        return False  # 空きマスでない場合は無効
    
    opponent = 1 if player == 2 else 2  # 相手の色
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        
        # 隣が相手の石でなければ無効
        if not (0 <= r < 8 and 0 <= c < 8) or board[r][c] != opponent:
            continue
        
        # さらにその先を探索
        while 0 <= r < 8 and 0 <= c < 8:
            r += dr
            c += dc
            
            if not (0 <= r < 8 and 0 <= c < 8):
                break
            
            if board[r][c] == 0:
                break  # 空白に到達したら無効
            
            if board[r][c] == player:
                return True  # 自分の石に挟まれたら有効
    
    return False

def place_piece(row, col, player):
    if not is_valid_move(row, col, player):
        return None  # 無効な手なら何もしない
    
    board[row][col] = player  # 石を置く
    opponent = 1 if player == 2 else 2  # 相手の色
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        stones_to_flip = []
        
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            stones_to_flip.append((r, c))
            r += dr
            c += dc
        
        # 相手の石に挟まれて自分の石が来る場合、石を裏返す
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for fr, fc in stones_to_flip:
                board[fr][fc] = player  # 石を裏返す
    
    return get_move_notation(row, col)


def count_stones():
    black, white = 0, 0
    for row in board:
        black += row.count(2)
        white += row.count(1)
    return black, white

def has_valid_moves(player):
    for r in range(8):
        for c in range(8):
            if is_valid_move(r, c, player):
                return True
    return False

def check_game_end():
    if not has_valid_moves(1) and not has_valid_moves(2):
        black, white = count_stones()
        if black > white:
            return "Black wins!"
        elif white > black:
            return "White wins!"
        else:
            return "It's a draw!"
    return None

def pass_turn(current_player):
    if not has_valid_moves(current_player):
        return 3 - current_player  # プレイヤーを交代
    return current_player


# Place a piece and update board
def place_piece(row, col, player):
    if is_valid_move(row, col, player):
        board[row][col] = player  # Update board
        return get_move_notation(row, col)  # Return notation for ESP32
    return None  # Move was invalid