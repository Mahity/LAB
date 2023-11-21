import chess

def get_human_move(board, moves, move_num):
    while True:
        move_str = moves[move_num]

        try:
            move = board.parse_san(move_str)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please enter a valid move in standard chess notation (e.g., e2e4).")
            continue

        if move not in board.legal_moves:
            print("Invalid move. Please enter a legal move for the current position.")
            continue

        return move, move_num + 1
    
def evaluate(board, maximizingPlayer):
    # Piece values in chess
    piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}

    # Calculate material advantage
    material_advantage = 0
    for piece in board.piece_map().values():
        # Use the piece's piece_type as a key to get its value from the piece_values dictionary
        piece_value = piece_values.get(piece.piece_type, 0)
        if piece.color == maximizingPlayer:
            material_advantage += piece_value
        else:
            material_advantage -= piece_value
    KEY_SQUARES = [chess.E4, chess.D4, chess.E5, chess.D5]
    # Evaluate control of key squares
    control_score = 0
    for square in KEY_SQUARES:
        if board.piece_at(square) and board.piece_at(square).color == maximizingPlayer:
            control_score += 1

    # Evaluate piece development
    development_score = 0
    for piece in board.piece_map().values():
        if piece.color == maximizingPlayer:
            development_score += piece.piece_type.value * piece.square.rank

    # Combine the factors into a final score
    score = material_advantage + control_score + development_score

    return score

def minimax(board, depth, maximizingPlayer, alpha, beta):
    if depth == 0 or board.is_game_over():
        return evaluate(board, maximizingPlayer), None

    best_move = None
    if maximizingPlayer:
        best_value = -float('inf')
        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push(move)
            new_value, _ = minimax(new_board, depth - 1, False, alpha, beta)
            if new_value > best_value:
                best_value = new_value
                best_move = move
            alpha = max(alpha, new_value)

            # Prune if alpha exceeds beta
            if beta <= alpha:
                break

        return best_value, best_move

    else:
        best_value = float('inf')
        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push(move)
            new_value, _ = minimax(new_board, depth - 1, True, alpha, beta)
            if new_value < best_value:
                best_value = new_value
                best_move = move
            beta = min(beta, new_value)

            # Prune if alpha exceeds beta
            if alpha >= beta:
                break

        return best_value, best_move


def play_game(moves):
    board = chess.Board()
    current_player = chess.WHITE
    move_num = 0

    while not board.is_game_over():
        print(board)
        if current_player:
            move, move_num = get_human_move(board, moves, move_num)
        else:
            _, move = minimax(board, 3, True, -float('inf'), float('inf'))
        board.push(move)
        current_player = not current_player  # Switch turns

    print(board)
    if board.is_checkmate():
        winner = 'White' if current_player else 'Black'
        print(f"Checkmate! {winner} wins!")
    elif board.is_stalemate() or board.is_insufficient_material():
        print("Draw due to stalemate or insufficient material.")
    else:
        print("Resignation!")

if __name__ == "__main__":
    # Define a list of moves
    moves = ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'g8f6', 'e1g1', 'f8d6', 'c2c3', 'e8g8']  
    play_game(moves)
