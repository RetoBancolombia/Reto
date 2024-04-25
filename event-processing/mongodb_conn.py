import os

import pymongo


class MongoManager(object):
    """
    Singleton class to manage the MongoDB connection
    """
    __client = None
    __instance = None

    @staticmethod
    def get_db_instance() -> pymongo.database.Database:
        """
        Returns an instance of the 'reto' database
        :return:
        """
        if MongoManager.__instance == None:
            MongoManager()
        return MongoManager.__instance

    def __init__(self):
        if self.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.__client = pymongo.MongoClient(
                os.getenv("MONGO_URI", "mongodb://root:root@localhost:27017/")
            )

            self.__instance = self.__client.reto

