'''
import os

import pymongo
from dotenv import load_dotenv

load_dotenv()

# DON'T LOAD MONGODB IF YOU DON'T HAVE TO (WE DON'T RIGHT NOW)

MONGODB = os.environ["MONGODB"]
client = pymongo.MongoClient(MONGODB)
database = client["main"]

users = database["users"]
guilds = database["guilds"]
pokemon = database["pokemon"]
'''
