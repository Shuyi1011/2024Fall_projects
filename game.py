import random

class BlokusDuoAI:
    def __init__(self):
        self.board_size = 14
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.pieces = self.generate_pieces()
        self.start_positions = {'Player 1': (0, 0), 'Player 2': (13, 13)}
        self.players = ['Player 1', 'Player 2']
        self.current_player = self.players[0]
        self.placed_pieces = {'Player 1': [], 'Player 2': []}
    
    def generate_full_blokus_pieces(self):
        """Generate the complete set of Blokus Duo pieces."""
        pieces = [
            # 1-square piece
            [(0, 0)],

            # 2-square pieces
            [(0, 0), (1, 0)],
            [(0, 0), (0, 1)],

            # 3-square pieces
            [(0, 0), (1, 0), (2, 0)],  # Line
            [(0, 0), (0, 1), (0, 2)],  # Horizontal line
            [(0, 0), (1, 0), (1, 1)],  # L-shape
            [(0, 0), (0, 1), (1, 1)],  # Corner

            # 4-square pieces
            [(0, 0), (1, 0), (2, 0), (3, 0)],  # Line
            [(0, 0), (0, 1), (0, 2), (0, 3)],  # Horizontal line
            [(0, 0), (1, 0), (2, 0), (2, 1)],  # L-shape
            [(0, 0), (0, 1), (1, 0), (1, 1)],  # Square
            [(0, 0), (1, 0), (1, 1), (2, 1)],  # Zigzag
            [(0, 0), (0, 1), (1, 1), (1, 2)],  # Reverse zigzag

            # 5-square pieces
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],  # Long line
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],  # Horizontal long line
            [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # L-shape
            [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)],  # T-shape
            [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)],  # Cross
            [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1)],  # Snake-like
            [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)],  # Hook
            [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)],  # U-shape
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

                # Check if the piece has edge contact with existing pieces
                for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if self.board[nx][ny] == current_player:
                            return False

        return has_corner_contact
        # return True

    def place_piece(self, player, piece_index, rotated_pieces, position):
        """Try to place a piece, checking all rotations."""
        # piece = self.pieces[player][piece_index]
        piece = rotated_pieces
        print(f"Placing piece {piece} for {player} at {position}")
        start_x, start_y = position
        for dx, dy in piece:
            x, y = start_x + dx, start_y + dy
            self.board[x][y] = "X" if player == "Player 1" else "O"
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
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.is_valid_move(player, piece, (row, col)):
                        # Heuristic: Maximize placement options for the next turn
                        score = self.evaluate_board_after_move(player, piece, (row, col))
                        if score > best_score:
                            best_score = score
                            best_move = (piece_index, (row, col))
        return best_move

    def evaluate_board_after_move(self, player, piece, position):
        """Evaluate board based on the number of valid moves after placing a piece."""
        # Simplified heuristic: Favor moves that maximize valid positions
        temp_board = [row[:] for row in self.board]
        start_x, start_y = position
        for dx, dy in piece:
            x, y = start_x + dx, start_y + dy
            temp_board[x][y] = player

        valid_positions = 0
        for piece in self.pieces[player]:
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.is_valid_move(piece, (row, col)):
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

    def play(self):
        """Main game loop for AI vs AI."""
        skip_count = 0  # Number of consecutive turns skipped
        while skip_count < 2:  # Game ends when both players skip their turns
            self.display_board()
            print(f"\n{self.current_player}'s turn:")

            move = self.random_ai(self.current_player)
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
if __name__ == "__main__":
    game = BlokusDuoAI()
    game.play()