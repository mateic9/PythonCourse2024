import socket

# Client to connect to the server
class GameClient:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port

    def start_client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        print("Connected to server!")

        while True:
            response = client_socket.recv(1024).decode()
            if response:
                print(response)
                if "Game Started!" in response:
                    self.play_game(client_socket)
                else:
                    print("Waiting for opponent...")

    def play_game(self, client_socket):
        while True:
            # Wait for the player's turn
            move = input("Enter your move (e.g., 'rock', 'paper', 'scissors') or 'end' to end turn: ")

            # Check if move is 'end' to indicate no more moves for this turn
            if move.lower() == 'end':
                client_socket.send("end".encode())
                break  # End this player's turn

            client_socket.send(move.encode())  # Send the move to the server
            opponent_move = client_socket.recv(1024).decode()
            print(f"Opponent's move: {opponent_move}")

if __name__ == "__main__":
    client = GameClient()
    client.start_client()
