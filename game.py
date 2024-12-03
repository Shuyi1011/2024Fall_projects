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

    def is_valid_move(self, piece, position):
        """Check if a piece can be placed at a given position."""
        start_x, start_y = position
        for dx, dy in piece:
            x, y = start_x + dx, start_y + dy
            if not (0 <= x < self.board_size and 0 <= y < self.board_size):  # Within bounds
                return False
            if self.board[x][y] is not None:  # No overlap
                return False
        return True

    def place_piece(self, player, piece_index, position):
        """Place a piece on the board for the current player."""
        piece = self.pieces[player][piece_index]
        if self.is_valid_move(piece, position):
            start_x, start_y = position
            for dx, dy in piece:
                x, y = start_x + dx, start_y + dy
                self.board[x][y] = "X" if player == "Player 1" else "O"
            self.placed_pieces[player].append(piece)
            self.pieces[player].pop(piece_index)  # Remove used piece
            return True
        return False

    def switch_player(self):
        """Switch to the next player."""
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def random_ai(self, player):
        """Dumb AI: Randomly selects a piece and position."""
        valid_moves = []
        for piece_index, piece in enumerate(self.pieces[player]):
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.is_valid_move(piece, (row, col)):
                        valid_moves.append((piece_index, (row, col)))
        return random.choice(valid_moves) if valid_moves else None

    def heuristic_ai(self, player):
        """Wise AI: Selects the move that maximizes board coverage."""
        best_move = None
        best_score = -1
        for piece_index, piece in enumerate(self.pieces[player]):
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.is_valid_move(piece, (row, col)):
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

    def play(self):
        """Main game loop for AI vs AI."""
        while True:
            self.display_board()
            print(f"\n{self.current_player}'s turn:")

            # AI logic
            if self.current_player == "Player 1":
                move = self.random_ai(self.current_player)  # Dumb player
            else:
                move = self.heuristic_ai(self.current_player)  # Wise player

            if move:
                piece_index, position = move
                self.place_piece(self.current_player, piece_index, position)
                print(f"{self.current_player} placed a piece at {position}.")
            else:
                print(f"{self.current_player} has no valid moves and passes.")
            
            # Check for game end
            if not any(self.random_ai(player) for player in self.players):
                print("Game Over!")
                break

            # Switch player
            self.switch_player()

if __name__ == "__main__":
    game = BlokusDuoAI()
    game.play()