import socket
import threading, time

from control import LogicGame

winner_id=-1
opponent_turn_message="Opponent move:"
confirmation_message="Received move:"
valid_move_msg="Valid move:"
nr_moves=0
last_opp_move=-1
def prepend_length(message):
    # Calculate the length of the message
    length = len(message)
    # Return the message with the length prepended
    return f"{length}:{message}"

def send_move_client(client_socket,move):
    msg=opponent_turn_message+str(move)
    client_socket.sendall(prepend_length(msg).encode('utf-8'))
def  wait_confirmation(client_socket):
      msg=client_socket.recv(1024).decode('utf-8')
      print("Confirmation:",msg)
def AI_decides_move():
    return 1
def get_move_from_player(client_socket,game):
    client_socket.sendall(prepend_length("Your turn now:").encode('utf-8'))
    move=int(client_socket.recv(1024).decode('utf-8'))
    while not game.is_valid_move(move):
        client_socket.sendall(prepend_length(f"{move} is an invalid_move:").encode('utf-8'))
        move=int(client_socket.recv(1024).decode('utf-8'))

    client_socket.sendall(prepend_length(f"Valid move:{move}").encode('utf-8'))
    return move
def handle_client_1p(client_socket, client_address,game_finished,game):
    move_index=0
    print("before loop")
    while not game.is_game_finished()[0]:
        if move_index % 2 == 0:

            current_move=get_move_from_player(client_socket,game)
            game.make_move(int(current_move))
        else:
            current_move=int(game.AI_decides_move())
            game.make_move(current_move)
            send_move_client(client_socket,current_move)
            wait_confirmation(client_socket)
        move_index+=1
    # global winner_id
    # print(f"Value of winner_id:{winner_id}")
    # client_socket.sendall(f"End of Game!Player {winner_id} won".encode('utf-8'))
    print("Out of loop")

    win_id=game.is_game_finished()[1]
    print(f"Value of winner_id:{win_id}")

    print(f"Value of winner_id:{win_id}")

    client_socket.sendall(prepend_length(f"End of Game!Player with id:{win_id} won").encode('utf-8'))


def handle_client_2p(client_socket, client_address, client_id,players_barrier,e1,e2,game):
    print(f"Client {client_id} connected from {client_address}")
    try:
        connect_msg=f"You connected to the server with this {client_id}"
        client_socket.sendall(prepend_length(connect_msg).encode('utf-8'))
        b_id=players_barrier.wait()
        print("Am trecut de bariera")

        while not game.is_game_finished()[0]:
          e1.wait()
          e1.clear()
          print(f"{client_id} trece de wait")
          if game.is_game_finished()[0]:
              break
          print("Nu face break")

          global last_opp_move
          if last_opp_move !=-1:
              send_move_client(client_socket,last_opp_move)
              wait_confirmation(client_socket)

          current_move=get_move_from_player(client_socket,game)
          game.make_move(int(current_move))
          last_opp_move=current_move
          e2.set()

        print("Out of loop")

        win_id=game.is_game_finished()[1]
        print(f"Value of winner_id:{win_id}")

        print(f"Value of winner_id:{win_id}")

        client_socket.sendall(prepend_length(f"End of Game!Player with id:{win_id} won").encode('utf-8'))



    except Exception as e:
        print(f"Error with Client {client_id}: {e}")
        time.sleep(30)
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

        mode=client_args[0]
        height=client_args[1]
        width=client_args[2]
        if mode =="singleplayer":
            level=client_args[3]
            game=LogicGame(mode,int(width),int(height),level)
        else:
            if client_id==1:
             game=LogicGame(mode,int(width),int(height))



        if mode=='singleplayer' :
           if not multiMode :
                 print("A single")
                 thread=threading.Thread(target=handle_client_1p, args=(client_socket, client_address,game_finished,game))
                 threads.append(thread)
                 thread.start()

                 break
           else:
                client_id-=1
                client_socket.sendall(prepend_length("You were disconnected").encode('utf-8'))
                client_socket.close()


        if mode=='multiplayer':
            multiMode=True
            print(mode)

            if client_id==1:
              thread = threading.Thread(target=handle_client_2p, args=(client_socket, client_address, client_id,wait_2players_barrier,e1,e2,game))
              threads.append(thread)
              thread.start()
            else:
              if game.height!= int(height) or game.width!=int(width):
                client_id-=1
                client_socket.sendall(prepend_length("You were disconnected because the dimensions of the gameboard do not correspond").encode('utf-8'))
                client_socket.close()
              else:

                  print("Sec thread")

                  thread = threading.Thread(target=handle_client_2p, args=(client_socket, client_address, client_id,wait_2players_barrier,e2,e1,game))
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
