from __future__ import annotations

import datetime
import math
import random

from tortoise import fields
from tortoise.models import Model

import constants


def get_type_emoji(type_: str, /) -> str:
    """Returns the respective emoji for a pokemon type"""
    return {
        "bug": "<:Bug:1110880284846604300>",
        "dark": "<:Dark:1110880288231395331>",
        "dragon": "<:Dragon:1110880274398588969>",
        "electric": "<:Electric:1110880276269252668>",
        "fairy": "<:Fairy:1110880271173169222>",
        "fighting": "<:Fighting:1110880291628793906>",
        "fire": "<:Fire:1110880266903375972>",
        "flying": "<:Flying:1110880293495255163>",
        "ghost": "<:Ghost:1110882263979274352>",
        "grass": "<:Grass:1110880305335775312>",
        "ground": "<:Ground:1110880283022074017>",
        "ice": "<:Ice:1110880302370394124>",
        "normal": "<:Normal:1110880264655220776>",
        "poison": "<:Poison:1110881571893936159>",
        "psychic": "<:Psychic:1110880296938778625>",
        "rock": "<:Rock:1110880279616311356>",
        "steel": "<:Steel:1110880300575248384>",
        "water": "<:Water:1110880261413023794>",
    }.get(type_, "")


class Species(Model):
    id = fields.IntField(pk=True)
    dex = fields.IntField()
    name_en = fields.TextField(null=True)
    name_ja = fields.TextField(null=True)
    name_jar = fields.TextField(null=True)
    name_jat = fields.TextField(null=True)
    name_de = fields.TextField(null=True)
    name_fr = fields.TextField(null=True)
    description = fields.TextField(default="")
    height = fields.IntField(default=0)
    weight = fields.IntField(default=0)
    region = fields.IntField()
    types = fields.TextField(default="0")
    abilities = fields.TextField(default="0")
    moves = fields.TextField(default="0")
    hp = fields.IntField(default=0)
    attack = fields.IntField(default=0)
    defense = fields.IntField(default=0)
    special_attack = fields.IntField(null=True)
    special_defense = fields.IntField(null=True)
    speed = fields.IntField(default=0)
    rarity = fields.IntField(default=0)
    capture_rate = fields.IntField(default=0)
    temp_evolution = fields.IntField(default=None, null=True)
    temp_evolved = fields.BooleanField(defualt=False)
    image_url = fields.TextField(default=None, null=True)
    shiny_image_url = fields.TextField(default=None, null=True)

    async def catch(self, owner: Account, shiny=False):
        lvl = random.randint(5, 40)
        cid = len(await Pokemon.filter(owner=owner)) + 1

        ret = await Pokemon.create(
            cid=cid,
            nick=None,
            owner=owner,
            species=self,
            level=lvl,
            iv_hp=random.randint(1, 31),
            iv_atk=random.randint(1, 31),
            iv_def=random.randint(1, 31),
            iv_satk=random.randint(1, 31),
            iv_sdef=random.randint(1, 31),
            iv_speed=random.randint(1, 31),
            lmoves="0",
            exp=1.25 * (lvl**3),
            shiny=shiny,
            nature=random.choice(constants.NATURES),
        )

        return ret


class Account(Model):
    id = fields.BigIntField(pk=True)
    balance = fields.IntField(default=0)
    shards = fields.IntField(default=0)
    selected_id = fields.IntField(default=0)
    battles_won = fields.IntField(default=0)
    battles_lost = fields.IntField(default=0)
    shiny_hunt = fields.BigIntField(default=0)
    shiny_streak = fields.IntField(default=0)
    suspended = fields.BooleanField(default=False)
    suspended_until = fields.DatetimeField(default=datetime.datetime.min)
    suspension_reason = fields.TextField(default="")
    last_voted = fields.DatetimeField(default=datetime.datetime.min)
    vote_total = fields.IntField(default=0)
    vote_rewards = fields.IntField(default=0)
    created_at = fields.DatetimeField(null=False)


class Pokemon(Model):
    uid = fields.UUIDField(pk=True)
    cid = fields.BigIntField(null=False)
    nick = fields.TextField(null=True)
    species: fields.ForeignKeyRelation[Species] = fields.ForeignKeyField(
        "models.Species",
        related_name="Species",
    )
    owner: fields.ForeignKeyRelation[Account] = fields.ForeignKeyField(
        "models.Account",
        related_name="Account",
    )
    nature = fields.TextField(null=False)
    level = fields.IntField(default=0)
    exp = fields.BigIntField(default=0)
    iv_hp = fields.IntField(default=0)
    iv_atk = fields.IntField(default=0)
    iv_def = fields.IntField(default=0)
    iv_satk = fields.IntField(default=0)
    iv_sdef = fields.IntField(default=0)
    iv_spd = fields.IntField(default=0)
    lmoves = fields.IntField(default=0)
    temp_evolved = fields.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def get_stat(self, stat: str):
        b = getattr(self.species, stat, 0)
        iv = getattr(self, "iv_" + stat)
        return math.floor(((2 * b + iv + 5) * self.level // 100 + 5) * constants.NATURE_MULTIPLIERS[self.nature][stat])

    @property
    def iv(self):
        return sum(self.iv_hp, self.iv_atk, self.iv_def, self.iv_satk, self.iv_sdef, self.iv_spd) / 6


class Uncaught(Model):
    channel_id = fields.BigIntField(pk=True)
    species_id = fields.IntField()


class Incense(Model):
    channel_id = fields.BigIntField(pk=True)
    guild_id = fields.BigIntField(null=False)
    remaining = fields.BooleanField(null=False)


__models__ = (
    Account,
    Species,
    Pokemon,
    Uncaught,
    Incense,
)
