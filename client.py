import asyncio

async def tcp_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8916)
    await asyncio.sleep(3)
    # Read the welcome message from the server
    while True:
        data=await reader.readline()
        print(data)
    # await asyncio.sleep(3)



# Run the client
asyncio.run(tcp_client())
