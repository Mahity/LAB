import chess

def minimax(node, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or node.is_checkmate() or node.is_stalemate() or node.is_insufficient_material():
        return evaluate(node)

    if maximizingPlayer:
        maxEval = float('-inf')
        for move in node.legal_moves:
            node.push(move)
            eval = minimax(node, depth - 1, alpha, beta, False)
            node.pop()
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = float('inf')
        for move in node.legal_moves:
            node.push(move)
            eval = minimax(node, depth - 1, alpha, beta, True)
            node.pop()
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def evaluate(node):
    # This is a very basic evaluation function that favors moves which result in a higher number of pieces
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
    return sum(piece_values[piece.symbol().upper()] for piece in node.piece_map().values())

# Create a new chess board
board = chess.Board()

# Make some moves
board.push_san("e4")
board.push_san("e5")
board.push_san("f4")

# Call the minimax function
print(minimax(board, 2, float('-inf'), float('inf'), True))
