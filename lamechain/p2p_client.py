import argparse
import asyncio
import logging

from aiohttp import web, ClientSession, WSMsgType


log = logging.getLogger(__name__)


class P2PClient:
    def __init__(self, initial_peers_addresses=None, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.peers = []
        self.initial_peers_addresses = initial_peers_addresses or []

    async def connect_to_peers(self, app):
        session = ClientSession()
        for peer_addres in self.initial_peers_addresses:
            ws = await session.ws_connect(peer_addres)
            log.info('connected to: {}'.format(peer_addres))
            self.peers.append(ws)

    async def send_invitation(self, app):
        for ws in self.peers:
            log.info('sending')
            await ws.send_str('Merry Christmas')

    async def websocket_handler(self, request):

        ws = web.WebSocketResponse()
        await ws.prepare(request)

        self.peers.append(ws)
        log.info('new peer connected')

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    print(msg.data)
            elif msg.type == WSMsgType.ERROR:
                log.error('ws connection closed with exception {}'.format(
                    ws.exception()))

        self.peers.remove(ws)
        return ws

    def setup_routes(self, app):
        app.router.add_route('GET', '/', self.websocket_handler, name='peers')

    def get_app(self):
        app = web.Application()
        self.setup_routes(app)
        app.on_startup.append(self.connect_to_peers)
        app.on_startup.append(self.send_invitation)
        app['peers'] = self.peers
        return app


def run_p2p_client(host, port, peers=None):
    p2p = P2PClient(peers=peers)
    app = p2p.get_app()
    web.run_app(app, host=host, port=port, loop=p2p.loop)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str, nargs=1)
    parser.add_argument('port', type=int, nargs=1)
    parser.add_argument('--peers', nargs='*')
    options = parser.parse_args()
    run_p2p_client(
        host=options.host[0], port=options.port[0], peers=options.peers)


if __name__ == "__main__":
    main()
