import pygame
import serial
import time
from GameLogicPCC2 import board, place_piece, is_valid_move, check_game_end, has_valid_moves

ESP32_COM_PORT = "COM13"
BAUD_RATE = 115200

def setup_serial():
    """ Establish a Bluetooth Serial connection to ESP32 via COM12 """
    try:
        esp32 = serial.Serial(ESP32_COM_PORT, BAUD_RATE, timeout=1)
        time.sleep(5)  # Give time to establish connection(looks like 5 is enough)
        print(f"Connected to ESP32 on {ESP32_COM_PORT} at {BAUD_RATE} baud")
        return esp32
    except serial.SerialException:
        print("Could not connect to ESP32. Check Bluetooth pairing & COM port (COM13).")
        return None

esp32 = setup_serial()

pygame.init()

WIDTH, HEIGHT = 400, 400
ROWS, COLS = 8, 8
CELL_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

def draw_board():
    """ Draws the Othello board from the 'board' array in GameLogicPCC21 """
    screen.fill(GREEN)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 2)

            if board[row][col] == 1:  # White piece
                pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE // 3)
            elif board[row][col] == 2:  # Black piece
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 3)

    pygame.display.update()

def send_move_to_esp32(move_notation):
    """ Sends a move (e.g., 'D4') to the ESP32 via Bluetooth Serial """
    if esp32 and esp32.is_open:
        try:
            esp32.write(move_notation.encode() + b"\n")
            print(f"Sent move to ESP32: {move_notation}")
        except serial.SerialException:
            print("Bluetooth error: Failed to send data. Check connection.")

running = True
current_player = 2  # Starting with Black pieces

while running:
    draw_board()  #Show the latest board

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if is_valid_move(row, col, current_player):
                move_notation = place_piece(row, col, current_player)
                if move_notation:
                    print(f"Move made: {move_notation}")

                    send_move_to_esp32(move_notation)

                    # Check if game ended
                    result = check_game_end()
                    if result:
                        print("Game Over:", result)
                        running = False
                        break

                    # Switch to next player if they have moves(Player configuration)
                    next_player = 3 - current_player
                    if has_valid_moves(next_player):
                        current_player = next_player
                else:
                    print("Invalid move or no flipping occurred.")
pygame.quit()
if esp32:
    esp32.close()
    print("Bluetooth connection closed.")
