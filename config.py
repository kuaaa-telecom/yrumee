import logging
import os

import config_secrets as secrets


class Config:
    is_test_env = False

    @classmethod
    def required_get(cls, env, key):
        if cls.is_test_env:
            return ""

        v = env.get(key) or getattr(secrets, key)
        if not v:
            raise KeyError(key)
        else:
            return v

    @classmethod
    def get(cls, env, key):
        v = env.get(key) or getattr(secrets, key)
        if not v:
            logging.warn("Env[{}] not loaded.".format(key))
            return None
        else:
            return v

    def __init__(self, env, is_test_env=False):
        Config.is_test_env = is_test_env
        self.bot_token = Config.required_get(env, "BOT_TOKEN")


config = Config(os.environ)
