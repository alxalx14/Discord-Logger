import discord
from os import getenv
import ujson

from sys import stdout
from cryptography import fernet
from threading import Thread
from datetime import datetime
from src.logger import logger


def getConfig() -> dict:
    """
    Loads startup config, containing Token
    :return:
    """
    with open("configs/startup.json", "r") as f:
        return ujson.loads(f.read())


CONFIG = getConfig()


def getEncryptionKey() -> bytes:
    """
    Reads the encryption key
    :return:
    """
    with open("configs/enc.key", "rb") as enc_file:
        return enc_file.read()


def getToken() -> str:
    """
    Decrypts and returns
    the decrypted token for
    running the bot
    :return:
    """
    crypto = fernet.Fernet(getEncryptionKey())
    token_bytes = crypto.decrypt(CONFIG["token"].encode())
    return token_bytes.decode()


bot = discord.Client()


def makeAuthor(author: object) -> str:
    """
    Combines authors name
    and discriminator for
    the full username
    :param author:
    :return:
    """
    return "%s#%s" % (author.name, author.discriminator)


@bot.event
async def on_ready():
    """
    Prints when it logge in
    to the Bot/user account
    :return:
    """
    print(f"Discord Message Logger 1.0")


@bot.event
async def on_message(message):
    """
    Most importnat feature,
    gets called whenever a
    message is sent then builds
    the log structure.
    :param message:
    :return:
    """
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
    stdout.write("\rUser: %s said: %s\n\n" % (makeAuthor(message.author), msg))
    log = logger(save_data, message.id)
    Thread(
        target=log.save,
        args=(has_image,)
    ).start()

bot.run(getToken(), bot=CONFIG["bot"])

