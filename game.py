import random
import copy
import math

class BlokusDuoAI:
    def __init__(self):
        self.board_size = 14
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.pieces = self.generate_pieces()
        self.start_positions = {'Player 1': (0, 0), 'Player 2': (13, 13)}
        self.players = ['Player 1', 'Player 2']
        self.current_player = self.players[0]
        self.placed_pieces = {'Player 1': [], 'Player 2': []}
        self.maximizing_player = 'Player 1'
        self.valid_pos = self.initial_valid_pos()
    
    def generate_full_blokus_pieces(self):
        """Generate the complete set of Blokus Duo pieces."""
        pieces = [
            # 1-square piece
            [(0, 0)],

            # 2-square pieces
            [(0, 0), (1, 0)],

            # 3-square pieces
            [(0, 0), (1, 0), (2, 0)],  # Line
            [(0, 0), (1, 0), (1, 1)],  # L-shape

            # 4-square pieces
            [(0, 0), (1, 0), (2, 0), (3, 0)],  # Line
            [(0, 0), (0, 1), (0, 2), (1, 2)],  # L-shape
            [(0, 0), (0, 1), (1, 0), (1, 1)],  # Square
            [(0, 0), (1, 0), (1, 1), (1, 2)],  # Zigzag
            [(0, 0), (0, 1), (0, 2), (1, 1)],

            # 5-square pieces
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],  # Long line
            [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)],  # L-shape
            [(0, 0), (1, 0), (1, 1), (2, 0), (3, 0)],  # T-shape
            [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)],  # reverse_L
            [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],  # Stair_shape
            [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],  # Cross
            [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)],  # Stack-shape
            [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)],
            [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
            [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]
        ]
        return pieces

    def rotate_piece(self, piece):
        """Generate all unique rotations of a piece."""
        rotations = set()
        current = piece
        for _ in range(4):  # 0°, 90°, 180°, 270°
            # (x, y) -> (y, -x)
            current = [(y, -x) for x, y in current]
            # Normalize the piece to start from the origin
            min_x = min(x for x, y in current)
            min_y = min(y for x, y in current)
            normalized = [(x - min_x, y - min_y) for x, y in current]
            rotations.add(tuple(normalized)) 
        return [list(r) for r in rotations]  
    
    def generate_pieces(self):
        """Generate full Blokus Duo pieces for each player."""
        return {
            "Player 1": self.generate_full_blokus_pieces(),
            "Player 2": self.generate_full_blokus_pieces(),
        }

    def display_board(self):
        """Print the current board."""
        for row in self.board:
            print(' '.join(['.' if cell is None else cell[0] for cell in row]))

    def is_valid_move(self, player, piece, position):
        start_x, start_y = position
        # print(f"Checking move for {player}: Piece {piece} at {position}")
        has_corner_contact = False
        current_player = "X" if player == "Player 1" else "O"


        for dx, dy in piece:
            x, y = start_x + dx, start_y + dy

            # check if the piece is out of bounds
            if not (0 <= x < self.board_size and 0 <= y < self.board_size):
                return False

            # check if the piece overlaps with existing pieces
            if self.board[x][y] is not None:
                return False

            # check if the piece has corner contact with existing pieces
            if not self.placed_pieces[player]:  # First piece
                if (x, y) == self.start_positions[player]:
                    has_corner_contact = True
            else:
                for nx, ny in [(x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if self.board[nx][ny] == current_player:
                            has_corner_contact = True

                for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if self.board[nx][ny] == current_player:
                            return False


        return has_corner_contact
        # return True

    def place_piece(self, player, piece_index, rotated_piece, position):
        """Try to place a piece, checking all rotations."""
        # piece = self.pieces[player][piece_index]
        piece = rotated_piece
        print(f"Placing piece {piece} for {player} at {position}")
        start_x, start_y = position
        for dx, dy in piece:
            x, y = start_x + dx, start_y + dy
            self.board[x][y] = "X" if player == "Player 1" else "O"
        self.update_valid_pos(piece, position, self.valid_pos)
        self.placed_pieces[player].append(piece)
        self.pieces[player].pop(piece_index)  # Remove used piece
        return True
    
    def switch_player(self):
        """Switch to the next player."""
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def random_ai(self, player):
        """Dumb AI: Randomly selects a piece, rotation, and position."""
        valid_moves = []
        for piece_index, piece in enumerate(self.pieces[player]):
            for row in range(self.board_size):
                for col in range(self.board_size):
                    for rotated_piece in self.rotate_piece(piece):
                        if self.is_valid_move(player, rotated_piece, (row, col)):
                            valid_moves.append((piece_index, (row, col), rotated_piece))
        if valid_moves:
            return random.choice(valid_moves) 
        print(f"Valid moves for {player}: {valid_moves}") 
        return None  

    def heuristic_ai(self, player):
        """Wise AI: Selects the move that maximizes board coverage."""
        best_move = None
        best_score = -1
        for piece_index, piece in enumerate(self.pieces[player]):
            ro_pieces = self.rotate_piece(piece)
            for ro_piece in ro_pieces:
                for pos in self.valid_pos:
                        if self.is_valid_move(player, ro_piece, pos):
                            # Heuristic: Maximize placement options for the next turn
                            pieces_copy = {player: self.pieces[player][:] for player in self.pieces}
                            pieces_copy[player].pop(piece_index)
                            placed_pieces_copy = {player: self.placed_pieces[player][:] for player in self.placed_pieces}
                            placed_pieces_copy[player].append(piece)
                            valid_pos_copy = self.valid_pos[:]
                            self.update_valid_pos(piece, pos, valid_pos_copy)
                            score = self.evaluate_board_after_move(player, ro_piece, pos, pieces_copy, placed_pieces_copy, valid_pos_copy)
                            if score > best_score:
                                best_score = score
                                best_move = (piece_index, pos, ro_piece)
        return best_move

    def evaluate_board_after_move(self, player, piece, position, pieces, placed_pieces_copy, valid_pos_copy):
        """Evaluate board based on the number of valid moves after placing a piece."""
        # Simplified heuristic: Favor moves that maximize valid positions
        temp_board = [row[:] for row in self.board]
        start_x, start_y = position
        for dx, dy in piece:
            x, y = start_x + dx, start_y + dy
            temp_board[x][y] = "X" if player == "Player 1" else "O"


        valid_positions = 0
        for piece in pieces[player]:
            rotated_pieces = self.rotate_piece(piece)
            for rotated_piece in rotated_pieces:
                placed_pieces_copy[player].append(piece)

                for pos in valid_pos_copy:

                        if self.is_valid_move_sim(player, rotated_piece, pos, temp_board, placed_pieces_copy):
                            valid_positions += 1
        return valid_positions
    
    def calculate_score(self, player):
        """
        Calculate the score for a player based on unplaced pieces.
        Each square in an unplaced piece contributes 1 point.
        Lower scores are better.
        """
        remaining_squares = 0
        for piece in self.pieces[player]:
            remaining_squares += len(piece)  # Each square in a piece adds 1 to the score
        # if remaining_squares == 0:  # All pieces placed
        #     return -5
        return remaining_squares

    def display_scores(self):
        """
        Display the scores for both players at the end of the game.
        """
        print("\nGame Over! Final Scores:")
        scores = {player: self.calculate_score(player) for player in self.players}
        for player, score in scores.items():
            print(f"{player}: {score} points")
        if scores["Player 1"] == scores["Player 2"]:
            print("It's a tie!")
        else:
            winner = min(scores, key=scores.get)  # Player with the lowest score wins
            print(f"Winner: {winner}!")

    def initial_valid_pos(self):
        valid_positions = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                valid_positions.append((row, col))
        return valid_positions

    def update_valid_pos(self, piece, position, valid_positions):
        start_x, start_y = position
        for dx, dy in piece:
            x, y = start_x + dx, start_y + dy
            if (x, y) in valid_positions:
                valid_positions.remove((x, y))


    def minimax_ai(self, player, depth=2):
        """
        Choose a move using minimax search.

        depth: how many plies deep to search
        """
        best_move = None
        # If we are the current player, we want to maximize our advantage.
        maximizing_player = True if player == self.maximizing_player else False

        valid_positions = self.valid_pos[:]

        alpha = -math.inf
        beta = math.inf

        best_score = -math.inf if maximizing_player else math.inf

        for piece_index, piece in enumerate(self.pieces[player]):
            rotated_pieces = self.rotate_piece(piece)
            for ro_piece in rotated_pieces:
                for pos in valid_positions:
                    if self.is_valid_move(player, ro_piece, pos):
                        # Simulate move
                        score = self.simulate_and_minimax(player, piece_index, ro_piece, pos, depth, alpha,
                                                          beta, maximizing_player, valid_positions)

                        if maximizing_player:
                            if score > best_score:
                                best_score = score
                                best_move = (piece_index, pos, ro_piece)
                                alpha = max(alpha, best_score)
                        else:
                            # If we were minimizing, but since typically minimax is from the perspective of the current player,
                            # this code assumes "player" is always the perspective of the AI.
                            # If you want player 2 to be minimizing, adjust logic accordingly.
                            # Typically, we consider the AI as always maximizing from its perspective.
                            # For a truly symmetrical minimax, you'd determine "maximizing_player" based on player identity.
                            if score < best_score:
                                best_score = score
                                best_move = (piece_index, pos, ro_piece)
                                beta = min(beta, best_score)

                            # Alpha-Beta Pruning
                            if beta <= alpha:
                                break
                if beta <= alpha:
                    break
            if beta <= alpha:
                break

        return best_move

    def simulate_and_minimax(self, player, piece_index, piece, position, depth, alpha, beta, maximizing_player, valid_positions):
        """
        Place the piece, switch player, and call minimax recursively.
        Returns the evaluated score of this position.
        """
        # Create a deep copy of the game state
        board_copy = [row[:] for row in self.board]
        pieces_copy = {player: self.pieces[player][:] for player in self.pieces}
        placed_pieces_copy = {player: self.placed_pieces[player][:] for player in self.placed_pieces}
        current_player_copy = player
        valid_pos_copy = valid_positions[:]

        # Execute the move on the copied state
        start_x, start_y = position
        current_player_marker = "X" if player == "Player 1" else "O"
        for dx, dy in piece:
            x, y = start_x + dx, start_y + dy
            board_copy[x][y] = current_player_marker

        placed_pieces_copy[player].append(piece)
        pieces_copy[player].pop(piece_index)  # remove used piece
        self.update_valid_pos(piece, position, valid_pos_copy)

        # Evaluate board now or check if game ends / no moves
        if depth == 0:
            # Terminal node or depth limit reached - static evaluation
            return self.static_evaluation(board_copy, pieces_copy)

        # Switch player
        next_player = self.players[1] if player == self.players[0] else self.players[0]

        # Check if next player has moves
        next_moves = self.get_all_moves(next_player, board_copy, pieces_copy, placed_pieces_copy, valid_pos_copy)
        if not next_moves:
            # If next player cannot move, maybe the current player gets another turn or game ends
            # Check if current player can also not move
            current_moves = self.get_all_moves(player, board_copy, pieces_copy, placed_pieces_copy, valid_pos_copy)
            if not current_moves:
                # Both cannot move: Game ends, evaluate final score
                return self.static_evaluation(board_copy, pieces_copy)
            else:
                # Next player passes, same player continues
                # This scenario is complex, but let's say if opponent passes, we call minimax again for the same player, reducing depth.
                return self.minimax_search(player, depth - 1, board_copy, pieces_copy, placed_pieces_copy, alpha, beta,
                                           maximizing_player, valid_pos_copy)
        else:
            # Normal turn for next player
            return self.minimax_search(next_player, depth - 1, board_copy, pieces_copy, placed_pieces_copy, alpha, beta,
                                       not maximizing_player, valid_pos_copy)

    def minimax_search(self, player, depth, board, pieces, placed_pieces, alpha, beta, maximizing_player, valid_positions):
        """
        The recursive minimax function that explores possible moves for `player`.
        """

        if depth == 0:
            return self.static_evaluation(board, pieces)

        valid_pos_copy = valid_positions[:]
        moves = self.get_all_moves(player, board, pieces, placed_pieces, valid_pos_copy)
        if not moves:
            # Player passes turn
            # Check if other player also can't move
            valid_pos_copy = valid_positions[:]
            other_player = self.players[1] if player == self.players[0] else self.players[0]
            other_moves = self.get_all_moves(other_player, board, pieces, placed_pieces, valid_pos_copy)
            if not other_moves:
                # Game over
                return self.static_evaluation(board, pieces)
            else:
                # Opponent gets next turn
                return self.minimax_search(other_player, depth - 1, board, pieces, placed_pieces, alpha, beta,
                                           not maximizing_player, valid_pos_copy)

        best_score = -math.inf if maximizing_player else math.inf

        for (p_index, pos, p_piece) in moves:
            # Simulate move
            board_copy = [r[:] for r in board]
            pieces_copy = {player: pieces[player][:] for player in pieces}
            placed_pieces_copy = {player: placed_pieces[player][:] for player in placed_pieces}
            valid_pos_copy = valid_positions[:]

            start_x, start_y = pos
            current_player_marker = "X" if player == "Player 1" else "O"
            for dx, dy in p_piece:
                x, y = start_x + dx, start_y + dy
                board_copy[x][y] = current_player_marker

            placed_pieces_copy[player].append(p_piece)
            pieces_copy[player].pop(p_index)
            self.update_valid_pos(p_piece, pos, valid_pos_copy)

            next_player = self.players[1] if player == self.players[0] else self.players[0]

            score = self.minimax_search(next_player, depth - 1, board_copy, pieces_copy, placed_pieces_copy, alpha,
                                        beta, not maximizing_player, valid_pos_copy)

            if maximizing_player:
                if score > best_score:
                    best_score = score
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                beta = min(beta, best_score)

            if beta <= alpha:
                break

        return best_score

    def get_all_moves(self, player, board, pieces, placed_pieces, valid_positions):
        """
        Generate all possible moves for `player` given the current board and piece set.
        Returns a list of tuples (piece_index, position, rotated_piece).
        """
        valid_moves = []
        for piece_index, piece in enumerate(pieces[player]):
            rotated_pieces = self.rotate_piece(piece)
            for ro_piece in rotated_pieces:
                for pos in valid_positions:
                        if self.is_valid_move_sim(player, ro_piece, pos, board, placed_pieces):
                            valid_moves.append((piece_index, pos, ro_piece))
        return valid_moves

    def is_valid_move_sim(self, player, piece, position, board, placed_pieces):
        """
        A version of is_valid_move that doesn't rely on self.placed_pieces, but uses a passed placed_pieces dictionary.
        This is needed since we are simulating states.
        """
        start_x, start_y = position
        current_player_marker = "X" if player == "Player 1" else "O"
        player_has_placed = len(placed_pieces[player]) > 0

        has_corner_contact = False
        for dx, dy in piece:
            x, y = start_x + dx, start_y + dy

            # Out of bounds
            if not (0 <= x < self.board_size and 0 <= y < self.board_size):
                return False

            # Overlap
            if board[x][y] is not None:
                return False

            # Corner contact rules:
            if not player_has_placed:
                # first piece must be placed at start position
                if (x, y) == self.start_positions[player]:
                    has_corner_contact = True
            else:
                # Already placed pieces, need corner contact with player's marker
                # Check corners
                for nx, ny in [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if board[nx][ny] == current_player_marker:
                            has_corner_contact = True

                # Check edges (should not share edge)
                for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if board[nx][ny] == current_player_marker:
                            return False

        return has_corner_contact

    def static_evaluation(self, board, pieces):
        """
        Compute a heuristic score of the board state.
        Lower score for the opponent, higher for the current player.
        For simplicity, let's say we score as:
        (Opponent's score - Current player's score)
        or some heuristic that you define.

        A simple approach:
        Score = (Count moves for Player 1) - (Count moves for Player 2)
        or use calculate_score difference.

        Here, we just do difference in remaining piece squares:
        """
        p1_score = self.calculate_player_score("Player 1", pieces)
        p2_score = self.calculate_player_score("Player 2", pieces)
        # If we consider Player 1 as maximizing player always:
        # Positive = good for Player 1, Negative = good for Player 2
        return p2_score - p1_score

    def calculate_player_score(self, player, pieces):
        remaining_squares = 0
        for piece in pieces[player]:
            remaining_squares += len(piece)
        return remaining_squares

    def play(self):
        """Main game loop for AI vs AI."""
        skip_count = 0  # Number of consecutive turns skipped
        ai_functions = {
            "Player 1": self.heuristic_ai,
            "Player 2": self.minimax_ai
        }
        while skip_count < 2:  # Game ends when both players skip their turns
            self.display_board()
            with open("board.txt", "a") as f:
                for row in self.board:
                    f.write(' '.join(['.' if cell is None else cell[0] for cell in row]) + "\n")
                f.write("\n")

            print(f"\n{self.current_player}'s turn:")

            move = ai_functions[self.current_player](self.current_player)
            if move:
                piece_index, position, rotated_pieces = move
                if self.place_piece(self.current_player, piece_index,rotated_pieces, position):
                    print(f"{self.current_player} placed a piece at {position}.")
                    skip_count = 0  # Reset skip count
                else:
                    print(f"{self.current_player} could not place a piece.")
            else:
                print(f"{self.current_player} has no valid moves and passes.")
                skip_count += 1  # Increment skip count

            # Switch to the next player
            self.switch_player()

        print("Game Over!")
        self.display_scores()

    # Then you would call `self.minimax_ai(self.current_player)` in your play loop for a turn instead of random_ai or heuristic_ai.
if __name__ == "__main__":
    game = BlokusDuoAI()
    game.play()