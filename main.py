import pygame, sys, time, random
from pygame.locals import *

pygame.init()

# Window dimensions
WIDTH, HEIGHT = 900, 900

# Create the game screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window
pygame.display.set_caption("Tic Tac Toe!")


# Colors for the game
BG_COLOR = (214, 201, 227)  # Background color
LINE_COLOR = (0, 0, 0)  # Line color
X_COLOR = (255, 0, 0)  # X marker color
O_COLOR = (0, 0, 255)  # O marker color


# Initialize the board as a 3x3 grid with None
board = [[None, None, None], [None, None, None], [None, None, None]]


# Fonts for text display
FONT = pygame.font.Font(None, 100)
SMALL_FONT = pygame.font.Font(None, 60)


# Initialize variables for game logic
to_move = None  # To keep track of whose turn it is
winner_message = None  # To display the winner
game_finished = False  # Flag to check if the game is over
selection_done = False  # Flag for player selection


# Draw the game grid
def draw_custom_grid():
    for x in range(1, 3):
        # Draw vertical lines
        pygame.draw.line(SCREEN, LINE_COLOR, (x * 300, 0), (x * 300, HEIGHT), 5)
        # Draw horizontal lines
        pygame.draw.line(SCREEN, LINE_COLOR, (0, x * 300), (WIDTH, x * 300), 5)


# Render the current state of the board
def render_board(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                # Draw X markers
                start_pos1 = (j * 300 + 50, i * 300 + 50)
                end_pos1 = (j * 300 + 250, i * 300 + 250)
                start_pos2 = (j * 300 + 50, i * 300 + 250)
                end_pos2 = (j * 300 + 250, i * 300 + 50)
                pygame.draw.line(SCREEN, X_COLOR, start_pos1, end_pos1, 10)
                pygame.draw.line(SCREEN, X_COLOR, start_pos2, end_pos2, 10)
            elif board[i][j] == 'O':
                # Draw O markers
                center = (j * 300 + 150, i * 300 + 150)
                pygame.draw.circle(SCREEN, O_COLOR, center, 100, 10)


# Display messages on the screen
def display_message(message, y_offset=0):
    text = FONT.render(message, True, (255, 0, 0))  # Red color
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    SCREEN.blit(text, text_rect)


# Initialize player move
def add_X(board, marker):
    """
    Place the player's marker (X) on the board based on mouse click.
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse click position
    row = mouse_y // 300  # Determine row
    col = mouse_x // 300  # Determine column

    if board[row][col] is None:  # Place marker only if the cell is empty
        board[row][col] = marker

    return board


# Initialize AI move
def ai_move(board):
    """
    AI places its marker (O) on the board.
    1. Tries to win.
    2. Blocks X if it is about to win.
    3. Picks a random empty cell if no immediate threat or win is found.
    """
    # Check for a winning move for AI (O)
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:  # If the cell is empty
                board[i][j] = 'O'
                if infer_winner(board) == 'O':  # Check if this move wins
                    return board
                board[i][j] = None  # Undo the move

    # Check to block opponent's winning move (X)
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:  # If the cell is empty
                board[i][j] = 'X'
                if infer_winner(board) == 'X':  # Check if X wins here
                    board[i][j] = 'O'  # Block the win by placing O
                    return board
                board[i][j] = None  # Undo the move

    # Choose a random empty cell
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 'O'

    return board


# Forward chaining inference rules
def infer_winner(board):
    """
    Apply inference rules to determine the winner.
    """
    # Rule: Check rows for a winner
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]  # The player occupying the row wins

    # Rule: Check columns for a winner
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]  # The player occupying the column wins

    # Rule: Check diagonals for a winner
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]  # Player occupying the main diagonal wins
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]  # Player occupying the anti-diagonal wins

    # Rule: Check for a draw (no empty spaces left)
    for row in board:
        if None in row:
            return None  # Game not finished yet

    return "DRAW"  # If no spaces left, it's a draw


# Main game loop
while True:
    # Event loop to handle user interactions like mouse clicks or window closing
    for event in pygame.event.get():
        if event.type == QUIT:  # Check if the user wants to close the game window
            pygame.quit()  # Exit Pygame
            sys.exit()  # Exit the Python script

        # Check if player selection (X or O) is not done yet
        if not selection_done:
            if event.type == MOUSEBUTTONDOWN:  # Check if the user clicked the mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Get the position of the mouse click
                # Check if the click was in the X button area
                if 200 <= mouse_x <= 400 and 400 <= mouse_y <= 500:
                    to_move = 'X'  # Player chooses to be 'X'
                    selection_done = True  # Mark that the player selection is done
                # Check if the click was in the O button area
                elif 500 <= mouse_x <= 700 and 400 <= mouse_y <= 500:
                    to_move = 'O'  # Player chooses to be 'O'
                    selection_done = True  # Mark that the player selection is done
        else:
            # If the current turn belongs to player X
            if event.type == MOUSEBUTTONDOWN and to_move == 'X' and not game_finished:
                board = add_X(board, 'X')  # Add X to the board at the selected position
                winner = infer_winner(board)  # Check if there is a winner or a draw
                if winner == 'X':  # If X is the winner
                    winner_message = "X Wins!"  # Display "X Wins" message
                    game_finished = True  # Mark the game as finished
                elif winner == 'DRAW':  # If the game ends in a draw
                    winner_message = "It's a Draw!"  # Display draw message
                    game_finished = True  # Mark the game as finished
                else:
                    to_move = 'O'  # Switch the turn to AI (O)

    # Handle AI's turn (O's turn)
    if selection_done and to_move == 'O' and not game_finished:
        time.sleep(0.5)  # Add a small delay for AI's move to feel natural
        board = ai_move(board)  # AI makes its move
        winner = infer_winner(board)  # Check if there is a winner or a draw
        if winner == 'O':  # If AI (O) wins
            winner_message = "O Wins!"  # Display "O Wins" message
            game_finished = True  # Mark the game as finished
        elif winner == 'DRAW':  # If the game ends in a draw
            winner_message = "It's a Draw!"  # Display draw message
            game_finished = True  # Mark the game as finished
        else:
            to_move = 'X'  # Switch the turn back to the player (X)

    # Clear the screen and redraw UI elements
    SCREEN.fill(BG_COLOR)  # Fill the background with the default color
    if not selection_done:
        # Draw buttons for selecting X or O
        pygame.draw.rect(SCREEN, (0, 255, 0), (200, 400, 200, 100))  # Green button for X
        pygame.draw.rect(SCREEN, (0, 0, 255), (500, 400, 200, 100))  # Blue button for O
        x_text = SMALL_FONT.render("X", True, (0, 0, 0))  # Render text "X"
        o_text = SMALL_FONT.render("O", True, (0, 0, 0))  # Render text "O"
        SCREEN.blit(x_text, (280, 425))  # Position "X" text on the X button
        SCREEN.blit(o_text, (580, 425))  # Position "O" text on the O button
    else:
        # Draw the game grid and current board state
        draw_custom_grid()  # Draw the Tic Tac Toe grid
        render_board(board)  # Render the board with Xs and Os

        # If the game has finished, display the winner message
        if game_finished:
            display_message(winner_message)  # Show the winner or draw message
            pygame.display.update()  # Update the screen
            time.sleep(2)  # Wait for 2 seconds before resetting the game

            # Reset the game variables for a new game
            board = [[None, None, None], [None, None, None], [None, None, None]]  # Empty board
            to_move = None  # Reset the player turn
            game_finished = False  # Mark game as not finished
            winner_message = None  # Clear the winner message
            selection_done = False  # Reset the selection process

    pygame.display.update()  # Update the entire game screen

