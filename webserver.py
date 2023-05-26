from aiohttp import web

import config

topggpass = config.TOPGG_PASSWORD


async def handle_topgghook(request):
    if request.headers.get("Authorization", None) != topggpass:
        return web.Response(text="Unauthorized", status=401)
    data = await request.json()
    if data.get("type") == "upvote":
        await app.bot.on_vote(data)  # TODO: Implement the on_vote event
    else:
        await app.bot.loghook.send("Received a test vote!")
    return "success"


routes = [web.get("/", lambda request: web.Response(text="Pika!")), web.get("/topgghook", handle_topgghook)]

app = web.Application()
app.add_routes(routes)

