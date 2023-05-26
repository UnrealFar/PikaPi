# import require # comment this out if u already have the requirements installed else uncomment it
import contextlib
import asyncio
import logging
from logging import handlers as _handlers

import discord
import jishaku

import bot

try:
    import uvloop
except ImportError:
    pass
else:
    uvloop.install()

log = logging.getLogger()
pikapi = bot.PikaPi()

async def main():
   await pikapi.start(pikapi.config.TOKEN)


jishaku.Flags.HIDE = True
jishaku.Flags.RETAIN = True
jishaku.Flags.NO_UNDERSCORE = True


@contextlib.contextmanager
def setup_logging():
    try:
        discord.utils.setup_logging()
        # __enter__
        max_bytes = 32 * 1024 * 1024  # 32 MiB

        if pikapi.config.LOGGER_ON_DEBUG:
            logging.getLogger("discord").setLevel(logging.DEBUG)
            log.setLevel(logging.DEBUG)
        else:
            logging.getLogger("discord").setLevel(logging.INFO)
            log.setLevel(logging.INFO)

        handler = _handlers.RotatingFileHandler(
            filename="pikapi.log", encoding="utf-8", mode="w", maxBytes=max_bytes, backupCount=5
        )
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        fmt = logging.Formatter("[{asctime}] [{levelname:<7}] {name}: {message}", dt_fmt, style="{")
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        # __exit__
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)


#with setup_logging():
if __name__ == "__main__":
    asyncio.run(main())
