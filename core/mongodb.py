import os

import certifi
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        self.connection: MongoClient = MongoClient(
            os.getenv("MONGO_URL"),
            tlsCAFile=certifi.where()
        )["disnake"]

    def update_guild_data(self, prefix: str, data: dict):
        collcetion = self.connection["983119421214187520"]["settings"]
        collcetion.update_one({"_id": "settings"}, {prefix: data}, upsert=True)

    def get_guild_data(self):
        return self.connection["983119421214187520"]["settings"]

    def check_tag(self, name: str):
        data = self.connection["983119421214187520"]["settings"].find_one(
            {'_id': 'settings'}
        )

        try:
            if data["tag_system"][name]:
                return None
        except KeyError:
            return True

    def get_tag(self, name: str):
        data = self.connection["983119421214187520"]["settings"].find_one(
            {'_id': 'settings'}
        )

        try:
            if data["tag_system"][name]:
                return data["tag_system"][name]
        except KeyError:
            return None
