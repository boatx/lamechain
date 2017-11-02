from aiohttp import web

from lamechain.chain import Chain


class LocalClient:
    def __init__(self):
        self.chain = None

    def on_startup(self, app):
        self.chain = Chain()
        self.chain.sync()

    async def get_blocks(self, request):
        blocks = [dict(block) for block in self.chain.node_blocks]
        return web.json_response({'blocks': blocks})

    async def mine(self, request):
        block = self.chain.mine_block(data='test')
        self.chain.add_block(block)
        return web.json_response(dict(block))


def setup_app():
    local_handler = LocalClient()
    app = web.Application()
    app.router.add_route('GET', '/blocks', local_handler.get_blocks)
    app.router.add_route('GET', '/mine', local_handler.mine)
    app.on_startup.append(local_handler.on_startup)
    return app


def main():
    app = setup_app()
    web.run_app(app, host='localhost', port=8888)


if __name__ == "__main__":
    main()
