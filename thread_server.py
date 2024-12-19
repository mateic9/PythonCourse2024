import socket
import threading, time
winner_id=-1
def apply_move(move,game_finished,client_id):

    if "3" in move:
        game_finished.set()
        global winner_id
        winner_id=client_id
def is_valid_move(data):
    if "1" in data :
        return True
    else:
        return False
def get_move_from_player(client_socket):
    client_socket.sendall("Your turn now:".encode('utf-8'))
    move=client_socket.recv(1024).decode('utf-8')
    while not is_valid_move(move):
        client_socket.sendall(f"{move} is an invalid_move:".encode('utf-8'))
        move=client_socket.recv(1024).decode('utf-8')
    return move
def handle_client(client_socket, client_address, client_id,players_barrier,e1,e2,game_finished):
    print(f"Client {client_id} connected from {client_address}")
    try:
        connect_msg=f"You connected to the server with this {client_id}"
        client_socket.sendall(connect_msg.encode('utf-8'))
        b_id=players_barrier.wait()
        print("Am trecut de bariera")
        print(game_finished.is_set())

        while not game_finished.is_set():
          e1.wait()
          e1.clear()
          if game_finished.is_set():
              break
          current_move=get_move_from_player(client_socket)
          apply_move(current_move,game_finished,client_id)
          e2.set()
        global winner_id
        print(f"Value of winner_id:{winner_id}")
        client_socket.sendall(f"End of Game!Player with id:{client_id} won".encode('utf-8'))



    except Exception as e:
        print(f"Error with Client {client_id}: {e}")
    finally:
        client_socket.close()

def start_server(host='127.0.0.1', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)  # Allow up to two simultaneous connections

    print(f"Server started on {host}:{port}. Waiting for two clients...")

    client_id = 1
    threads = []
    e1 = threading.Event()
    e2 = threading.Event()
    game_finished=threading.Event()
    print(game_finished.is_set())
    wait_2players_barrier=threading.Barrier(2)
    e1.set()
    while client_id <= 2:
        client_socket, client_address = server_socket.accept()
        if(client_id==1):
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_id,wait_2players_barrier,e1,e2,game_finished))
        else:
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_id,wait_2players_barrier,e2,e1,game_finished))
        threads.append(thread)
        thread.start()
        client_id += 1

    # Wait for both threads to complete
    for thread in threads:
        thread.join()

    print("Both clients have disconnected. Shutting down server.")
    server_socket.close()

if __name__ == "__main__":
    start_server()
