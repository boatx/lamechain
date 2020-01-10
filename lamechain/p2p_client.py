import asyncio
import logging

from aiohttp import web, ClientSession, WSMsgType, ClientConnectorError

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


class P2PClient:
    def __init__(self, peers_addresses=None):
        self.peers = []
        self._session = None
        self._peers_addresses = peers_addresses or []

    async def connect_to_peers(self, app):
        self._session = ClientSession()
        loop = asyncio.get_event_loop()
        for peer_addres in self._peers_addresses:
            _, host = peer_addres.split("://")
            try:
                ws = await self._session.ws_connect(peer_addres)
                log.info("connecting to %s", peer_addres)
                await ws.send_str("INITIAL")
                loop.create_task(self.handle_response(ws))
            except ClientConnectorError:
                log.warning("Cannot connect to %s", host)

    async def send_block(self, block):
        for ws in self.peers:
            await ws.send_json(dict(block))

    async def handle_response(self, ws):
        self.peers.append(ws)
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                await self.handle_message(msg.data)
            elif msg.type == WSMsgType.ERROR:
                log.error(
                    "ws connection closed with exception {}".format(ws.exception())
                )
        self.peers.remove(ws)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        peername = request.remote
        log.info("new peer connected: %s", peername)
        await self.handle_response(ws)
        log.info("peer: %s has disconnected", peername)
        return ws

    async def handle_message(self, msg):
        log.info(msg)

    def setup_routes(self, app):
        app.router.add_route("GET", "/", self.websocket_handler, name="peers")

    def get_app(self):
        app = web.Application()
        self.setup_routes(app)
        app.on_startup.append(self.connect_to_peers)
        return app


def run_p2p_client(host, port, peers=None):
    peers = peers or []
    p2p = P2PClient(initial_peers_addresses=peers)
    app = p2p.get_app()
    web.run_app(app, host=host, port=port)
