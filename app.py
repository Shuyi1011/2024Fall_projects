from flask import Flask, jsonify, request, render_template
import random
from game import BlokusDuoAI

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')  # Ensure templates/index.html exists

@app.route('/favicon.ico')
def favicon():
    """Serve the favicon."""
    return app.send_static_file('favicon.ico')

# Initialize game state
game = BlokusDuoAI()
pieces = game.generate_pieces()
game_state = {
    "board": [[None for _ in range(14)] for _ in range(14)],
    "current_player": "Player 1",
    "pieces": pieces,  # Add full Blokus pieces here
}

# AI Player Logic
def random_ai(player):
    """Dumb AI: Randomly selects a piece and position."""
    valid_moves = []
    for piece_index, piece in enumerate(game_state["pieces"][player]):
        for row in range(14):
            for col in range(14):
                if is_valid_move(piece, (row, col)):
                    valid_moves.append((piece_index, (row, col)))
    return random.choice(valid_moves) if valid_moves else None

def heuristic_ai(player):
    """Wise AI: Selects the move that maximizes board coverage."""
    best_move = None
    best_score = -1
    for piece_index, piece in enumerate(game_state["pieces"][player]):
        for row in range(14):
            for col in range(14):
                if is_valid_move(piece, (row, col)):
                    # Simple heuristic: prioritize center area
                    score = (7 - abs(row - 7)) + (7 - abs(col - 7))
                    if score > best_score:
                        best_score = score
                        best_move = (piece_index, (row, col))
    return best_move

def is_valid_move(piece, position):
    """Validate if a move is legal on the board."""
    start_x, start_y = position
    for dx, dy in piece:
        x, y = start_x + dx, start_y + dy
        if not (0 <= x < 14 and 0 <= y < 14):  # Out of bounds
            return False
        if game_state["board"][x][y] is not None:  # Space occupied
            return False
    return True

def apply_move(player, piece_index, position):
    """Apply a move to the board."""
    piece = game_state["pieces"][player][piece_index]
    if is_valid_move(piece, position):
        start_x, start_y = position
        for dx, dy in piece:
            x, y = start_x + dx, start_y + dy
            game_state["board"][x][y] = 'P1' if player == "Player 1" else 'P2'
        game_state["pieces"][player].pop(piece_index)
        return True
    return False

@app.route('/api/get_board', methods=['GET'])
def get_board():
    """Return the current board state."""
    return jsonify(game_state)

@app.route('/api/make_move', methods=['POST'])
def make_move():
    """Handle a player's move or an AI move."""
    data = request.json
    player = game_state["current_player"]

    if player == "Player 1":  # Assume Player 1 is human
        piece_index = data['piece_index']
        position = tuple(data['position'])
    else:  # Assume Player 2 is AI
        move = heuristic_ai(player)
        if not move:
            return jsonify({"status": "error", "message": "AI has no valid moves"}), 400
        piece_index, position = move

    success = apply_move(player, piece_index, position)
    if success:
        # Switch to next player
        game_state["current_player"] = "Player 2" if player == "Player 1" else "Player 1"
        return jsonify({"status": "success", "board": game_state["board"]})
    else:
        return jsonify({"status": "error", "message": "Invalid move"}), 400

@app.route('/api/reset', methods=['POST'])
def reset_game():
    """Reset the game state."""
    global game_state
    game_state = {
        "board": [[None for _ in range(14)] for _ in range(14)],
        "current_player": "Player 1",
        "pieces": {},  # Add full Blokus pieces here
    }
    return jsonify({"status": "success", "message": "Game reset"})

if __name__ == '__main__':
    app.run(debug=True)