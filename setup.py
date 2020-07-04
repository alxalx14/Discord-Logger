from cryptography import fernet
import json
from os import mkdir
import subprocess
import sys


with open("requirements.txt", "r") as module_file:
    for module in module_file.readlines():
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

folder_structure = [
    "logs/",
    "logs/DM/",
    "logs/Group DM/",
    "logs/Servers/",
    "logs/Files/",
    "logs/Files/C# Files/",
    "logs/Files/C++ Files/",
    "logs/Files/C Files/",
    "logs/Files/Images/",
    "logs/Files/JSON Files/",
    "logs/Files/Log Files/",
    "logs/Files/Others/",
    "logs/Files/PE Files/",
    "logs/Files/Python Files/",
    "logs/Files/Text Files/",
    "logs/Files/Torrent Files/",
    "logs/Files/XML Files/"
]

bot_choice = {
    1: False,
    2: True
}

for folder in folder_structure:
    try:
        mkdir(folder)
    except FileExistsError:
        pass
key = fernet.Fernet.generate_key()
with open("configs/enc.key", "wb") as f:
    f.write(key)

with open("configs/enc.key", "rb") as enc_file:
    enc = fernet.Fernet(enc_file.read())

token = enc.encrypt(input("Whats your token?\n> ").encode()).decode()
isBot = input("""Will this be a selfbot or a normal bot?
                [1]Self bot     [2]Normal Bot\n\r> """)

with open("configs/startup.json", "w") as config_file:
    config_data = {
        "token": token,
        "bot": bot_choice.get(int(isBot), True)
    }
    config_file.write(json.dumps(config_data))

print("""Have fun using this program!""")
