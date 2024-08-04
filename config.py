import os

APP_ID = int(os.environ.get("APP_ID", "24248654"))
API_HASH = os.environ.get("API_HASH", "c0da9c346d2c45dbc7ec49a05da9b2b6")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7176736920:AAFXXS-RWLY36OdXrlJ54h5tnEIx_Z6vkq8")
DB_CHANNEL_ID = int(os.environ.get("DB_CHANNEL_ID", "-1001529235696"))
IS_PRIVATE = os.environ.get("IS_PRIVATE",False) # any input is ok But True preferable
OWNER_ID = int(os.environ.get("OWNER_ID", "2109732446"))
PROTECT_CONTENT = False
UPDATE_CHANNEL = os.environ.get('UPDATE_CHANNEL', 'marselbots')
AUTH_USERS = list(int(i) for i in os.environ.get("AUTH_USERS", "").split(" ")) if os.environ.get("AUTH_USERS") else []
if OWNER_ID not in AUTH_USERS:
    AUTH_USERS.append(OWNER_ID)
