import os

APP_ID = int(os.environ.get("APP_ID", "13675555"))
API_HASH = os.environ.get("API_HASH", "c0da9c346d2c45dbc7ec49a05da9b2b6")
BOT_TOKEN = os.environ.get("BOT_TOKEN", 5696982423:AAE45yJTxnjhApGbtl1eZXwHSCtrG2PwAow)
DB_CHANNEL_ID = os.environ.get("-1001911775310")
IS_PRIVATE = os.environ.get("IS_PRIVATE",False) # any input is ok But True preferable
OWNER_ID = int(os.environ.get("5591954930"))
PROTECT_CONTENT = False
UPDATE_CHANNEL = os.environ.get('UPDATE_CHANNEL', '-1001721659524')
AUTH_USERS = list(int(i) for i in os.environ.get("AUTH_USERS", "").split(" ")) if os.environ.get("AUTH_USERS") else []
if OWNER_ID not in AUTH_USERS:
    AUTH_USERS.append(OWNER_ID)