import discord
from os import getenv
import ujson

from cryptography import fernet
from threading import Thread
from datetime import datetime
from src.logger import logger


def getConfig() -> dict:
    with open("configs/startup.json", "r") as f:
        return ujson.loads(f.read())


CONFIG = getConfig()


def getEncryptionKey() -> bytes:
    with open("configs/enc.key", "rb") as enc_file:
        return enc_file.read()


def getToken() -> str:
    crypto = fernet.Fernet(getEncryptionKey())
    token_bytes = crypto.decrypt(CONFIG["token"].encode())
    return token_bytes.decode()


bot = discord.Client()


def makeAuthor(author: object) -> str:
    return "%s#%s" % (author.name, author.discriminator)


@bot.event
async def on_ready():
    print(f"Discordius is online!")


@bot.event
async def on_message(message):
    if message.author == bot.user or message is None:
        return
    msg = message.clean_content if not message.attachments else message.attachments[0].url
    save_data = {
        message.id: {
            "guild": {
                "id": message.guild.id if message.guild else None,
                "name": message.guild.name if message.guild else None,
                "channel": {
                    "id": message.channel.id,
                }
            },
            "author": {
                "name": makeAuthor(message.author),
                "id": message.author.id
            },
            "message": {
                "type": str(message.channel.type),
                "content": msg
            },
            "time_stamp": f"{datetime.now()}"
        }
    }
    has_image = False if "http" not in msg else True
    print("\x1b[95mUser\x1b[97m: \x1b[96m%s \x1b[95msaid\x1b[97m:\x1b[96m %s" % (makeAuthor(message.author), msg))
    log = logger(save_data, message.id)
    Thread(
        target=log.save,
        args=(has_image,)
    ).start()

bot.run(getToken(), bot=False)
