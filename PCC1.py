import pygame
import serial
import time

# Setup Bluetooth Serial Connection
ESP32_COM_PORT = "COM5"  # Change this based on your PC's Bluetooth COM port
BAUD_RATE = 115200

try:
    esp32 = serial.Serial(ESP32_COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Give time to establish connection
    print("Connected to ESP32 Bluetooth")
except serial.SerialException:
    print("Could not connect to ESP32. Check Bluetooth pairing & COM port.")
    esp32 = None

# Initialize Pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 8, 8
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

# Othello board (0: empty, 1: white, 2: black)
board = [[0] * COLS for _ in range(ROWS)]
board[3][3] = board[4][4] = 1  # White pieces
board[3][4] = board[4][3] = 2  # Black pieces

# Draw board
def draw_board():
    screen.fill(GREEN)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 2)

            if board[row][col] == 1:
                pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE//3)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE//3)

    pygame.display.update()

# Convert board position to move notation (e.g., (3, 4) → "D4")
def get_move_notation(row, col):
    col_letters = "ABCDEFGH"
    return f"{col_letters[col]}{row+1}"

# Main game loop
running = True
current_player = 2  # Black starts
while running:
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // CELL_SIZE, y // CELL_SIZE

            if board[row][col] == 0:  # Only allow move on empty spaces
                board[row][col] = current_player
                move_notation = get_move_notation(row, col)
                print(f"Move: {move_notation}")

                # Send move to ESP32 via Bluetooth
                if esp32:
                    esp32.write(move_notation.encode())
                    print(f"Sent: {move_notation}")

                # Switch player
                current_player = 1 if current_player == 2 else 2

pygame.quit()
if esp32:
    esp32.close()
