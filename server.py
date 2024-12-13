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

        if len(self.clients) == 0:
            print("All clients disconnected. Restarting server.")

    async def start_game(self):
        if len(self.clients) < 2:
            for _, writer in self.clients:
                writer.write(b"Waiting for another player to connect...\n")
                await writer.drain()
            return

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
        async def game_loop():
            while True:
                if len(self.clients) == 2:
                    await self.start_game()
                    await asyncio.sleep(1)  # Avoid tight loops

        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server started on {self.host}:{self.port}")

        async with server:
            game_task = asyncio.create_task(game_loop())
            await server.serve_forever()
            game_task.cancel()
            try:
                await game_task
            except asyncio.CancelledError:
                pass

if __name__ == "__main__":
    game_server = GameServer()
    try:
        asyncio.run(game_server.run_server())
    except KeyboardInterrupt:
        print("Server stopped.")
