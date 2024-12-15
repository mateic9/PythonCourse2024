import asyncio
MAX_CONNECTIONS = 5

# Create a semaphore with a limit
semaphore = asyncio.Semaphore(MAX_CONNECTIONS)
class GameServer:
    def __init__(self, host='127.0.0.1', port=8916):
        self.host = host
        self.port = port
        self.clients = []






    async def run_server(self):
         server=await




if __name__ == "__main__":
    game_server = GameServer()
    try:
        asyncio.run(game_server.run_server())
    except KeyboardInterrupt:
        print("Server stopped.")

