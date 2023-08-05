import asyncio
from asyncio import transports


class TCPServer(asyncio.Protocol):
    def connection_made(self, transport: transports.BaseTransport) -> None:
        peername = transport.get_extra_info("peername")
        print(f"Connection from {peername}")
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        message = data.decode()
        print(f"Data received: {message}")

        print(f"Send: {message}")
        self.transport.write(message)

        print(f"Close the client socket")
        self.transport.close()
