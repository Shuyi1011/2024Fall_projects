import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches


def load_board_states(file_path):
    """Load board states from a text file."""
    with open(file_path, 'r') as f:
        content = f.read().strip()
    raw_states = content.split('\n\n')  # Separate rounds by double newline
    board_states = []
    for raw_state in raw_states:
        board = [row.split() for row in raw_state.split('\n')]
        board_states.append(board)
    return board_states


def create_animation(board_states, output_file=None):
    """Create an animation from board states."""
    fig, ax = plt.subplots(figsize=(7, 7))  # Adjust figsize to change the grid size
    ax.axis('off')  # Hide axes

    size = len(board_states[0])  # Assuming square board

    def render_board(ax, board):
        ax.clear()
        ax.axis('off')
        # Draw grid lines
        for x in range(size + 1):
            ax.axhline(x - 0.5, color='black', linewidth=1)  # Horizontal lines
            ax.axvline(x - 0.5, color='black', linewidth=1)  # Vertical lines

        # Fill cells with colors and labels
        for i in range(size):
            for j in range(size):
                cell = board[i][j]
                if cell == "X":  # Player 1
                    ax.add_patch(
                        patches.Rectangle(
                            (j - 0.5, size - i - 1 - 0.5), 1, 1, color="lightblue"
                        )
                    )
                    ax.text(j, size - i - 1, "X", ha="center", va="center", fontsize=12)
                elif cell == "O":  # Player 2
                    ax.add_patch(
                        patches.Rectangle(
                            (j - 0.5, size - i - 1 - 0.5), 1, 1, color="lightcoral"
                        )
                    )
                    ax.text(j, size - i - 1, "O", ha="center", va="center", fontsize=12)
                else:  # Empty cell
                    ax.add_patch(
                        patches.Rectangle(
                            (j - 0.5, size - i - 1 - 0.5), 1, 1, color="white"
                        )
                    )

    def update(frame):
        board = board_states[frame]
        render_board(ax, board)
        ax.set_title(f"Round {frame + 1}", fontsize=16)
        return []

    ani = FuncAnimation(fig, update, frames=len(board_states), interval=1000, blit=False)

    if output_file:
        if output_file.endswith(".gif"):
            ani.save(output_file, fps=1, writer="pillow")
        elif output_file.endswith(".mp4"):
            ani.save(output_file, fps=1, writer="ffmpeg")
        print(f"Animation saved as {output_file}")
    else:
        plt.show()


# Load board states
board_states = load_board_states("board.txt")

# Create and display the animation
create_animation(board_states, output_file="blokus_animation.gif")