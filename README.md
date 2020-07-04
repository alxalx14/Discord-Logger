#Discord Message Logger
>Features
- Log all messages to JSON files
- Log images, files, etc to a folder
- Logs messages from servers, groups and private messages
- Uses ujson for extra speed after files get bigger
- Can be used as a bot or selfbot
- Encrypts token using Fernet and a random generated key
- Can be ran on a server for logging 24/7
>Log structure
- Identified by message ID
- Guild ID and Name(only for servers)
- Channel ID
- Timestamp
- Author and the authors discrimator + ID

>Requirements
- python 3.6+
- ujson module
- discord module
- discord bot/user authorization token

>Usage
1. Run encrypt.py to generate a key and encrypt your token.
2. Place the text printed to the screen inside configs/startup.json, in the token field.
3. Run main.py and watch it go.

>Upcoming Features
- WebPanel to manage\access logs
- Download logs directly from discord
- Statistics, avg messages/minute etc. 
- Cloud Storage using Google Drive
