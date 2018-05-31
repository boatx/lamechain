import logging

from aiohttp import web, ClientSession, WSMsgType, ClientConnectorError

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


class P2PClient:
    def __init__(self, initial_peers_addresses=None):
        self.peers = {}
        self.initial_peers_addresses = initial_peers_addresses or []

    async def connect_to_peers(self, app):
        session = ClientSession()
        for peer_addres in self.initial_peers_addresses:
            _, host = peer_addres.split('://')
            try:
                ws = await session.ws_connect(peer_addres)
                log.info('connected to: {}'.format(peer_addres))
                self.peers[host] = ws
            except ClientConnectorError:
                log.warning('Cannot connect to: {}'.format(host))

    async def send_invitation(self, app):
        for ws in self.peers.values():
            log.info('sending')
            await ws.send_str('Initial')

    async def websocket_handler(self, request):

        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.peers[request.host] = ws

        log.info('new peer connected: {}'.format(request.host))

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                await self.handle_message(msg.data)
            elif msg.type == WSMsgType.ERROR:
                log.error('ws connection closed with exception {}'.format(
                    ws.exception()))

        self.peers.remove(ws)
        return ws

    async def handle_message(self, msg):
        log.info(msg)

    def setup_routes(self, app):
        app.router.add_route('GET', '/', self.websocket_handler, name='peers')

    def get_app(self):
        app = web.Application()
        self.setup_routes(app)
        app.on_startup.append(self.connect_to_peers)
        app.on_startup.append(self.send_invitation)
        return app


def run_p2p_client(host, port, peers=None):
    peers = peers or []
    p2p = P2PClient(initial_peers_addresses=peers)
    app = p2p.get_app()
    web.run_app(app, host=host, port=port)
