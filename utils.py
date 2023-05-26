import base64
import json
import time


def create_secret_key(discord_id: int, /) -> str:
    t = (str(discord_id) + "|" + str(time.time()).replace(".", "")).encode()
    return base64.a85encode(base64.b64encode(t)).decode()


def decode_secret_key(key: str) -> int:
    t = base64.b64decode(base64.a85decode(key.encode()))
    return t.decode().split("|")[0]


async def backup_species(db):
    with open("species_backup.json", "w") as bkp:
        td = {"species": []}
        for species in await db.Species.all():
            y = {"image_url": f"https://raw.githubusercontent.com/poketwo/data/master/images/{species.id}.png"}
            td["species"].append(
                {
                    **{
                        x: getattr(species, x)
                        for x in "id,name,description,height,weight,types,abilities,moves,hp,attack,defense,special_attack,special_defense,speed,rarity,capture_rate".split(
                            ","
                        )
                    },
                    **y,
                }
            )
        json.dump(td, bkp)
