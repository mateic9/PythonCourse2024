import asyncio

async def tcp_client(client_id):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8916)
    print(f"Client {client_id} connected")
    try:
        while True:
            data = await reader.readline()
            if not data:  # Exit if the server closes the connection
                break
            print(f"Client {client_id} received: {data.decode().strip()}")
    except Exception as e:
        print(f"Client {client_id} encountered an error: {e}")
    finally:
        print(f"Client {client_id} closing connection")
        writer.close()
        await writer.wait_closed()

async def main():
    clients = [tcp_client(i) for i in range(1020)]
    await asyncio.gather(*clients)  # Run all clients concurrently

# Start the asyncio event loop
asyncio.run(main())
