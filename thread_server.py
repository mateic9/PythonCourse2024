import socket
import threading, time

from control import LogicGame

winner_id=-1
opponent_turn_message="Opponent move:"
confirmation_message="Received move:"
nr_moves=0
last_opp_move=-1
def send_move_client(client_socket,move):
    msg=opponent_turn_message+move
    client_socket.sendall(msg.encode('utf-8'))
def  wait_confirmation(client_socket):
      msg=client_socket.recv(1024).decode('utf-8')
      print("Confirmation:",msg)
def AI_decides_move():
    return "1"
def apply_move(move,game_finished,client_id):
    global last_opp_move
    last_opp_move=move
    if "3" in move:
        game_finished.set()
        global winner_id
        winner_id=client_id
def is_valid_move(data):
    if "1" in data  or "4" in data:
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
def handle_client_1p(client_socket, client_address,game_finished):
    move_index=0
    print("before loop")
    while not game_finished.is_set():
        if move_index % 2 == 0:

            current_move=get_move_from_player(client_socket)
            apply_move(current_move,game_finished,"Human")
        else:
            current_move=AI_decides_move()
            apply_move(current_move,game_finished,"AI")
            send_move_client(client_socket,current_move)
            wait_confirmation(client_socket)
        move_index+=1
    global winner_id
    print(f"Value of winner_id:{winner_id}")
    client_socket.sendall(f"End of Game!Player {winner_id} won".encode('utf-8'))


def handle_client_2p(client_socket, client_address, client_id,players_barrier,e1,e2,game_finished):
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
          global last_opp_move
          if last_opp_move !=-1:
              send_move_client(client_socket,last_opp_move)
              wait_confirmation(client_socket)
          current_move=get_move_from_player(client_socket)
          apply_move(current_move,game_finished,client_id)
          e2.set()


        global winner_id
        print(f"Value of winner_id:{winner_id}")
        client_socket.sendall(f"End of Game!Player with id:{winner_id} won".encode('utf-8'))



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
    multiMode=False
    threads = []
    e1 = threading.Event()
    e2 = threading.Event()
    e1.set()
    wait_2players_barrier=threading.Barrier(2)
    game_finished=threading.Event()
    print(game_finished.is_set())


    while client_id <= 2:
        print("Client id:",client_id)
        client_socket, client_address = server_socket.accept()
        client_args = client_socket.recv(1024).decode('utf-8').split(':')
        time.sleep(4)
        mode=client_args[0]
        height=client_args[1]
        width=client_args[2]
        print("parsat argumente")
        print(height)
        print(width)

        print("Cl_id:",client_id)
        time.sleep(4)
        if client_id == 1:
            print("id1")
            game=LogicGame(width,height)


        print("Am primit",mode)
        time.sleep(4)
        if mode=='singleplayer' :
           if not multiMode :
                 print("A single")
                 thread=threading.Thread(target=handle_client_1p, args=(client_socket, client_address,game_finished))
                 threads.append(thread)
                 thread.start()
                 time.sleep(10)
                 break
           else:
                client_id-=1
                client_socket.sendall("You were disconnected".encode('utf-8'))
                client_socket.close()


        if mode=='multiplayer':
            multiMode=True
            print(mode)
            time.sleep(4)
            if client_id==1:
              thread = threading.Thread(target=handle_client_2p, args=(client_socket, client_address, client_id,wait_2players_barrier,e1,e2,game_finished))
              threads.append(thread)
              thread.start()
            else:
              if game.height!=height or game.width!=width:
                client_id-=1
                client_socket.sendall("You were disconnected because the dimensions of the gameboard do not correspond".encode('utf-8'))
                client_socket.close()
              else:

                  print("Sec thread")
                  thread = threading.Thread(target=handle_client_2p, args=(client_socket, client_address, client_id,wait_2players_barrier,e2,e1,game_finished))
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
