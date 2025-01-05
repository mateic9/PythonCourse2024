# connect4_visuals.py
import tkinter as tk

class Connect4Visuals:



    def __init__(self, height, width):
        self.height = int(height)
        self.width = int(width)
        self.board = [["."] * self.width for _ in range(self.height)]

        self.root = tk.Tk()
        self.root.title("Connect4 Game")


        self.canvas = tk.Canvas(self.root, width=self.width * 100, height=self.height * 10, bg="green")
        self.canvas.pack()
        self.number_clicks = tk.IntVar(value=0)
        self.last_clicked=-1

        self.message_label = tk.Label(self.root, text="Player 1's turn (Red)", font=("Arial", 14), fg="blue")
        self.message_label.pack(pady=10)
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.buttons = []
        for row in range(self.height):
            button_row = []
            for col in range(self.width):
                canvas = tk.Canvas(button_frame, width=80, height=80, bg="white", bd=0, highlightthickness=0)
                round_button = canvas.create_oval(10, 10, 70, 70, fill="blue", outline="black")
                canvas.tag_bind(round_button, "<Button-1>", lambda event, c=col, r=row: self.on_button_click( c))
                canvas.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(canvas)

            self.buttons.append(button_row)

    def on_button_click(self, col):
        print("Click detected")
        self.last_clicked = col
        print("column:",col)
        self.number_clicks.set(self.number_clicks.get() + 1)
        print(self.number_clicks.get())



    def draw_board(self):
        self.root.update()

    def apply_move(self, col, player):
        col = int(col)
        for row in reversed(range(self.height)):
            if self.board[row][col] == ".":
                self.board[row][col] = "X" if player == "you" else "O"
                color = "red" if player == "you" else "yellow"
                print("Color:",color)
                print(f"{row},{col}")
                self.buttons[row][col].config(bg=color)
                self.draw_board()
                return True
        print(f"Column {col + 1} is full!")
        return False

    def game_over(self, winner):
        if winner == "draw":
            msg = "Game over! It's a draw!"
        else:
            msg = f"Game over! {winner.capitalize()} wins!"
        self.show_message(msg)
    def toggle_buttons(self, state):
     for row in self.buttons:
        for button in row:
            button["state"] = state
    def wait_for_move(self):
        self.root.wait_variable(self.number_clicks)
        return str(self.last_clicked)
    def update_message(self,message):
         self.message_label.config(text=message)




    def show_message(self, message):
        self.root.attributes('-disabled', True)
        top = tk.Toplevel(self.root)
        top.title("Game Over")
        top.geometry("300x150")
        tk.Label(top, text=message, font=("Arial", 14)).pack(pady=10)
        tk.Button(top, text="OK", command=self.root.quit).pack(pady=5)

    def on_close(self):
        self.root.quit()

    def start_mainloop(self):
        self.root.mainloop()