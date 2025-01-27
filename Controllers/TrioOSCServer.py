import trio
    
class TrioOSCServer:

    def __init__(self, connectionTuple, dispatcher=None):
        self.ip, self.port = connectionTuple
        self._map = {}
        self.dispatcher = dispatcher 
        
    async def datagram_received(self, data: bytes, client_address: tuple[str, int]) -> None:
        await self.dispatcher.call_handlers_for_packet(data, client_address)
    
    async def start(self):
        sock = trio.socket.socket(trio.socket.AF_INET, 
                                trio.socket.SOCK_DGRAM)
        await sock.bind((self.ip, self.port))
        while True:
            try:
                data, addr = await sock.recvfrom(4096)
            except OSError:
                # Just discard the malformed packet and move on
                await trio.sleep(0)
                continue

            await self.datagram_received(data, addr)
            await trio.sleep(0)