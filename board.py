# board.py
import pygame
from constants import BOARD_SIZE, TILE_SIZE, WHITE, RED, BLUE, BLACK


# Function to draw the board in the main game window
def draw_board(screen, board):
    print(board[3][0])  # Debugging: print the piece in row 3, column 0
    print(board[0][0])  # Debugging: print the piece in row 0, column 0
    pygame.display.set_caption('Game Play')
    # Load background image (assumed to be loaded during the Game class initialization)
    background = pygame.image.load('bkg.png').convert()
    background = pygame.transform.scale(background, (BOARD_SIZE * TILE_SIZE, BOARD_SIZE * TILE_SIZE))

    # Blit the background to the screen
    screen.blit(background, (0, 0))

    # Define the font once, outside the loop, for efficiency
    font = pygame.font.Font(None, 36)

    # Colors for grid lines and border
    GRID_COLOR = (150, 130, 60)  # Lighter brown for grid lines
    BORDER_COLOR = (150, 130, 60)  # Darker brown for the border

    # Dimensions for the board
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE

    # Draw the border outside the grid (thicker border)
    #border_thickness = 8
    #pygame.draw.rect(screen, BORDER_COLOR, (-border_thickness, -border_thickness, board_width + 2 * border_thickness, board_height + 2 * border_thickness), border_thickness)

    # Draw the grid and pieces
    for row in range(BOARD_SIZE):
        print("\n BOARD[ROW] = ", board[row])  # Debugging: print the row data
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            color = WHITE

            # Determine the color and text based on piece properties
            if piece:
                color = RED if piece.player == "Human" else BLUE
                # Show rank for revealed pieces or for unrevealed red pieces; hide for unrevealed blue pieces
                if piece.revealed or (piece.player == "Human" and not piece.revealed):
                    text = str(piece.rank)
                else:
                    text = "?"

                # Draw the rectangle for the piece
                piece_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                piece_surface.set_alpha(200)  # Set transparency level (0-255)
                piece_surface.fill(color)
                screen.blit(piece_surface, (col * TILE_SIZE, row * TILE_SIZE))

                # Render and display the piece text
                text_surface = font.render(text, True, WHITE if piece.revealed else BLACK)
                screen.blit(text_surface, (col * TILE_SIZE + 20, row * TILE_SIZE + 10))

            # Draw the grid line with lighter brown color
            pygame.draw.rect(screen, GRID_COLOR, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

            # Tooltip logic: Show rank info when hovering over a piece
            mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
            if piece and (piece.revealed or (piece.player == "Human" and not piece.revealed)):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if rect.collidepoint(mouse_pos):
                    # Show tooltip with rank on a white background
                    tooltip_text = f"Rank: {piece.rank}"
                    tooltip_surface = font.render(tooltip_text, True, BLACK)
                    tooltip_background = pygame.Surface((tooltip_surface.get_width() + 6, tooltip_surface.get_height() + 4))
                    tooltip_background.fill(WHITE)

                    # Position tooltip above or below piece
                    tooltip_x = col * TILE_SIZE + TILE_SIZE // 2
                    tooltip_y = row * TILE_SIZE - 25 if row > 0 else row * TILE_SIZE + TILE_SIZE + 10
                    tooltip_rect = tooltip_surface.get_rect(center=(tooltip_x, tooltip_y))

                    # Draw tooltip background and then text
                    screen.blit(tooltip_background, (tooltip_rect.x - 3, tooltip_rect.y - 2))
                    screen.blit(tooltip_surface, tooltip_rect)

    # Draw the "STRATEGO" text at the bottom of the board (centered)
    text_surface = font.render("STRATEGO", True, pygame.Color("black"))
    screen.blit(text_surface, ((BOARD_SIZE * TILE_SIZE) // 2 - text_surface.get_width() // 2,
                               BOARD_SIZE * TILE_SIZE + 10))

    # Update the display after drawing everything
    pygame.display.flip()

# board.py
import sys
import pygame
from constants import BOARD_SIZE, BUTTON_HEIGHT, BUTTON_WIDTH, TILE_SIZE, WHITE, RED, BLUE, BLACK
from piece import Piece

def is_within_bounds(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def generate_possible_moves(piece_position, board):
    x, y = piece_position
    moves = []
    piece = board[x][y]

    # Check if the piece is movable
    if not piece.is_movable:
        return moves  # Return empty moves if the piece is immovable

    # Movement offsets: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    if piece.player == "Human":
        # Red pieces (player) can move to rows 0-4 (decreasing row count)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check for moving up (decreasing row count)
            if dx == -1 and is_within_bounds(nx, ny):
                if board[nx][ny] is None or board[nx][ny].player != piece.player:
                    moves.append((nx, ny))

            # Check for lateral movement (left/right)
            elif dx == 0 and is_within_bounds(nx, ny):
                if board[nx][ny] is None or board[nx][ny].player != piece.player:
                    moves.append((nx, ny))

    else:
        # Blue pieces (AI) can move to rows 5-7 (increasing row count)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check for moving down (increasing row count)
            if dx == 1 and is_within_bounds(nx, ny):
                if board[nx][ny] is None or board[nx][ny].player != piece.player:
                    moves.append((nx, ny))

            # Check for lateral movement (left/right)
            elif dx == 0 and is_within_bounds(nx, ny):
                if board[nx][ny] is None or board[nx][ny].player != piece.player:
                    moves.append((nx, ny))

    return moves

def player_move(start, end, board):
    attacker = board[start[0]][start[1]]
    defender = board[end[0]][end[1]]
    
    if defender and defender.player != attacker.player:
        print(f"Attack! {attacker.rank} attacks {defender.rank}")
        winner = resolve_attack(attacker, defender)
        print(winner)
        if winner:
            if winner == attacker:
                # The attacker wins
                board[end[0]][end[1]] = winner  # Move the winning attacker to the defender's position
                print(f"{winner.rank} wins the battle! {winner.rank} revealed!")
                board[start[0]][start[1]] = None  # Clear the attacker's original position
            else:
                # The defender wins
                board[end[0]][end[1]] = defender  # Defender remains in place
                board[start[0]][start[1]] = None  # Remove the attacker from the board
                print(f"{defender.rank} wins the battle! {defender.rank} remains in position.")

            if winner.player == "Human":
                update_revealed_ranks(winner,end) 
                print("Revealed Human Pieces :")
            
        else:
            print("received none now removing")
            # Both pieces are eliminated in case of a tie
            board[start[0]][start[1]] = None  # Clear the attacker's position
            board[end[0]][end[1]] = None  # Clear the defender's position
            print("Both pieces are eliminated!")
            
    else:
        # Move the piece to an empty cell if there's no attack
        board[end[0]][end[1]] = attacker  

    # Clear the start position only if it's a valid move or an attack where no battle occurs
    if defender is None:
        board[start[0]][start[1]] = None  
    
    if attacker.player == "Human" and attacker.rank in revealed_human_ranks:
        update_revealed_ranks(attacker, end)
 

def ai_turn(board):
    best_move = find_best_move(board)
    if best_move:
        (start, end) = best_move
        attacker = board[start[0]][start[1]]
        defender = board[end[0]][end[1]]
        
        if defender and defender.player != attacker.player:
            print(f"AI Attack! {attacker.rank} attacks {defender.rank}")
            winner = resolve_attack(attacker, defender)
             
            if winner:
                if winner == attacker:
                    # The attacker wins
                    board[end[0]][end[1]] = winner  # Move the winning attacker to the defender's position
                    print(f"{winner.rank} wins the battle! {winner.rank} revealed!")
                    board[start[0]][start[1]] = None  # Clear the attacker's original position
                else:
                    # The defender wins
                    board[end[0]][end[1]] = defender  # Defender remains in place
                    board[start[0]][start[1]] = None  # Remove the attacker from the board
                    print(f"{defender.rank} wins the battle! {defender.rank} remains in position.")
            
                if winner.player == "Human":
                    update_revealed_ranks(winner, end) 
                    print("Revealed Human Pieces :")
            else:
                print("received none now removing")
                # Both pieces are eliminated in case of a tie
                board[start[0]][start[1]] = None  # Clear the attacker's position
                board[end[0]][end[1]] = None  # Clear the defender's position
                print("Both pieces are eliminated!")

        else:
            board[end[0]][end[1]] = attacker  # Move the piece to an empty cell
        
        board[start[0]][start[1]] = None  # Clear the start position



def display_game_over(winner):
    pygame.init()

    # Load background images
    image1 = pygame.image.load('redwin.png').convert()  # Background when AI wins
    image2 = pygame.image.load('bluewin.png').convert()  # Background when Human wins

    # Set the window size based on your desired dimensions or the image size
    screen = pygame.display.set_mode((600, 400))  # Adjust the window size here
    pygame.display.set_caption("Game Over")

    # Choose the background based on the winner
    if winner == "AI":
        background = pygame.transform.scale(image2, (600, 400))  # Adjust size as needed
    else:
        background = pygame.transform.scale(image1, (600, 400))  # Adjust size as needed

    # Font and text setup
    font = pygame.font.Font(None, 36)
    exit_button_text = font.render("Exit", True, (0, 0, 0))  # Black text for exit button
    exit_button_rect = exit_button_text.get_rect(topright=(570, 10))  # Position the exit button at the top right

    # Create a grey background for the exit button
    exit_button_bg = pygame.Surface((exit_button_rect.width + 10, exit_button_rect.height + 10))
    exit_button_bg.fill((169, 169, 169))  # Grey color

    # Draw the background and text on the screen
    screen.blit(background, (0, 0))  # Blit the background image
    screen.blit(exit_button_bg, exit_button_rect.topleft)  # Blit the grey background for the exit button
    screen.blit(exit_button_text, exit_button_rect)  # Blit the exit button text

    pygame.display.flip()

    # Event handling loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):  # Check if the Exit button is clicked
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

revealed_human_ranks = {}

def update_revealed_ranks(piece, piece_position):
    """ Update knowledge of revealed ranks if an AI piece successfully attacks a human piece. """
    if piece and piece.player == "Human":
        # Record the revealed rank of the human piece
        revealed_human_ranks[piece.rank] = piece_position


def resolve_attack(attacker, defender):
    # Flag capture scenario
    if defender.rank == "F":
        print(f"{attacker.player}'s {attacker.rank} captures the Flag! Game over.")
        display_game_over(attacker.player)
        return attacker  # Game over, return attacker as the winner

    # Reveal ranks for visibility
    attacker.revealed = True
    defender.revealed = True

        # Bomb vs. Miner scenario
    if defender.rank == "B":
        if attacker.rank == 3:  # Miner rank
            print("Miner defuses the Bomb!")
            return attacker  # Miner wins and defuses the bomb
        else:
            print(f"{attacker.player}'s {attacker.rank} hits the Bomb and is removed.")
            return defender  # Bomb wins; attacker is removed

    # Spy vs. General scenario
    if attacker.rank == 1 and defender.rank == 6:  # Spy and General ranks
        print("Spy uses charm to defeat the General!")
        return attacker  # Spy wins against General

    # Standard rank comparison for other cases
    if isinstance(attacker.rank, int) and isinstance(defender.rank, int):
        if attacker.rank < defender.rank:
            print(f"{attacker.player}'s {attacker.rank} is defeated by {defender.player}'s {defender.rank}.")
            return defender  # Defender wins
        elif attacker.rank > defender.rank:
            print(f"{attacker.player}'s {attacker.rank} defeats {defender.player}'s {defender.rank}.")
            return attacker  # Attacker wins
        else:
            print(f"Both {attacker.rank} and {defender.rank} are eliminated in a tie.")
            print("returning none")
            return None  # Both pieces are removed

    # Invalid case fallback
    print("Invalid attack scenario.")
    return None

def player_turn(start, end, board):
    piece = board[start[0]][start[1]]
    if piece and (end in generate_possible_moves(start, board)):
        player_move(start, end, board)
    else:
        print("Invalid move. Try again.")

revealed_human_ranks = {}

def get_adjacent_positions(position):
    """Returns valid adjacent board positions to the given location."""
    x, y = position
    # Generate adjacent positions and filter those within board boundaries
    return [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if is_within_bounds(x + dx, y + dy)]

def is_near_flag_zone(position):
    """Determines if the given position is near the opponent's flag zone."""
    # Assuming opponent's flag zone is in rows 0-2; adjust if needed
    return 0 <= position[0] <= 2

def is_in_vulnerable_position(board,position):
    x, y = position
    # Here, we define a "vulnerable position" as one that is near an enemy piece or close to an unknown piece.
    # This is for situations where we want to intentionally expose weaker pieces like spies or scouts.
    
    enemy_player = "Human"  # AI is playing against the human
    
    # Check if the position is next to an enemy piece (adjacent squares)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip the current position
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]):  # Check if within board bounds
                piece = board[nx][ny]
                if piece and piece.player == enemy_player:  # If there's an enemy piece here
                    return True
    return False

def is_near_enemy_troops(board,position):
    x, y = position
    enemy_player = "Human"  # AI is playing against the human
    
    # Check the 8 adjacent positions (up, down, left, right, and diagonals)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip the current position
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]):  # Check if within board bounds
                piece = board[nx][ny]
                if piece and piece.player == enemy_player:  # If there's an enemy piece here
                    return True
    return False

def evaluate_move(move, piece, board, start_position):
    x, y = move  # Unpack the end position (potential move)
    target_piece = board[x][y] if board[x][y] else None  # Get target piece if it exists
    
    score = 0

    # 1. Aggressive Behavior for Rank 4/5 Pieces (Strong pieces)
    if piece.rank in [4, 5]:  # Stronger pieces like Major (4) or General (5)
        if target_piece:  # If there's a target piece
            if target_piece.player == "Human":  # Target enemy pieces
                score += 90  # Neutral but still a valid move
                
        # Encourage strong pieces to move into enemy territory
        if x > start_position[0]:  # Moving towards the enemy flag zone
            score += 50  # Big reward for advancing aggressively
        elif x == start_position[0]:  # Same row, penalize lateral movement
            score -= 10

    # 2. Spy vs. Marshall Strategy (Keep the spy cautious)
    if piece.rank == 1:  # Spy
        if target_piece and target_piece.player == "Human" and target_piece.rank == 6:  # Target is Marshall
            score += 50  # Prioritize moves that target the Marshall
        else:
            score -= 10  # Discourage risky moves for the Spy

    # 3. Miner vs. Bomb Strategy
    elif piece.rank == 3:  # Miner
        if target_piece and target_piece.player == "Human" and (target_piece.rank == "B" or is_near_flag_zone(move)):
            score += 70  # Miners targeting bombs get a higher score
        elif is_near_flag_zone(move):
            score += 30  # Encourage Miners to explore potential flag zones near bombs

    # 4. Bomb and Flag-Proximity Heuristic
    if target_piece and target_piece.rank == "B":
        score += 20  # Assume potential Flag nearby if Bomb found
        for adj in get_adjacent_positions(move):
            if is_within_bounds(x, y):
                adj_piece = board[adj[0]][adj[1]]
                if not adj_piece or adj_piece.player == "AI":
                    score += 40  # Reward moves that close in around Bomb locations

    # 5. Handling Known and Unknown Human Ranks
    if target_piece and target_piece.player == "Human":
        # Check if the target piece's position is in the revealed dictionary
        for human_rank, pos in revealed_human_ranks.items():
            if pos == move:  # If the position of the target piece is revealed
                comparison_result = piece.compare(target_piece)
                if comparison_result > 0:
                    score += 70  # Favor moves where AI has a higher rank
                elif comparison_result < 0:
                    score -= 50  # Discourage moves where AI is at a disadvantage
                else:
                    score += 45  # Neutral for same-rank encounters
                break
        else:  # If the position is not revealed
            if piece.rank in [2, 3, 6]:
                score += 70  # Prefer using lower-ranked pieces for scouting
            elif piece.rank in [5, 4]:
                score -= 10  # Avoid sending the General into uncertain attacks
            else:
                score += 30  # Moderate risk if it's neither high nor low rank
            if is_near_flag_zone(move):
                score += 10  # Take risk if near enemy's flag zone
            elif is_near_flag_zone(start_position):
                score -= 10  # Avoid risky moves near own flag zone

    # 6. Penalize Risk for Revealed Pieces
    if piece.revealed:
        score -= 10  # Reduce score for revealed pieces in risky moves

    # 7. Encourage Exploratory Moves for Specific Pieces
    if piece.rank in [2, 3, 6] and is_near_enemy_troops(board, start_position):
        score += 100  # Encourage scouts and miners to explore enemy territory
    elif piece.rank in [5, 4] and is_near_enemy_troops(board, start_position):
        score -= 20  # Avoid sending higher-ranked pieces too far ahead unless necessary

    # 8. Favor Vulnerable Pieces in the Opponent's Weak Zones
    if piece.rank in [1, 2, 3] and is_in_vulnerable_position(board, move):
        score += 70  # Allow pieces in weak positions to explore opponent's vulnerable zones

    # 9. High Priority for Left/Right Movements in Rows 6/7 (Exploration in Enemy Territory)
    if start_position[0] in [7]:  # If the piece is in rows 6/7, enemy territory
        if move[1] != start_position[1]:  # If there is a left/right movement
            score += 100  # Give a big reward for moving left or right in enemy territory
        else:
            score -= 5  # Penalize vertical movements in enemy territory
    else:
        # 5. Prefer Moves Toward the Opponent’s Flag Zone
        if x > start_position[0]:  # Moving up towards the human flag zone
            score += 70  # Reward for advancing
        elif x == start_position[0]:  # Same row
            score -= 20  # Penalize left-right moves
    return score


def find_best_move(board):
    best_move = None
    max_score = float('-inf')
    
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            piece = board[i][j]
            if piece and piece.player == "AI":
                possible_moves = generate_possible_moves((i, j), board)
                
                for move in possible_moves:
                    # Call evaluate_move with the starting position and the piece
                    score = evaluate_move(move, piece, board, (i, j))
                    
                    if score > max_score:
                        max_score = score
                        best_move = ((i, j), move)
    
    return best_move


def animate_move(start, end, piece, board):
    board[start[0]][start[1]] = None
    board[end[0]][end[1]] = piece
    piece.move_history.append(start)
    if len(piece.move_history) > 5:
        piece.move_history.pop(0)


# Draw button with hover effect
def draw_button(screen, text, color, hover_color, rect):
    font = pygame.font.Font(None, 30)
    mouse_pos = pygame.mouse.get_pos()
    button_color = hover_color if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, button_color, rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Check if the button is clicked
def button_clicked(rect):
    return rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
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

    # Event handling loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click was inside the "Begin" button area
                if pygame.Rect(button_x, button_y, button_width, button_height).collidepoint(event.pos):
                    return  # Proceed to the arrange_troops screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Allow quitting with ESC key
                    pygame.quit()
                    sys.exit()
