
class LogicGame:
    def __init__(self,mode, width=7, height=6,difficulty=None):

        self.mode=mode
        self.width = width
        self.height = height

        self.difficulty = difficulty if mode == "singleplayer" else None
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.current_player = 1
        if self.mode=="singleplayer" and self.difficulty not in ["easy","medium","hard"]:
             raise Exception("Difficulty parameter problem")
        if self.difficulty=="easy":
            self.depth=1
        if self.difficulty=="medium":
            self.depth=2
        if self.difficulty=="hard":
            self.depth=3

    def print_board(self):

        for row in self.board:
            print("|" + " ".join(str(cell) for cell in row) + "|")
        print(" " + "-" * (2 * self.width - 1))

    def is_valid_move(self, column):

        """
        Check if a move is valid for the given column

        Parameters:
            column (int): The column index where the player wants to place their piece

        Returns:
            bool: True if the move is valid (column is within bounds and not full), otherwise False
        """
        if column < 0 or column >= self.width:
            return False
        return self.board[0][column] == 0

    def make_move(self, column):
        """

        Place the current player's piece in the specified column if the chosen move is a valid one

        The piece is placed in the lowest available row in the column
        The turn alternates between players after a successful move

        Parameters:
            column (int): The column index where the piece is to be placed

        Returns:
            bool: True if the move was successful, otherwise False if the move is invalid
        """
        if not self.is_valid_move(column):
            return False

        for row in reversed(range(self.height)):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                self.current_player = 3 - self.current_player
                return True
        return False

    def check_winner(self):
        """
        Check if there is a winner on the board.

        Evaluates horizontal, vertical, and diagonal lines for a sequence of 4
        matching pieces for either player.

        Returns:
            int: The player number (1 or 2) if there is a winner, or 0 if no winner exists.
        """
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

                # Diagonal dreapta jos
                if row + 3 < self.height and col + 3 < self.width and all(self.board[row + i][col + i] == player for i in range(4)):
                    return player

                # Diagonal dreapta sus
                if row - 3 >= 0 and col + 3 < self.width and all(self.board[row - i][col + i] == player for i in range(4)):
                    return player

        return 0

    def is_full(self):
        return all(self.board[0][col] != 0 for col in range(self.width))

    def is_game_finished(self):
        winner = self.check_winner()
        if winner != 0:
            return True, winner
        if self.is_full():
            return True, 0
        return False, None
    def AI_decides_move(self):
        """
        Determine the optimal move for the AI player using the minimax algorithm

        Copies the current board state after evaluating all potential moves up to the
        configured depth and selecting the move with the best score.

        Returns:
            int: The column index of the best move for the AI.
        """



        boardcopy = self.copy_board()
        score,best_move=self.minimax(2*self.depth,boardcopy)
        print(f"AI Decision -> Score: {score}, Best Move: {best_move}")

        if best_move is not None:
            print("before making move")
            print(best_move)
            self.make_move(int(best_move))
            print("after making move")
        self.print_board()
        return best_move

    def copy_board(self):
        boardcopy=[]
        for  row in self.board:
            copy_row=[]
            for element in row:
                 copy_row.append(element)
            boardcopy.append(copy_row)
        return boardcopy
    def is_valid_move_AI_sim(self,board,col,id_player):
        if col < 0 or col >= len(board[0]):
            return False
        return board[0][col] == 0
    def apply_move_AI_sim(self,board,column,id_player):
        height=len(board)
        for row in range(height-1,-1,-1):
            if board[row][column] ==0:
                board[row][column]=id_player
                return row
    def unapply_move_AI_sim(self,board,column,row):
        board[row][column] =0

    def minimax(self, total_moves, board):
        """
        Perform the minimax algorithm to evaluate the optimal move for a player

        Recursively simulates all possible moves up to a given depth, scoring each
        move based on its effect on the board state

        Parameters:
            total_moves (int): The remaining depth for the minimax evaluation.
            board (list): The current simulated state of the game board.

        Returns:
            tuple: A score representing the board state and the column index of the best move.
        """
        width = len(board[0])
        map_score_move = {}
        key_to_return = None
        min_score = float('inf')
        max_score = float('-inf')


        if total_moves == 0:
            return self.evaluate_board(board,self.current_player), None


        id_player = 1 if total_moves % 2 == 0 else 2

        for col in range(width):
            if self.is_valid_move_AI_sim(board, col, id_player):
                row = self.apply_move_AI_sim(board, col, id_player)
                score, _ = self.minimax(total_moves - 1, board)
                map_score_move[col] = score
                self.unapply_move_AI_sim(board, col, row)


        if id_player == 1:
            for key, value in map_score_move.items():
                if value < min_score:
                    min_score = value
                    key_to_return = key

            return min_score, key_to_return
        else:
            for key, value in map_score_move.items():
                if value > max_score:
                    max_score = value
                    key_to_return = key

            return max_score, key_to_return

    def evaluate_board(self, board,ai_id):
        score = 0
        ai_player = ai_id
        opponent_player = 3-ai_id

        if self.check_win(board, ai_player):
            return 9999999
        elif self.check_win(board, opponent_player):
            return -99999999

        score+=1000*self.count_open_sequences(board,ai_player,2)+2000*self.count_open_sequences(board,ai_player,3)

        score-=1000*self.count_open_sequences(board,opponent_player,2)+2000*self.count_open_sequences(board,opponent_player,3)

        score+=50*self.count_sequences(board,ai_player,2)+100*self.count_sequences(board,ai_player,3)
        score-=50*self.count_sequences(board,opponent_player,2)+100*self.count_sequences(board,opponent_player,3)
        # if score <-1000:
        #     print(score)
        return score


    def count_sequences(self, board, player, length):

        count = 0

        for row in range(len(board)):
            for col in range(len(board[0])):
                if self.check_sequence(board, row, col, 1, 0, player, length):  # Horizontal
                    count += 1
                if self.check_sequence(board, row, col, 0, 1, player, length):  # Vertical
                    count += 1
                if self.check_sequence(board, row, col, 1, 1, player, length):  # Diagonal /
                    count += 1
                if self.check_sequence(board, row, col, 1, -1, player, length):  # Diagonal \
                    count += 1

        return count
    def check_win(self, board, player):


        for row in range(len(board)):
            for col in range(len(board[0])):
                if (
                    self.check_direction(board, row, col, 1, 0, player) or  # Horizontal
                    self.check_direction(board, row, col, 0, 1, player) or  # Vertical
                    self.check_direction(board, row, col, 1, 1, player) or  # Diagonal /
                    self.check_direction(board, row, col, 1, -1, player)   # Diagonal \
                ):
                    return True
        return False
    def check_direction(self, board, row, col, delta_row, delta_col, player):

        for i in range(4):
            r, c = row + i * delta_row, col + i * delta_col
            if not (0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player):
                return False
        return True
    def check_sequence(self, board, row, col, delta_row, delta_col, player, length):

        count = 0
        for i in range(length):
            r, c = row + i * delta_row, col + i * delta_col
            if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
                count += 1
            else:
                break
        return count == length
    def count_open_sequences(self, board, player, length):
        def is_open_sequence(line, start, length):
            """
            Check if the sequence of the specified length is open on both ends.
            """
            end = start + length
            if start > 0 and end < len(line):
                return line[start - 1] == 0 and line[end] == 0
            return False

        count = 0
        rows, cols = len(board), len(board[0])

        # Check horizontally
        for row in range(rows):
            for col in range(cols - length + 1):
                window = board[row][col:col + length]
                if window.count(player) == length and is_open_sequence(board[row], col, length):
                    count += 1

        # Check vertically
        for col in range(cols):
            for row in range(rows - length + 1):
                window = [board[row + i][col] for i in range(length)]
                if window.count(player) == length:
                    if (row > 0 and row + length < rows and board[row - 1][col] == 0 and board[row + length][col] == 0):
                        count += 1


        for row in range(rows - length + 1):
            for col in range(cols - length + 1):
                window = [board[row + i][col + i] for i in range(length)]
                if window.count(player) == length:

                    if (row > 0 and col > 0 and row + length < rows and col + length < cols and
                            board[row - 1][col - 1] == 0 and board[row + length][col + length] == 0):
                        count += 1


        for row in range(length - 1, rows):
            for col in range(cols - length + 1):
                window = [board[row - i][col + i] for i in range(length)]
                if window.count(player) == length:
                    if (row + 1 < rows and col > 0 and row - length + 1 >= 0 and col + length < cols and
                            board[row + 1][col - 1] == 0 and board[row - length][col + length] == 0):
                        count += 1

        return count


