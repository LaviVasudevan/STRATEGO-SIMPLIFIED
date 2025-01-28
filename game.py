from board import display_game_over, find_best_move, generate_possible_moves, update_revealed_ranks
from piece import Piece

revealed_human_ranks = {}

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

