from yrumee.storage import Storage
from config import config
from yrumee import YrumeeClient

if __name__ == "__main__":
    client = YrumeeClient()
    client.storage = Storage.load() or Storage()
    client.run(config.bot_token)
    client.storage.save()
