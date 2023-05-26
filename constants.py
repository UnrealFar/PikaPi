from enum import Enum

LANGUAGE_EMOJIS = {
    "name_en": ":flag_gb:",
    "name_ja": ":flag_jp:",
    "name_jar": ":flag_jp:",
    "name_jat": ":flag_jp:",
    "name_de": ":flag_de:",
    "name_fr": ":flag_fr:",
}

REGIONS = [
    "kanto",
    "johto",
    "hoenn",
    "sinnoh",
    "unova",
    "kalos",
    "alola",
    "galar",
]


class STARTERS(Enum):
    Bulbasaur = 1
    Charmander = 4
    Squirtle = 7
    Chikorita = 152
    Cyndaquil = 155
    Totodile = 158
    Treecko = 252
    Torchic = 255
    Mudkip = 258
    Turtwig = 387
    Chimchar = 390
    Piplup = 393
    Snivy = 495
    Tepig = 498
    Oshawott = 501
    Chespin = 650
    Fennekin = 653
    Froakie = 656
    Rowlet = 722
    Litten = 725
    Popplio = 728
    Grookey = 810
    Scorbunny = 813
    Sobble = 816


STATS = {
    "hp": "HP",
    "atk": "Attack",
    "defn": "Defense",
    "satk": "Special Attack",
    "sdef": "Special Defense",
    "spd": "Speed",
}

NATURES = (
    "Adamant",
    "Bashful",
    "Bold",
    "Brave",
    "Calm",
    "Careful",
    "Docile",
    "Gentle",
    "Hardy",
    "Hasty",
    "Impish",
    "Jolly",
    "Lax",
    "Lonely",
    "Mild",
    "Modest",
    "Naive",
    "Naughty",
    "Quiet",
    "Quirky",
    "Rash",
    "Relaxed",
    "Sassy",
    "Serious",
    "Timid",
)

NATURE_MULTIPLIERS = {
    "Hardy": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 1,
        "sdef": 1,
        "spd": 1,
    },
    "Lonely": {
        "hp": 1,
        "atk": 1.1,
        "def": 0.9,
        "satk": 1,
        "sdef": 1,
        "spd": 1,
    },
    "Brave": {
        "hp": 1,
        "atk": 1.1,
        "def": 1,
        "satk": 1,
        "sdef": 1,
        "spd": 0.9,
    },
    "Adamant": {
        "hp": 1,
        "atk": 1.1,
        "def": 1,
        "satk": 0.9,
        "sdef": 1,
        "spd": 1,
    },
    "Naughty": {
        "hp": 1,
        "atk": 1.1,
        "def": 1,
        "satk": 1,
        "sdef": 0.9,
        "spd": 1,
    },
    "Bold": {
        "hp": 1,
        "atk": 0.9,
        "def": 1.1,
        "satk": 1,
        "sdef": 1,
        "spd": 1,
    },
    "Docile": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 1,
        "sdef": 1,
        "spd": 1,
    },
    "Relaxed": {
        "hp": 1,
        "atk": 1,
        "def": 1.1,
        "satk": 1,
        "sdef": 1,
        "spd": 0.9,
    },
    "Impish": {
        "hp": 1,
        "atk": 1,
        "def": 1.1,
        "satk": 0.9,
        "sdef": 1,
        "spd": 1,
    },
    "Lax": {
        "hp": 1,
        "atk": 1,
        "def": 1.1,
        "satk": 1,
        "sdef": 0.9,
        "spd": 1,
    },
    "Timid": {
        "hp": 1,
        "atk": 0.9,
        "def": 1,
        "satk": 1,
        "sdef": 1,
        "spd": 1.1,
    },
    "Hasty": {
        "hp": 1,
        "atk": 1,
        "def": 0.9,
        "satk": 1,
        "sdef": 1,
        "spd": 1.1,
    },
    "Serious": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 1,
        "sdef": 1,
        "spd": 1,
    },
    "Jolly": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 0.9,
        "sdef": 1,
        "spd": 1.1,
    },
    "Naive": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 1,
        "sdef": 0.9,
        "spd": 1.1,
    },
    "Modest": {
        "hp": 1,
        "atk": 0.9,
        "def": 1,
        "satk": 1.1,
        "sdef": 1,
        "spd": 1,
    },
    "Mild": {
        "hp": 1,
        "atk": 1,
        "def": 0.9,
        "satk": 1.1,
        "sdef": 1,
        "spd": 1,
    },
    "Quiet": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 1.1,
        "sdef": 1,
        "spd": 0.9,
    },
    "Bashful": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 1,
        "sdef": 1,
        "spd": 1,
    },
    "Rash": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 1.1,
        "sdef": 0.9,
        "spd": 1,
    },
    "Calm": {
        "hp": 1,
        "atk": 0.9,
        "def": 1,
        "satk": 1,
        "sdef": 1.1,
        "spd": 1,
    },
    "Gentle": {
        "hp": 1,
        "atk": 1,
        "def": 0.9,
        "satk": 1,
        "sdef": 1.1,
        "spd": 1,
    },
    "Sassy": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 1,
        "sdef": 1.1,
        "spd": 0.9,
    },
    "Careful": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 0.9,
        "sdef": 1.1,
        "spd": 1,
    },
    "Quirky": {
        "hp": 1,
        "atk": 1,
        "def": 1,
        "satk": 1,
        "sdef": 1,
        "spd": 1,
    },
}
