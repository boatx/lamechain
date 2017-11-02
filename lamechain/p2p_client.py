import argparse

from aiohttp import web, ClientSession

from chain import Chain
from handlers import websocket_handler


def setup_routes(app):
    app.router.add_route('GET', '/', websocket_handler, name='peers')


class P2PClient:
    def __init__(self, start_list_of_peers=None):
        self.start_list_of_peers = start_list_of_peers or []
        self.peers = []
        self.app = web.Application()
        self.app['peers'] = self.peers
        setup_routes(self.app)
        self.app.on_startup.append(self.connect_to_peers)
        self.app.on_startup.append(self.send_invitation)

    def run(self, host='localhost', port=8000):
        web.run_app(self.app, host=host, port=port)

    async def connect_to_peers(self, app):
        session = ClientSession()
        for peer in self.start_list_of_peers:
            ws = await session.ws_connect(peer)
            print('connected to: {}'.format(peer))
            app['peers'].append(ws)

    async def send_invitation(self, app):
        for ws in app['peers']:
            print('sending')
            await ws.send_str('Merry Christmas')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str, nargs=1)
    parser.add_argument('port', type=int, nargs=1)
    parser.add_argument('--peers', nargs='*')
    options = parser.parse_args()
    p2p = P2PClient(options.peers)
    p2p.run(host=options.host[0], port=options.port[0])


if __name__ == "__main__":
    main()
