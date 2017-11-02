from aiohttp import web

from lamechain.chain import Chain


class LocalServer:

    def __init__(self):
        self.chain = None

    def on_startup(self, app):
        self.chain = Chain()
        self.chain.sync()

    async def get_blocks(self, request):
        blocks = [dict(block) for block in self.chain.node_blocks]
        return web.json_response({'blocks': blocks})

    async def mine(self, request):
        # TODO pass data on post
        block = self.chain.mine_block(data='test')
        self.chain.add_block(block)
        return web.json_response(dict(block))

    def setup_routes(self, app):
        app.router.add_route('GET', '/blocks', self.get_blocks)
        app.router.add_route('GET', '/mine', self.mine)

    def get_app(self):
        app = web.Application()
        self.setup_routes(app)
        app.on_startup.append(self.on_startup)
        return app


def run_local_server():
    local_server = LocalServer()
    app = local_server.get_app()
    web.run_app(app, host='localhost', port=8888)
