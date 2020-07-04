from cryptography import fernet
import json


key = fernet.Fernet.generate_key()
with open("configs/enc.key", "wb") as f:
    f.write(key)
    
with open("configs/enc.key", "rb") as enc_file:
    enc = fernet.Fernet(enc_file.read())

token = enc.encrypt(input("Whats your token?\n> ").encode()).decode()
with open("configs/startup.json", "w") as config_file:
    config_file.write(json.dumps({"token": token}))

print("""If you do not see a logs folder, run setup.py as it will install
        all required modules and setup the log structure""")