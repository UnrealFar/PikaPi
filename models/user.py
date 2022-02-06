import discord
from typing import List, Dict

from .pokemon import Pokemon

class User:
    __cached_users__ = dict()

    def __init__(self, payload: dict):
        self.bot = payload.pop("bot")
        self.id: int = int(payload.pop("_id"))
        self.badges: List = payload.pop("badges", [])
        self.caught: dict = payload.pop("caught", {})
        self.bal: dict = payload.pop("bal", {})
        self.votes: List = payload.pop("votes", [])
        self.__cached_users__[self.id] = self

    async def add_pokemon(self, pokemon: Pokemon) -> bool:
        acc = await self.get_account_data()
        if not acc: return False
        payload = pokemon.get_payload()
        acc["caught"]["t"] += 1
        self.caught["t"] += 1
        if pokemon.shiny:
            acc["caught"]["s"] += 1
            self.caught["s"] += 1
        r = pokemon.rarity[0]
        acc["caught"][r] += 1
        self.caught[r] += 1
        acc["bal"]["c"] += 20
        self.bal["c"] += 20
        if len(acc["pokemon"]) >= 1:
            acc["pokemon"][str(int(tuple(acc["pokemon"])[-1] )+ 1)] = payload
        else:
            acc["pokemon"]["0"] = payload
        return await self.bot.accounts.update_one({"_id": self.id}, {"$set": {"pokemon": acc["pokemon"], "caught": acc["caught"], "bal": acc["bal"]}})

    async def remove_pokemon(self, uid) -> bool:
        return await self.bot.accounts.update_one(
            {"_id": self.id},
            {"$unset": f"pokemon.{uid}"}
        ) 

    async def all_pokemon(self) -> Dict[int, Pokemon]:
        pokes = await self.get_account_data()
        pokes = pokes.get("pokemon", {})
        for p_id, poke in pokes.items():
            yield p_id, Pokemon(poke)

    async def add_bal(self, coins = None, shards: int = None):
        payload = {"$inc": {}}
        if coins:
            payload["$inc"]["bal.c"] = coins
            self.bal["c"] = self.bal["c"] + coins
        if shards:
            payload["$inc"]["bal.s"] = shards
            self.bal["s"] = self.bal["s"] + shards
        await self.bot.accounts.update_one(
            {"_id": self.id}, payload
        )

    async def get_pokemon(self, pokemon_id) -> Pokemon:
        ret = await self.get_account_data()
        if ret:
            ret = ret["pokemon"].get(str(pokemon_id))
            if ret:
                ret["bot"] = self.bot
                return await Pokemon.new_pokemon(**ret)

    async def vote(self):
        votes = self.votes
        t = discord.utils.utcnow()
        votes.append(t)
        return await self.bot.accounts.update_one(
            {"_id": self.id},
            {"$set": {"votes": votes}}
            )

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
            "bal": {"c": 100, "s": 0},
            "badges": [],
            "caught": {"t": 0, "n": 0, "m": 0, "l": 0, "u": 0, "s": 0},
            "pokemon": {},
            "votes": []
        }
        try:
            await db.insert_one(payload)
        except:
            return
        payload["bot"] = bot
        return cls(payload)



