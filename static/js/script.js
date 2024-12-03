const boardElement = document.getElementById('board');
const statusElement = document.getElementById('status');

async function fetchBoard() {
    try {
        const response = await fetch('/api/get_board');
        const gameState = await response.json();
        renderBoard(gameState.board);
        statusElement.textContent = `Current Player: ${gameState.current_player}`;

        // If it's AI's turn, automatically make a move
        if (gameState.current_player === "Player 2") {
            await makeMove(); // No parameters for AI move
        }
    } catch (error) {
        console.error("Error fetching board:", error);
    }
}

function renderBoard(board) {
    boardElement.innerHTML = ''; // Clear the board
    board.forEach(row => {
        row.forEach(cell => {
            const div = document.createElement('div');
            div.className = `cell ${cell || ''}`;
            boardElement.appendChild(div);
        });
    });
}

async function makeMove(pieceIndex = null, position = null) {
    const data = pieceIndex !== null && position !== null
        ? { piece_index: pieceIndex, position: position }
        : {}; // Empty for AI move

    try {
        const response = await fetch('/api/make_move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            await fetchBoard(); // Update board after move
        } else {
            const error = await response.json();
            statusElement.textContent = error.message;
        }
    } catch (error) {
        console.error("Error making move:", error);
    }
}

async function resetGame() {
    try {
        const response = await fetch('/api/reset', { method: 'POST' });
        if (response.ok) {
            await fetchBoard(); // Reset board state
        } else {
            console.error("Error resetting game");
        }
    } catch (error) {
        console.error("Error resetting game:", error);
    }
}

// Initial fetch of the board state
fetchBoard();
