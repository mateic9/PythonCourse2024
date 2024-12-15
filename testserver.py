# SuperFastPython.com
# example of creating a server
import asyncio

# handler for client connections
async def handler(reader, writer):
    addr = writer.get_extra_info('peername')
    print(type(writer))
    for i in range(0,3):
        writer.write("Lalala\n".encode())
        await writer.drain()
# main coroutine
async def main():
    # create an asyncio server
    server = await asyncio.start_server(handler, '127.0.0.1', port=8916)
    # report the details of the server
    print(server)
    await server.serve_forever()
    print(server)

# start the asyncio event loop
asyncio.run(main())