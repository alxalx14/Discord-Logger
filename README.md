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

>Upcoming Features
- WebPanel to manage\access logs
- Download logs directly from discord
- Statistics, avg messages/minute etc. 
