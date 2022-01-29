import discord
from .pokemon import Pokemon

class User:
    __cached_users__ = dict()

    def __init__(self, payload: dict):
        self.bot = payload.pop("bot")
        self.id: int = int(payload.pop("_id"))
        self.__cached_users__[self.id] = self

    async def add_pokemon(self, pokemon: Pokemon) -> bool:
        acc = await self.get_account_data()
        if not acc: return False
        payload = pokemon.get_payload()
        db = self.bot.accounts
        acc["caught"]["t"] = acc["caught"]["t"] + 1
        if pokemon.shiny:
            acc["caught"]["s"] = acc["caught"]["s"] + 1
        r = pokemon.rarity[0]
        acc["caught"][r] = acc["caught"][r] + 1
        if len(acc["pokemon"]) >= 1:
            acc["pokemon"][str(int(list(acc["pokemon"])[-1]) + 1)] = payload
        else: acc["pokemon"]["0"] = payload
        await db.update_one({"_id": self.id}, {"$set": {"pokemon": acc["pokemon"], "caught": acc["caught"]}})
        return True

    async def remove_pokemon(self, uid) -> bool:
        data = await self.get_account_data()
        if not data: return False
        for p in data["pokemon"]:
            if p.get("_id") == uid:
                del data["pokemon"][p]
                await self.bot.accounts.update_one({"_id": self.id}, {"$set": data})
                return True

    async def get_account_data(self) -> dict:
        return await self.bot.accounts.find_one({"_id": self.id})

    @classmethod
    def get_account(cls: "User", payload):
        e = cls.__cached_users__.get(payload.get("_id"))
        if e:
            return e
        return cls(payload)

    @classmethod
    async def create_account(cls: "User", bot, uid: int):
        db = bot.accounts
        payload = {
            "_id": uid,
            "token": bot.helper.new_token(uid),
            "created": discord.utils.utcnow(),
            "bal": 100,
            "badges": [],
            "caught": {"t": 0, "n": 0, "m": 0, "l": 0, "u": 0, "s": 0},
            "pokemon": {}
        }
        await db.insert_one(payload)
        payload["bot"] = bot
        return cls(payload)



