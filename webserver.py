from quart import Quart, request, abort
import os

app = Quart("PikaPi")

topggpass = os.environ.get("topggpass")

@app.route("/")
async def home():
    return "Pika!"

@app.route("/topgghook", methods = ["POST"])
async def topgghook():
    print("hahayes")
    if request.headers.get("Authorization") != topggpass:
        abort(401)
    data = await request.get_json(force = True)
    if data.get("type") == "upvote":
        await app.bot.on_vote(data)
    else:
        await app.bot.loghook.send("Received a test vote!")
    return "success"
