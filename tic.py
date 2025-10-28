# Tic Tac Toe Game - 2 Player (Text-Based)
# Author: Jiya

def print_board(board):
    """Function to print the Tic Tac Toe board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(board, player):
    """Check if a player has won."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in win_conditions:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return " " not in board

def play_game():
    """Main function to play the Tic Tac Toe game."""
    board = [" "] * 9
    current_player = "X"
    print("Welcome to Tic Tac Toe!\n")
    print_board(board)

    while True:
        # Ask for player input
        try:
            move = int(input(f"Player {current_player}, choose your position (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid position! Choose a number between 1 and 9.")
                continue
            if board[move] != " ":
                print("That position is already taken! Try again.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        # Make the move
        board[move] = current_player
        print_board(board)

        # Check for win
        if check_winner(board, current_player):
            print(f"🎉 Player {current_player} wins! Congratulations!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw! 🤝")
            break

        # Switch player
        current_player = "O" if current_player == "X" else "X"

# Run the game
if __name__ == "__main__":
    play_game()
