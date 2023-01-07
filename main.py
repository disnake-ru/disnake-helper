from os import getenv
from dotenv import load_dotenv

from core import DisnakeBot

load_dotenv()

if __name__ == "__main__":
    bot = DisnakeBot()
    bot.i18n.load("./localization")
    bot.load_extensions()
    bot.run(getenv("TOKEN"))
