import socket

# Define the client
class GameClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        # Connect to the server
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

    def send_message(self, message):
        # Send a message to the server
        self.client_socket.send(message.encode('utf-8'))
        print(f"Sent to server: {message}")

        # Receive a response from the server
        response = self.client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {response}")

    def close(self):
        # Close the connection
        self.client_socket.close()

# Start the client
if __name__ == "__main__":
    client = GameClient()
    client.connect()

    while True:
        # Get user input to simulate a game action
        message = input("Enter a message to send to the server (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client.send_message(message)

    client.close()
