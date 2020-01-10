import asyncio
import logging

from aiohttp import web
from lamechain.block import Block
from lamechain.chain import DB_FILENAME, Chain
from lamechain.p2p_client import P2PClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class LocalServer:
    def __init__(self, chain_db=DB_FILENAME):
        self.chain = None
        self.chain_db = chain_db

    def sync_chain(self):
        self.chain = Chain(chain_db=self.chain_db)
        self.chain.sync()

    async def mine(self, data):
        block = self.chain.mine_block(data)
        self.chain.add_block(block)
        return block

    async def get_blocks_handler(self, request):
        blocks = [dict(block) for block in self.chain.node_blocks[::-1]]
        return web.json_response({"blocks": blocks})

    async def mine_handler(self, request):
        post_data = await request.post()
        loop = asyncio.get_event_loop()
        loop.create_task(self.mine(post_data["data"]))
        return web.json_response({"status": "ok"})

    def setup_routes(self, app):
        app.router.add_route("GET", "/blocks", self.get_blocks_handler)
        app.router.add_route("POST", "/blocks", self.mine_handler)

    def get_app(self):
        app = web.Application()
        self.setup_routes(app)
        self.sync_chain()
        return app


class Server(LocalServer):
    def __init__(self, chain_db_file=DB_FILENAME, peers_addresses=None):
        super().__init__(chain_db_file)
        self.p2p = P2PClient(peers_addresses)

    async def mine(self, data):
        block = await super().mine(data)
        await self.p2p.send_block(block)

    async def handle_new_block(self, block):
        block = Block(**block)
        log.info("New block: %s", block)
        if self.chain.validate_block():
            log.info("adding new block")
            self.chain.add_block(block)

    def run(self, p2p_port=8080, http_port=8090):
        server_app = self.get_app()
        p2p_app = self.p2p.get_app()
        p2p_runner = web.AppRunner(p2p_app)
        server_runner = web.AppRunner(server_app)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(p2p_runner.setup())
        loop.run_until_complete(server_runner.setup())
        p2p_site = web.TCPSite(p2p_runner, "localhost", p2p_port)
        server_site = web.TCPSite(server_runner, "localhost", http_port)
        loop.run_until_complete(p2p_site.start())
        loop.run_until_complete(server_site.start())

        try:
            print("======== Running ========\n (Press CTRL+C to quit)")
            loop.run_forever()
        except KeyboardInterrupt:  # pragma: no cover
            pass


def run_local_server(port):
    local_server = LocalServer()
    app = local_server.get_app()
    web.run_app(app, host="localhost", port=port)
