import asyncio

from foldex.tcp_server import TCPServer


async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: TCPServer(),
        "127.0.0.1",
        4040,
    )

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
