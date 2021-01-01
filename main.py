from config import config
from yrumee import YrumeeClient

if __name__ == "__main__":
    client = YrumeeClient()
    client.run(config.bot_token)
