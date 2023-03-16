import os
import traceback

import disnake
from disnake.ext import commands

from .mongodb import MongoDB


class DisnakeBot(commands.InteractionBot):
    def __init__(self):
        super().__init__(
            intents=disnake.Intents.all()
        )

    def load_extensions(self):
        for filename in os.listdir("./extensions"):
            if filename.endswith(".py"):
                try:
                    self.load_extension(f"extensions.{filename[:-3]}")
                except Exception as e:
                    traceback.format_exc(e)
