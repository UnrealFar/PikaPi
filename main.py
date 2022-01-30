import bot
import os

pikapi = bot.PikaPi()
pikapi.run(os.environ.get("token"))
