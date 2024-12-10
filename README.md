# Blokus Duo
## Team Member
Shuyi Guo, Yunhe Li

## Updates after presentation
1. Refine README, explain how to use our code/open the time complexity file.


## Game Rules
1. Objective:
Place as many of your pieces on the board as possible while blocking your opponent. The player with the fewest squares left unplaced wins.
2. Setup:
* The board is a 14x14 grid.
* Each player has 21 pieces of different shapes (like Tetris blocks), in their own color (e.g., black and white).
* The first player starts in the top-left corner, and the second player starts in the bottom-right corner.
3.	How to Play:
* Players take turns placing one piece at a time.
* Each new piece must touch at least one corner of your own previously placed pieces.
* Pieces cannot share edges with your own pieces but can touch edges of the opponent’s pieces.
* Pieces must stay entirely within the board.
4.	Game End:
* The game ends when neither player can place a piece.
* Each player scores the total number of squares in their unplaced pieces. The lower score wins.
5.	Bonus:
If a player places all their pieces, they receive a bonus of -5 points.

## Two AI players
* Random Player: it selects a valid move at random from the available options.
* Smart Player: (1) Heuristic AI: Evaluates potential moves based on a heuristic that maximizes future placement options; (2) Minimax AI: Uses the Minimax algorithm to evaluate the best move by simulating multiple future turns. Considers both the AI’s potential moves and the opponent’s responses to find the optimal strategy.

## How to use the code?
Run the following command:

```python blokus_game.py```

After game ends, a txt result file will be generated, which includes all game states. 

Then you can generate a GIF based on the result file. Run the following command:

```python output_animation.py```

## Time Complexity Analysis
Check the files named ```output.prof```

In order to open this file, you need to install a package by running the following command:

```pip install snakeviz```

Then open the file by running the following command:

```snakeviz output.prof```