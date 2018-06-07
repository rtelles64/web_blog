__author__ = "Roy Telles Jr"

import pymongo

class Database:
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod # tells Python we're not going to be using "self" in this method because this method only belongs
                  # to the Database class as a whole, and never to an instance of a Database
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["fullstack"]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query) # returns Cursor object

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query) # gets first element that gets returned by the Cursor
