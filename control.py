class LogicGame:
    def __init__(self,mode, width=7, height=6,difficulty=None):
        """
        Initialize the game board with given width and height.
        """
        self.mode=mode
        self.width = width
        self.height = height
        self.difficulty = difficulty if mode == "singleplayer" else None
        self.board = [[0 for _ in range(width)] for _ in range(height)]  # 0 indicates empty cells
        self.current_player = 1  # Player 1 starts the game

    def print_board(self):
        """Prints the current state of the board."""
        for row in self.board:
            print("|" + " ".join(str(cell) for cell in row) + "|")
        print(" " + "-" * (2 * self.width - 1))

    def is_valid_move(self, column):
        """
        Checks if a move is valid (i.e., the column is not full).

        Args:
            column (int): The column where the player wants to drop a disc.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if column < 0 or column >= self.width:
            return False
        return self.board[0][column] == 0

    def make_move(self, column):
        """
        Drops a disc in the specified column for the current player if the move is valid.

        Args:
            column (int): The column where the player wants to drop a disc.

        Returns:
            bool: True if the move was successful, False if invalid.
        """
        if not self.is_valid_move(column):
            return False

        for row in reversed(range(self.height)):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                self.current_player = 3 - self.current_player  # Switch player (1 -> 2 or 2 -> 1)
                return True
        return False

    def check_winner(self):
        """
        Checks if there is a winner in the game.

        Returns:
            int: The player number (1 or 2) if there's a winner, 0 otherwise.
        """
        # Check horizontal, vertical, and diagonal lines
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 0:
                    continue

                player = self.board[row][col]

                # Horizontal
                if col + 3 < self.width and all(self.board[row][col + i] == player for i in range(4)):
                    return player

                # Vertical
                if row + 3 < self.height and all(self.board[row + i][col] == player for i in range(4)):
                    return player

                # Diagonal (down-right)
                if row + 3 < self.height and col + 3 < self.width and all(self.board[row + i][col + i] == player for i in range(4)):
                    return player

                # Diagonal (up-right)
                if row - 3 >= 0 and col + 3 < self.width and all(self.board[row - i][col + i] == player for i in range(4)):
                    return player

        return 0

    def is_full(self):
        """
        Checks if the board is full (no more valid moves).

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return all(self.board[0][col] != 0 for col in range(self.width))

    def is_game_finished(self):
        """
        Checks if the game is finished, either by a win or a draw.

        Returns:
            bool: True if the game is finished, False otherwise.
            int: 0 if draw, winning player's number otherwise.
        """
        winner = self.check_winner()
        if winner != 0:
            return True, winner
        if self.is_full():
            return True, 0  # Draw
        return False, None

# Example usage:
if __name__ == "__main__":
    game = LogicGame(3,3)
    game.print_board()

    while True:
        col = int(input(f"Player {game.current_player}, choose a column (0-{game.width - 1}): "))
        if game.make_move(col):
            game.print_board()
            finished, winner = game.is_game_finished()
            if finished:
                if winner == 0:
                    print("The game is a draw!")
                else:
                    print(f"Player {winner} wins!")
                break
        else:
            print("Invalid move. Try again.")
