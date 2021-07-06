from config import config
from yrumee import YrumeeClient
from yrumee.storage import Storage

if __name__ == "__main__":
    client = YrumeeClient()
    client.storage = Storage.load() or Storage()
    try:
        client.run(config.bot_token)
    except Exception as e:
        print(e)
    finally:
        client.on_exit()
        client.storage.save()
