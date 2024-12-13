import socket
import threading

# Define the server
class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connections = []

    def start(self):
        # Bind and listen for client connections
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Client connected: {client_address}")
            self.client_connections.append(client_socket)

            # Start a new thread to handle the client's communication
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            while True:
                # Receive data from the client
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                print(f"Received from client: {data}")

                # Process the data (in this case, just echoing it back)
                response = f"Server: {data}"
                client_socket.send(response.encode('utf-8'))
        except ConnectionResetError:
            print("Client disconnected unexpectedly")
        finally:
            client_socket.close()
            self.client_connections.remove(client_socket)

# Start the server
if __name__ == "__main__":
    server = GameServer()
    server.start()
