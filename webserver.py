from quart import Quart

app = Quart("PikaPi")


@app.route("/")
async def home():
    return "Pika!"

