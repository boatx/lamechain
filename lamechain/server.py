import asyncio

from aiohttp import web

from lamechain.chain import Chain


class LocalServer:

    def __init__(self, loop=None):
        self.chain = None
        self.loop = loop or asyncio.get_event_loop()

    def on_startup(self, app):
        self.chain = Chain()
        self.chain.sync()

    async def get_blocks(self, request):
        blocks = [dict(block) for block in self.chain.node_blocks[::-1]]
        return web.json_response({'blocks': blocks})

    async def mine(self, data):
        block = self.chain.mine_block(data)
        self.chain.add_block(block)

    async def mine_handler(self, request):
        post_data = await request.post()
        self.loop.create_task(self.mine(post_data['data']))
        return web.json_response({'status': 'ok'})

    def setup_routes(self, app):
        app.router.add_route('GET', '/blocks', self.get_blocks)
        app.router.add_route('POST', '/mine', self.mine_handler)

    def get_app(self):
        app = web.Application()
        self.setup_routes(app)
        app.on_startup.append(self.on_startup)
        return app


def run_local_server():
    local_server = LocalServer()
    app = local_server.get_app()
    web.run_app(app, host='localhost', port=8888, loop=local_server.loop)
