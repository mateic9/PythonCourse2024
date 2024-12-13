import asyncio
async def game_client(host='127.0.0.1', port=8888):
    reader, writer = await asyncio.open_connection(host, port)

    print("Connected to the server. Type your messages below.")
    try:
        while True:
            server_message = await reader.readline()
            if not server_message:
                break
            print(f"Server: {server_message.decode().strip()}")

            if "Your turn!" in server_message.decode():
                user_input = input("You: ")
                writer.write(f"{user_input}\n".encode())
                await writer.drain()
    except asyncio.CancelledError:
        pass
    finally:
        print("Disconnected from the server.")
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(game_client())
    except KeyboardInterrupt:
        print("Client stopped.")