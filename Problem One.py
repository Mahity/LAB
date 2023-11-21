import os
import time
from tabulate import tabulate

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_board(board):
    clear_screen()
    print('---------')
    for i in range(3):
        for j in range(3):
            print('|', end='')
            print(board[i][j] if board[i][j] != ' ' else 3*i+j+1, end='|')
        print('\n---------')

def is_game_over(state):
    for i in range(3):
        if state[i][0] == state[i][1] == state[i][2] != ' ' or state[0][i] == state[1][i] == state[2][i] != ' ':
            return True
    if state[0][0] == state[1][1] == state[2][2] != ' ' or state[0][2] == state[1][1] == state[2][0] != ' ':
        return True
    if ' ' not in [state[i][j] for i in range(3) for j in range(3)]:
        return True
    return False

def score(state, ai_player):
    for i in range(3):
        if state[i][0] == state[i][1] == state[i][2] == ai_player or state[0][i] == state[1][i] == state[2][i] == ai_player:
            return 1
        elif state[i][0] == state[i][1] == state[i][2] != ' ' or state[0][i] == state[1][i] == state[2][i] != ' ':
            return -1
    if state[0][0] == state[1][1] == state[2][2] == ai_player or state[0][2] == state[1][1] == state[2][0] == ai_player:
        return 1
    elif state[0][0] == state[1][1] == state[2][2] != ' ' or state[0][2] == state[1][1] == state[2][0] != ' ':
        return -1
    return 0

def minimax(state, player, ai_player):
    if is_game_over(state):
        return score(state, ai_player), None, None

    if player == ai_player:
        value = -float('inf')
        for i in range(3):
            for j in range(3):
                if state[i][j] == ' ':
                    state[i][j] = player
                    new_value, _, _ = minimax(state, 'O' if player == 'X' else 'X', ai_player)
                    if new_value > value:
                        value, row, col = new_value, i, j
                    state[i][j] = ' '
        return value, row, col
    else:
        value = float('inf')
        for i in range(3):
            for j in range(3):
                if state[i][j] == ' ':
                    state[i][j] = player
                    new_value, _, _ = minimax(state, 'O' if player == 'X' else 'X', ai_player)
                    if new_value < value:
                        value, row, col = new_value, i, j
                    state[i][j] = ' '
        return value, row, col

def count_empty_spaces(board):
    return sum(row.count(' ') for row in board)

def tic_tac_toe():
    results = []  # Initialize an empty list to store the results
    game_count = 1  # Initialize a counter for the game number
    while True:  # Keep playing games until the user decides to quit
        clear_screen()  # Clear the screen
        ai_player = input("Choose your symbol (X/O): ").upper()
        while ai_player not in ['X', 'O']:
            print("Invalid input. Please enter 'X' or 'O'.")
            ai_player = input("Choose your symbol (X/O): ").upper()
        ai_player = 'O' if ai_player == 'X' else 'X'

        user_first = input("Do you want to go first? (yes/no): ").lower()
        while user_first not in ['yes', 'no']:
            print("Invalid input. Please enter 'yes' or 'no'.")
            user_first = input("Do you want to go first? (yes/no): ").lower()
        user_first = user_first == 'yes'

        board = [[' ']*3 for _ in range(3)]
        while not is_game_over(board):
            print_board(board)
            if (user_first and count_empty_spaces(board) % 2 != 0) or (not user_first and count_empty_spaces(board) % 2 == 0):
                move = input("Enter the number (1-9) for your move: ")
                while not move.isdigit() or int(move) < 1 or int(move) > 9 or board[(int(move)-1) // 3][(int(move)-1) % 3] != ' ':
                    print("Invalid move. Please try again.")
                    move = input("Enter the number (1-9) for your move: ")
                x, y = (int(move) - 1) // 3, (int(move) - 1) % 3
                board[x][y] = 'O' if ai_player == 'X' else 'X'
            else:
                _, x, y = minimax(board, ai_player, ai_player)
                board[x][y] = ai_player
                time.sleep(1)  # pause for a moment before clearing the screen

        print_board(board)
        result = score(board, ai_player)
        if result == 1:
            print('AI wins!')
            results.append(["Game " + str(game_count), "AI wins"])
        elif result == -1:
            print('You win!')
            results.append(["Game " + str(game_count), "You win"])
        else:
            print('Draw!')
            results.append(["Game " + str(game_count), "Draw"])

        # Print the results table
        print("\nResults so far:")
        print(tabulate(results, headers=["Game", "Result"], tablefmt="grid"))

        play_again = input('Do you want to play again? (y/n): ')
        if play_again.lower() != 'y':
            break  # End the loop and quit the game

        game_count += 1  # Increment the game counter for the next game

tic_tac_toe()
