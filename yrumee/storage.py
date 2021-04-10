
import os
import logging
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

    def __init__(self):
        self.logger.warning("First load")
        self.initialize_if_not_exists()

    def of(self, server_id: str):
        if server_id not in self.instances:
            self.instances[server_id] = StorageInstance()
        return self.instances[server_id]

    def initialize_if_not_exists(self):
        if not hasattr(self, "instances"):
            self.instances = {}

    def save(self):
        pickle.dump(self, open(self.storage_path, "wb"))
        self.logger.info("saved.")

    @classmethod
    def load(cls):
        try:
            ss = pickle.load(open(cls.storage_path, "rb"))
            ss.initialize_if_not_exists()
            return ss
        except:
            return None

