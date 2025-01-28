# main.py
import pygame
from chromosome import genetic_algorithm
from board import ai_turn, button_clicked, draw_board, draw_button, generate_possible_moves, player_turn
from constants import BUTTON_HEIGHT, BUTTON_WIDTH, TILE_SIZE, BOARD_SIZE, FPS

# Main game function
import pygame
import sys
import time

from piece import Piece


def arrange_troops():
    RED = pygame.Color(255, 0, 0)  # Define the RED color constant

    background = pygame.image.load('bkg.png').convert()
    background = pygame.transform.scale(background, (BOARD_SIZE * TILE_SIZE, BOARD_SIZE * TILE_SIZE))

    screen = pygame.display.set_mode((BOARD_SIZE * TILE_SIZE, BOARD_SIZE * TILE_SIZE + BUTTON_HEIGHT + 10))
    pygame.display.set_caption('Troop Arrangement')
    
    # Initial game state with some pieces for the human player, arranged in a 2D list format
    human_pieces = [
        [Piece(2, "Human"), Piece(2, "Human"), Piece(2, "Human"), Piece(2, "Human"),
         Piece(2, "Human"), Piece(2, "Human"), Piece(3, "Human"), Piece(3, "Human")],
        [Piece(5, "Human"), Piece(6, "Human"), Piece(4, "Human"), Piece('4', "Human"),
         Piece(1, "Human"), Piece('F', "Human"), Piece('B', "Human"), Piece('B',"Human")],
    ] + [[None] * BOARD_SIZE for _ in range(BOARD_SIZE - 2)]

    dragged_piece = None
    drag_pos = None
    is_dragging = False
    running = True
    screen_width = BOARD_SIZE * TILE_SIZE
    screen_height = BOARD_SIZE * TILE_SIZE + BUTTON_HEIGHT + 10
    
    done_button_rect = pygame.Rect((screen_width * 3 // 4 - BUTTON_WIDTH // 2, screen_height - BUTTON_HEIGHT - 5, BUTTON_WIDTH, BUTTON_HEIGHT))

    while running:
        # First, fill the screen with the specified color
        screen.fill(pygame.Color(240,240,240))

        # Then, draw the background image on top of the colored screen
        screen.blit(background, (0, 0))

        # Draw the board and pieces
        font = pygame.font.Font(None, 36)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = human_pieces[row][col]
                if piece:
                    piece_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    piece_surface.set_alpha(200)  # Set transparency level (0-255)
                    piece_surface.fill(RED)  # Use the RED color constant
                    screen.blit(piece_surface, (col * TILE_SIZE, row * TILE_SIZE))

                    # Render and display the rank text
                    text_surface = font.render(str(piece.rank), True, pygame.Color("white"))
                    screen.blit(text_surface, (col * TILE_SIZE + 20, row * TILE_SIZE + 10))

        # Draw grid lines on top of the pieces
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                pygame.draw.rect(screen, pygame.Color(150,130,60),
                                 (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

        # Draw the dragged piece
        if dragged_piece:
            piece_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            piece_surface.set_alpha(150)
            piece_surface.fill(RED)  # Use the RED color constant
            screen.blit(piece_surface, drag_pos)
            text_surface = font.render(str(dragged_piece.rank), True, pygame.Color("white"))
            screen.blit(text_surface, (drag_pos[0] + 20, drag_pos[1] + 10))

        # Draw the bottom UI text and button
        font = pygame.font.Font(None, 30)
        text = "Position your Forces!"
        text_surface = font.render(text, True, pygame.Color("black"))
        text_x = screen_width // 4 - text_surface.get_width() // 2
        text_y = screen_height - BUTTON_HEIGHT - 10
        screen.blit(text_surface, (text_x, text_y + 10))
        draw_button(screen, "Onward", pygame.Color("gray"), pygame.Color("black"), done_button_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_clicked(done_button_rect):
                    running = False  # Exit the loop if "Done" is clicked
                else:
                    x, y = mouse_pos
                    col, row = x // TILE_SIZE, y // TILE_SIZE
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and human_pieces[row][col]:
                        dragged_piece = human_pieces[row][col]
                        human_pieces[row][col] = None
                        is_dragging = True
                        drag_pos = mouse_pos
            elif event.type == pygame.MOUSEMOTION and is_dragging:
                drag_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and is_dragging:
                x, y = pygame.mouse.get_pos()
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and human_pieces[row][col] is None:
                    human_pieces[row][col] = dragged_piece
                dragged_piece = None
                is_dragging = False

        pygame.display.flip()

    return human_pieces  # Return the final 2D board configuration

def play_screen():
    pygame.init()

    # Set the window size (use appropriate dimensions for your game)
    screen = pygame.display.set_mode((600, 400))  # Adjust size to fit your background image
    pygame.display.set_caption("Stratego Game")

    # Load background image for the play screen
    background_image = pygame.image.load('play5.png').convert()  # Replace with your image path
    background_image = pygame.transform.scale(background_image, (600, 400))  # Scale the background image

    # Set up the "Begin" button
    font = pygame.font.Font(None, 36)
    begin_button_text = font.render("Begin", True, (0, 0, 0))  # Black text for the Begin button
    begin_button_rect = begin_button_text.get_rect()  # Create a rect for text sizing

    # Create a grey background for the "Begin" button, with padding
    button_width = begin_button_rect.width + 40
    button_height = begin_button_rect.height + 20
    begin_button_bg = pygame.Surface((button_width, button_height))
    begin_button_bg.fill((240,240,240))  # Grey color for the button

    # Position the button at bottom-right corner, centered text
    button_x = 540 - button_width // 2
    button_y = 370 - button_height // 2
    begin_button_rect.center = (button_x + button_width // 2, button_y + button_height // 2)

    # Draw the background and button
    screen.blit(background_image, (0, 0))  # Blit the background image
    screen.blit(begin_button_bg, (button_x, button_y))  # Blit the grey background for the button
    screen.blit(begin_button_text, begin_button_rect)  # Center the text on the button

    pygame.display.flip()

# Main game function
def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE * TILE_SIZE, BOARD_SIZE * TILE_SIZE))
    pygame.display.set_caption("Stratego Game")
    clock = pygame.time.Clock()

    # Step 1: Show the Play Screen and wait for "Go" button click
    play_screen()  # Call play screen function

    # After the "Go" button is clicked, move to the arrange_troops screen
    board_ai = genetic_algorithm().board_config
    print("BOARD_AI\n")
    print(board_ai)
    
    # Use the arrange_troops function to arrange the human player's board
    board_human = arrange_troops()
    print("BOARD_HUMAN\n")
    print(board_human)
    
    # Merge the AI board (first two rows) with the human board (last two rows)
    board = board_ai[:6] + board_human[6:]
    
    print("Combined Board Setup:")
    print(board)
    print("\n\nTYPE :",board[2][1])
    
    player_turn_indicator = True  # True means it's the player's turn
    start_pos = None  # Initialize the starting position

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Player's turn logic
            if player_turn_indicator:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    selected_tile = (mouse_y // TILE_SIZE, mouse_x // TILE_SIZE)
                    piece = board[selected_tile[0]][selected_tile[1]]
                    if piece and piece.player == "Human":
                        start_pos = selected_tile  # Store the starting position
                        print(f"Selected piece: {piece.rank}")
                        possible_moves = generate_possible_moves(start_pos, board)
                        print(f"Possible moves: {possible_moves}")  # Print possible moves
                    elif start_pos and selected_tile != start_pos:
                        end_pos = selected_tile
                        player_turn(start_pos, end_pos, board)
                        player_turn_indicator = False  # Switch to AI's turn
                        start_pos = None  # Reset start position after move

        if not player_turn_indicator:  # AI's turn
            time.sleep(1)
            ai_turn(board)
            player_turn_indicator = True  # Switch back to player's turn

        screen.fill((240,240,240))
        
        # Draw the board, passing the combined board setup
        draw_board(screen, board)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
