import socket
import threading
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
def handle_client(client_socket, client_address, client_id,players_barrier,e1,e2):
    print(f"Client {client_id} connected from {client_address}")
    try:
        connect_msg=f"You connected to the server with this {client_id}"
        client_socket.sendall(connect_msg.encode('utf-8'))
        b_id=players_barrier.wait()
        print("Am trecut de bariera")
        while True:
          e1.wait()
          e1.clear()
          get_move_from_player(client_socket)
          e2.set()



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
    wait_2players_barrier=threading.Barrier(2)
    e1.set()
    while client_id <= 2:
        client_socket, client_address = server_socket.accept()
        if(client_id==1):
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_id,wait_2players_barrier,e1,e2))
        else:
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_id,wait_2players_barrier,e2,e1))
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
