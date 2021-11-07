import logging
import os
import pickle
from collections import defaultdict
from typing import Any, Dict


class StorageInstance:
    def get(self, key: str, default_value: Any) -> Any:
        if hasattr(self, key):
            return getattr(self, key, None)
        else:
            setattr(self, key, default_value)
            return default_value


class Storage:
    logger = logging.getLogger("storage")
    storage_path = os.path.join(os.getcwd(), ".storage")

    instances: Dict[str, StorageInstance]

    @property
    def latest_version(self):
        return 3

    def __init__(self):
        self.logger.warning("First load")
        self.__version__ = self.latest_version
        self.initialize_if_not_exists()

    def of(self, server_id: str):
        _server_id = str(server_id)
        if _server_id not in self.instances:
            self.instances[_server_id] = StorageInstance()
        return self.instances[_server_id]

    def initialize_if_not_exists(self):
        if not hasattr(self, "instances"):
            self.instances = {}

    def save(self):
        pickle.dump(self, open(self.storage_path, "wb"))
        self.logger.info("saved.")

    @classmethod
    def migrate_if_needed(cls, storage):
        storage_version = getattr(storage, "__version__", 1)
        if storage.latest_version > storage_version:
            for instance in storage.instances.values():
                cls.migrate(instance, storage.latest_version, storage_version)
            storage.version = storage.latest_version

    @classmethod
    def migrate(cls, instance: StorageInstance, version_to: int, version_from: int):
        cls.logger.info("migrate: {} -> {}".format(version_from, version_to))
        if version_to == 2:
            # migration for e15afb376421b19bc721f45344af7cb03aa91204
            for key in ["breakfast", "lunch", "dinner", "yasik", "diet", "on_diet", "GM", "cardDB", "EXCardDB", "SSRCardDB", "SRCardDB", "RCardDB", "users"]:
                maybe_list = instance.get(key, None)
                if type(maybe_list) is list:
                    setattr(instance, key, set(maybe_list))
        elif version_to == 3:
            # migration for 1f74b0a9d43cf8b62b8f805a3927d446f8c4fee5
            for key in [
                "cardDB",
                "EXCardDB",
                "SSRCardDB",
                "SRCardDB",
                "RCardDB",
            ]:
                val = instance.get(key, None)
                if val is None:
                    setattr(instance, key, set())
            maybe_users = instance.get("users", None)
            if maybe_users is None:
                setattr(instance, maybe_users, {})
        else:
            pass

    @classmethod
    def load(cls):
        try:
            ss = pickle.load(open(cls.storage_path, "rb"))
            ss.initialize_if_not_exists()
            ss.migrate_if_needed(ss)
            return ss
        except:
            return None
