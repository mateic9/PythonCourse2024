import tkinter as tk

class Connect4Visuals:
    def __init__(self, height, width, on_column_click):
        self.height = int(height)
        self.width = int(width)
        self.board = [["."] * self.width for _ in range(self.height)]
        self.on_column_click = on_column_click  # Callback for column click
        self.root = tk.Tk()
        self.root.title("Connect4 Game")

        self.canvas = tk.Canvas(self.root, width=self.width * 100, height=self.height * 100, bg="blue")
        self.canvas.pack()

        self.cells = []
        for row in range(self.height):
            cell_row = []
            for col in range(self.width):
                x1, y1 = col * 100, row * 100
                x2, y2 = x1 + 100, y1 + 100
                cell = self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="white")
                cell_row.append(cell)
            self.cells.append(cell_row)

        self.canvas.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        col = event.x // 100 + 1  # Convert click position to column number
        if self.on_column_click:
            self.on_column_click(col)

    def apply_move(self, col, player):
        col = int(col) - 1  # Convert to zero-based index
        for row in reversed(range(self.height)):
            if self.board[row][col] == ".":
                self.board[row][col] = "X" if player == "you" else "O"
                color = "red" if player == "you" else "yellow"
                self.canvas.itemconfig(self.cells[row][col], fill=color)
                self.root.update()
                return True
        print(f"Column {col + 1} is full!")
        return False

    def game_over(self, winner):
        msg = f"Game over! {winner.capitalize()} wins!" if winner != "draw" else "Game over! It's a draw!"
        self.show_message(msg)

    def show_message(self, message):
        self.root.attributes('-disabled', True)
        top = tk.Toplevel(self.root)
        top.title("Game Over")
        top.geometry("300x150")
        tk.Label(top, text=message, font=("Arial", 14)).pack(pady=10)
        tk.Button(top, text="OK", command=self.root.quit).pack(pady=5)

    def start_mainloop(self):
        self.root.mainloop()
