from aiohttp import web, WSMsgType


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['peers'].append(ws)
    print('new peer connected')

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                print(msg.data)
                #await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception {}'.format(
                ws.exception()))

    request.app['peers'].remove(ws)
    return ws
