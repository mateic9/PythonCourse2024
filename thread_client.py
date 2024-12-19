import socket

your_turn_message="Your turn now:"
invalid_move_msg="is an invalid_move:"
end_of_game_msg="End of Game!"
def make_a_move(client_socket):
    message = input("Enter your message (or 'quit' to exit): ")
    client_socket.sendall(message.encode('utf-8'))
def start_client(host='127.0.0.1', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        while True:
            # Send a message to the server
            # message = input("Enter your message (or 'quit' to exit): ")
            # if message.lower() == 'quit':
            #     break
            #
            # client_socket.sendall(message.encode('utf-8'))

            # Receive a response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Respone:{response}\n")
            if response=="Your turn now:" or invalid_move_msg in str(response):
                make_a_move(client_socket)
            if response.startswith(end_of_game_msg):
                break
        end_msg=input("Enter your message (or 'quit' to exit): ")
        print(end_msg)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Disconnected from server.")

if __name__ == "__main__":
    start_client()
