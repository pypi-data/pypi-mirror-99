from pymongo import MongoClient
import pymongo.collection
from datetime import datetime
import logging
import time
from contextlib import contextmanager
import os


class NoUserException(Exception):
    pass


class User(dict):
    def __init__(self, coll: pymongo.collection.Collection, query: dict):
        self.coll = coll
        data = self.coll.find_one_and_update(
            query, {"$set": {"last_login": datetime.utcnow(), "logged_in": True}}, sort=[("last_login", 1)]
        )
        if not data:
            raise NoUserException(f"Didnt get any user from db ({self.coll}) using query {query}")
        super().__init__(data)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.coll.find_one_and_update({"_id": self["_id"]}, {"$set": {key: value}})


class MongoReader:
    def __init__(self, uri=None, database=None, collection=None, filters=[]):
        uri = uri or os.environ["LOCUST_MONGO"]
        database = database or os.environ["LOCUST_MONGO_DATABASE"]
        collection = collection or os.environ["LOCUST_MONGO_COLLECTION"]
        self.coll = MongoClient(uri)[database][collection]
        self.filters = filters
        self.reduced_filters = []
        self.delay_warning = 0
        self.query = {"$and": filters + [{"logged_in": False}]}

    @contextmanager
    def user(self):
        start_at = time.monotonic()
        user = User(self.coll, self.query)

        if start_at + self.delay_warning < time.monotonic():
            if not self.delay_warning:
                # dont warn on first query, just set the threshold
                self.delay_warning = 1
            else:
                logging.warning(
                    f"Getting a user with filter more than {self.delay_warning} seconds (doubling warning threshold for next time, filter used was {self.filters})"
                )
                self.delay_warning *= 2
        try:
            yield user
        finally:
            releasessn = self.coll.find_one_and_update(
                {"_id": user["_id"]},
                {"$set": {"logged_in": False}},
            )
        if releasessn is None:
            raise Exception(f"Couldnt release lock for user: {user}")
