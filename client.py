import socket
import argparse,time

from click import confirmation_option
from visual import Connect4Visuals
your_turn_message="Your turn now:"
invalid_move_msg="is an invalid_move:"
end_of_game_msg="End of Game!"
opponent_turn_message="Opponent move:"
confirmation_message="Received move:"
disconnect_message="You were disconnected"
valid_move_msg="Valid move:"
def make_a_move(client_socket, visuals):
    # visuals.draw_board()
    message = input("Enter your move (column number): ")
    client_socket.sendall(message.encode('utf-8'))
    print("s-a trimis mutarea")
def apply_move(move):
    print(f"{move} is applied")
# def make_a_move(client_socket):
#     message = input("Enter your message (or 'quit' to exit): ")
#     client_socket.sendall(message.encode('utf-8'))
# def start_client(host='127.0.0.1', port=65432):
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         client_socket.connect((host, port))
#         print(f"Connected to server at {host}:{port}")
#
#         global client_params
#         print(client_params)
#         client_socket.sendall(client_params.encode('utf-8'))
#         print("Am trimis parametrii")
#         tokens_params=client_params.split(':')
#         height=tokens_params[1]
#         width=tokens_params[2]
#         visuals = Connect4Visuals(height, width)
#         while True:
#             # Send a message to the server
#             # message = input("Enter your message (or 'quit' to exit): ")
#             # if message.lower() == 'quit':
#             #     break
#             #
#             # client_socket.sendall(message.encode('utf-8'))
#
#             # Receive a response from the server
#             response = client_socket.recv(1024).decode('utf-8')
#             print(f"Response:{response}\n")
#             if response=="Your turn now:" or invalid_move_msg in str(response):
#
#                 make_a_move(client_socket,visuals)
#             if response.startswith(valid_move_msg):
#                 move=response.split(':')[1]
#                 visuals.apply_move(move, "player")
#             if response.startswith(opponent_turn_message):
#                 opp_move=response.split(':')[1]
#                 visuals.apply_move(opp_move, "opponent")
#                 msg=confirmation_message+opp_move
#                 print("inainte de confirmare")
#                 client_socket.sendall(msg.encode('utf-8'))
#                 print("dupa confirmare")
#             if response.startswith(end_of_game_msg) or response.startswith(disconnect_message):
#                 winner = response.split(":")[1] if ":" in response else "draw"
#                 visuals.game_over(winner)
#                 break
#         end_msg=input("Enter your message (or 'quit' to exit): ")
#         print(end_msg)
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         client_socket.close()
#         print("Disconnected from server.")
def start_client(host='127.0.0.1', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)  # Set a timeout for server responses
    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        global client_params
        print(client_params)
        client_socket.sendall(client_params.encode('utf-8'))
        print("Parameters sent to server.")
        tokens_params = client_params.split(':')
        height = tokens_params[1]
        width = tokens_params[2]
        visuals = Connect4Visuals(height, width)
        visuals.draw_board()

        while True:
            try:
                # Receive a response from the server
                response = client_socket.recv(1024).decode('utf-8')
                print(f"Response: {response}\n")
                time.sleep(1)
                if "Your turn now:" in response or invalid_move_msg in response:
                    make_a_move(client_socket, visuals)

                elif response.startswith(valid_move_msg):
                    move = response.split(':')[1]
                    visuals.apply_move(move, "you")

                elif response.startswith(opponent_turn_message):
                    opp_move = response.split(':')[1]
                    visuals.apply_move(opp_move, "opponent")
                    msg = confirmation_message + opp_move
                    print("Sending confirmation to server.")
                    client_socket.sendall(msg.encode('utf-8'))

                elif response.startswith(end_of_game_msg) or response.startswith(disconnect_message):
                    winner = response.split(":")[1] if ":" in response else "draw"
                    visuals.game_over(winner)
                    break

            except socket.timeout:
                print("No response from server, retrying...")
                continue

        print("Game session ended.")
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(45)
    finally:
        client_socket.close()
        print("Disconnected from server.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Client for 2-player or single-player game.")
    parser.add_argument("--mode", type=str, choices=["multiplayer", "singleplayer"], required=True,help="Game mode: 'multiplayer' to play against another player, 'singleplayer' to play against the server AI")
    parser.add_argument("--height", type=str, required=True)
    parser.add_argument("--width", type=str, required=True)
    args = parser.parse_args()
    # client_params+=args.mode
    client_params=':'.join(str(value) for value in vars(args).values())
    print(client_params)
    # time.sleep(4)
    start_client()
