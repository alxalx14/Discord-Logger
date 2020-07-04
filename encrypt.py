from cryptography import fernet


key = fernet.Fertnet.generate_key()

with open("configs/enc.key", "w") as f:
    f.write(key)

with open("configs/enc.key", "rb") as f:
    enc = fernet.Fernet(f.read())

token = input("Whats your token?\n> ").encode()
print("Store this in the startup.json: ", enc.encrypt(token))
