import os

import pymongo


class MongoManager(object):
    """
    Singleton class to manage the MongoDB connection
    """
    _client = None
    _instance = None

    @staticmethod
    def get_db_instance() -> pymongo.database.Database:
        """
        Returns an instance of the 'reto' database
        :return:
        """
        if MongoManager._instance == None:
            MongoManager()
        return MongoManager._instance

    def __init__(self):
        if MongoManager._instance != None:
            raise Exception("This class is a singleton!")
        else:
            MongoManager._client = pymongo.MongoClient(
                os.getenv("MONGODB_URI", "mongodb://reto:Extrovert-Unbiased9-Oxidize-Recycler@localhost:27017/?authSource=reto")
            )

            MongoManager._instance = MongoManager._client.reto

