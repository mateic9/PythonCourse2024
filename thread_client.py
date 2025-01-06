import socket
import argparse,time
import sys
from click import confirmation_option
from visual import Connect4Visuals
your_turn_message="Your turn now:"
invalid_move_msg="is an invalid_move"
end_of_game_msg="End of Game!"
opponent_turn_message="Opponent move:"
confirmation_message="Received move:"
disconnect_message="You were disconnected"
valid_move_msg="Valid move"
def validate_args(args):
    """
    Validate the command-line arguments after parsing

    Parameters:
        args (Namespace): Parsed command-line arguments

    Raises:
        SystemExit: If required arguments for singleplayer mode are missing
    """
    if args.mode == "singleplayer" and not args.difficulty and not args.first:
        print("Error: --difficulty and --first  is required when mode is 'singleplayer", file=sys.stderr)
        sys.exit(1)
def receive_message(client_socket):
    """
    Receive a message from the server with length-prefix encoding.

    Parameters:
        client_socket (socket): The client's socket connection.

    Returns:
        str: The decoded message received from the server.

    Raises:
        ValueError: If the message length is invalid or data is incomplete.
    """
    length_data = b''
    while True:
        byte = client_socket.recv(1)
        if byte == b':' or not byte:
            break
        length_data += byte

    if not length_data:
        raise ValueError("No length data received or socket closed")


    message_length = int(length_data.decode('utf-8'))


    message_data = client_socket.recv(message_length)

    if len(message_data) != message_length:
        raise ValueError(f"Message length mismatch: expected {message_length} but received {len(message_data)}")


    return message_data.decode('utf-8')
def make_a_move(client_socket, visuals):
    """
    Allow the player to make a move and send it to the server.

    Parameters:
        client_socket (socket): The client's socket connection.
        visuals (Connect4Visuals): Visual representation of the game board.
    """
    visuals.toggle_buttons("normal")
    # message = input("Enter your move (column number): ")
    message=visuals.wait_for_move()

    visuals.toggle_buttons("disabled")
    client_socket.sendall(message.encode('utf-8'))


def start_client(host='127.0.0.1', port=65432):
    """
    Start the client for a Connect 4 game and communicate with the server.

    Parameters:
        host (str): The server's IP address or hostname.
        port (int): The server's port number.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)
    try:
        client_socket.connect((host, port))


        global client_params

        client_socket.sendall(client_params.encode('utf-8'))

        tokens_params = client_params.split(':')
        height = tokens_params[1]
        width = tokens_params[2]
        visuals = Connect4Visuals(height, width)
        visuals.draw_board()

        while True:
            try:

                response = receive_message(client_socket)

                visuals.update_message(response)

                if "Your turn now:" in response or invalid_move_msg in response:
                    make_a_move(client_socket, visuals)

                elif response.startswith(valid_move_msg):
                    move = response.split(':')[1]
                    visuals.apply_move(move, "you")

                elif response.startswith(opponent_turn_message):
                    opp_move = response.split(':')[1]
                    visuals.apply_move(opp_move, "opponent")
                    msg = confirmation_message + opp_move

                    client_socket.sendall(msg.encode('utf-8'))

                elif response.startswith(end_of_game_msg) or response.startswith(disconnect_message):

                    visuals.update_message(response)
                    visuals.message_label.update_idletasks()
                    visuals.message_label.update()

                    time.sleep(10)
                    break

            except socket.timeout:
                visuals.update_message("No response from server, retrying...")
                continue

        visuals.update_message("Game session ended.")
    except Exception as e:

        time.sleep(45)
    finally:
        client_socket.close()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Client for 2-player or single-player game.")
    parser.add_argument("--mode", type=str, choices=["multiplayer", "singleplayer"], required=True,help="Game mode: 'multiplayer' to play against another player, 'singleplayer' to play against the server AI")
    parser.add_argument("--height", type=str, required=True)
    parser.add_argument("--width", type=str, required=True)
    parser.add_argument("--difficulty", type=str, choices=["easy", "medium", "hard"],
                    help="Difficulty level for single-player mode: 'easy', 'medium', 'hard'")
    parser.add_argument("--first", type=str, choices=["yes", "no"],
                    help="Decides if the player is first or not")
    args = parser.parse_args()
    validate_args(args)
    client_params=':'.join(str(value) for value in vars(args).values())
    print("Args launching client:",client_params)
    # time.sleep(4)
    start_client()
