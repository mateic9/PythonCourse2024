
import asyncio

class GameServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.clients = []

    async def handle_client(self, reader, writer):
        address = writer.get_extra_info('peername')
        print(f"Client connected: {address}")
        self.clients.append((reader, writer))

        if len(self.clients) == 2:
            await self.start_game()

        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                print(f"Received {data.decode().strip()} from {address}")
        except asyncio.CancelledError:
            pass
        finally:
            print(f"Client disconnected: {address}")
            self.clients.remove((reader, writer))
            writer.close()
            await writer.wait_closed()

    async def start_game(self):
        for _, writer in self.clients:
            writer.write(b"Welcome to the Game!\n")
            await writer.drain()

        for round in range(3):  # Example: 3 rounds of play
            for reader, writer in self.clients:
                writer.write(b"Your turn! Enter a message: ")
                await writer.drain()
                data = await reader.readline()
                message = data.decode().strip()
                print(f"Player said: {message}")
                writer.write(f"You said: {message}\n".encode())
                await writer.drain()

        for _, writer in self.clients:
            writer.write(b"Game over. Thanks for playing!\n")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        self.clients.clear()

    async def run_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server started on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    game_server = GameServer()
    try:
        asyncio.run(game_server.run_server())
    except KeyboardInterrupt:
        print("Server stopped.")



