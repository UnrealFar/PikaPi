from typing import List
import math, numpy, random, io
from helper import new_token
import discord, asyncio

async def gen_stats(base_stats, level, iv) -> dict:
    ret = {}
    hp = (0.01 * (2 * float(base_stats["hp"]) + iv + 1) * level)
    ret["hp"] = math.floor(hp) + level + 10
    for s in base_stats:
        x = (0.01 * (2 * float(base_stats[s]) + iv + 1) * level + 5)
        x = math.floor(x)
        ret[s] = x
    return ret

async def gen_level() -> float:
    return round(random.uniform(4.9, 39.9), 1)

async def gen_iv(loop) -> float:
    opts = {
        "a": (1.01, 7.74),
        "b": (4.45, 14.73),
        "c": (13.33, 24.06),
        "d": (23.65, 47.56),
        "e": (40.92, 57.45),
        "f": (54.33, 69.42),
        "g": (67.56, 84.03),
        "h": (81.09, 93.31),
        "j": (91.93, 96.1),
        "k": (95.01, 99.99)
    }
    per = await loop.run_in_executor(
        None,
        numpy.random.choice,
        list(opts),
        None,
        True,
        [
            0.0001, 0.0009, 0.009, 0.4, 0.5, 0.072, 0.012, 0.005, 0.0009, 0.0001
        ]
    )
    return round(random.uniform(*(opts[per])), 2)

class Pokemon:
    __slots__ = (
        "id",
        "dex",
        "slug",
        "names",
        "types",
        "base_stats",
        "stats",
        "rarity",
        "region",
        "shiny",
        "appearance",
        "iv",
        "level",
        "created",
        "bot",
        "owner",
        "event",
        "img",
        "simg"
    )

    def __init__(
        self,
        payload: dict
    ):
        self.id: int = payload.pop("_id", None)
        self.dex: int = payload.pop("dex", None)
        self.slug: str = payload.pop("slug", None)
        self.names: dict[str, str] = {
            "en": payload.pop("name_en", None),
            "ja": payload.pop("name_ja", None),
            "jar": payload.pop("name_jar", None),
            "de": payload.pop("name_de", None),
            "fr": payload.pop("name_fr", None)
        }
        self.types: List[str] = payload.pop("types", [])
        self.rarity: str = payload.pop("rarity", None)
        self.region: str = payload.pop("region", None)
        self.appearance: dict[str, str] = payload.pop("appearance", None)
        self.base_stats: dict = payload.pop("stats", None)
        self.stats: dict = payload.pop("sstats", None)
        self.shiny: bool = payload.pop("shiny", False)
        self.iv: float = payload.pop("iv", None)
        self.level: float = payload.pop("level", None)
        self.created = payload.pop("created", discord.utils.utcnow())
        if "event" in payload:
            self.event: bool = payload.pop("event")
        self.bot = payload.pop("bot", None)
        if "img" in payload:
            self.img = payload.pop("img")
        if "simg" in payload:
            self.simg = payload.pop("simg")

    async def get_image(self) -> discord.File:
        if not getattr(self, "img", None):
            if not self.shiny:
                imgdata = await self.bot.session.get(
                f"https://raw.githubusercontent.com/poketwo/data/master/images/{self.dex}.png"
        )
            else:
                imgdata = await self.bot.session.get(
                f"https://raw.githubusercontent.com/poketwo/data/master/shiny/{self.dex}.png"
            )
        else:
            imgdata = await self.bot.session.get(self.img)
        imgbytes = io.BytesIO(await imgdata.content.read())
        return discord.File(imgbytes, filename = "pokemon.png")

    def get_payload(self) -> dict:
        ret = {}
        dont = ("base_stats", "_id", "stats", "bot", "simg")
        for slot in self.__slots__:
            if slot not in dont:
                if hasattr(self, slot):
                    ret[slot] = getattr(self, slot)
        ret["_id"] = self.id
        ret["stats"] = self.stats
        ret["tk"] = new_token(self.id)
        if self.shiny:
            ret["img"] = self.simg
        return ret

    @classmethod
    async def new_pokemon(cls: "Pokemon", **payload) -> "Pokemon":
        if "iv" in payload:
            iv = payload["iv"]
        else:
            iv = await gen_iv(payload["bot"].loop)
            payload["iv"] = iv
        if "level" in payload:
            lvl = payload["level"]
        else:
            lvl = await gen_level()
            payload["level"] = lvl
        payload["sstats"] = await gen_stats(payload.get("stats"), lvl, iv)
        return cls(payload)
        
