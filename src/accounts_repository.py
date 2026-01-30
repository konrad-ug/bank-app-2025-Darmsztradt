from abc import ABC, abstractmethod
from pymongo import MongoClient
import os


class AccountsRepository(ABC):
    @abstractmethod
    def save_all(self, accounts):
        pass

    @abstractmethod
    def load_all(self):
        pass


class MongoAccountsRepository(AccountsRepository):
    def __init__(self, connection_string=None, database_name="bank", collection_name="accounts"):
        if connection_string is None:
            connection_string = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
        self._client = MongoClient(connection_string)
        self._db = self._client[database_name]
        self._collection = self._db[collection_name]

    def save_all(self, accounts):
        self._collection.delete_many({})
        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()},
                upsert=True,
            )

    def load_all(self):
        return list(self._collection.find({}))

    def clear(self):
        self._collection.delete_many({})
