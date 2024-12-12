import socket
import threading

# Game State
class Game:
    def __init__(self):
        self.players = []  # This will store the sockets of the two players
        self.active = False
        self.turn = 0  # 0 for player 1's turn, 1 for player 2's turn
        self.moves = {"Player 1": [], "Player 2": []}  # Stores the moves for each player

    def add_player(self, player_socket):
        self.players.append(player_socket)
        if len(self.players) == 2:
            self.start_game()

    def start_game(self):
        self.active = True
        player1, player2 = self.players
        player1.send("Game Started! You're Player 1\n".encode())
        player2.send("Game Started! You're Player 2\n".encode())

        # Start by telling Player 1 to take their turn
        player1.send("Your turn!\n".encode())
        player2.send("Waiting for Player 1...\n".encode())

    def process_move(self, player_socket, move):
        player_id = "Player 1" if player_socket == self.players[0] else "Player 2"
        # Add the move to the player's list of moves
        self.moves[player_id].append(move)
        self.switch_turn()

    def switch_turn(self):
        # Switch turns
        if self.turn == 0:
            self.turn = 1
            self.players[1].send("Your turn!\n".encode())  # Notify Player 2
            self.players[0].send("Waiting for Player 2...\n".encode())  # Notify Player 1
        else:
            self.turn = 0
            self.players[0].send("Your turn!\n".encode())  # Notify Player 1
            self.players[1].send("Waiting for Player 1...\n".encode())  # Notify Player 2

# Server to handle multiple games
class GameServer:
    def __init__(self, host="127.0.0.1", port=12345, max_matches=5):
        self.host = host
        self.port = port
        self.max_matches = max_matches
        self.matches = []  # List to keep track of current games
        self.lock = threading.Lock()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print("Server started, waiting for players...")

        while True:
            # Wait for an incoming connection
            client_socket, client_address = server_socket.accept()
            print(f"Player connected: {client_address}")

            # Handle player matching in a separate thread
            threading.Thread(target=self.match_players, args=(client_socket,)).start()

    def match_players(self, client_socket):
        with self.lock:
            # Find or create a match
            match_found = False
            for match in self.matches:
                if len(match.players) < 2:
                    match.add_player(client_socket)
                    match_found = True
                    break

            if not match_found and len(self.matches) < self.max_matches:
                # Create a new match if there's room
                new_game = Game()
                new_game.add_player(client_socket)
                self.matches.append(new_game)

            if not match_found:
                # Send message that player is waiting for an opponent
                client_socket.send("Waiting for opponent...\n".encode())

    def handle_turn(self, client_socket, move, match):
        if match.turn == 0 and client_socket == match.players[0]:  # Player 1's turn
            match.process_move(client_socket, move)
        elif match.turn == 1 and client_socket == match.players[1]:  # Player 2's turn
            match.process_move(client_socket, move)

# Start the server in a separate thread
def start_game_server():
    server = GameServer()
    server.start_server()

# Running the server in the background
server_thread = threading.Thread(target=start_game_server)
server_thread.daemon = True  # Daemonize the server thread so it stops with the program
server_thread.start()

# To keep the main program alive while the server is running
while True:
    pass  # Server continues to run in the background
