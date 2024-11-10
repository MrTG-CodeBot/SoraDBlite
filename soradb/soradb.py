import pymongo
from pymongo import MongoClient

class Soradb:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.sora = pymongo

    def connect(self, db_url, db_password, db_collection):
        try:
            self.client = pymongo.MongoClient(db_url)
            self.db = self.client[db_password]
            self.collection = self.db[db_collection]
            print("Connected to MongoDB database successfully.")
        except Exception as e:
            print(f"Error occurred: {e}")

    def drop_collection(self, collection_name):
        try:
            collection = self.db[collection_name]
            collection.drop()
            print(f"Collection '{collection_name}' dropped successfully.")
        except Exception as e:
            print(f"Error dropping collection '{collection_name}': {e}")

    # Basic CRUD Operations
    def insert_one(self, document):
        result = self.collection.insert_one(document)
        return result.inserted_id

    def insert_many(self , documents):
        result = self.collection.insert_many(documents)
        return result.inserted_ids

    def find_one(self, query={}):
        result = self.collection.find_one(query)
        return result

    def find_many(self, query={}, projection={}):
        results = self.collection.find(query, projection)
        return list(results)

    def update_one(self, filter, update):
        result = self.collection.update_one(filter, update)
        return result.modified_count

    def delete_one(self, filter):
        result = self.collection.delete_one(filter)
        return result.deleted_count

    def update_many(self, filter, update):
        result = self.collection.update_many(filter, update)
        return result.modified_count

    def delete_one(self, filter):
        result = self.collection.delete_one(filter)
        return result.deleted_count

    def delete_many(self, filter):
        result = self.collection.delete_many(filter)
        return result.deleted_count

    def find(self, query={}, projection={}, sort=None, limit=None):
        cursor = self.collection.find(query, projection)

        if sort:
            if isinstance(sort, dict):
                cursor = cursor.sort(sort)
            elif isinstance(sort, list):
                cursor = cursor.sort(sort)
            else:
                raise ValueError("Sort parameter must be a dict or list")

        if limit:
            cursor = cursor.limit(limit)

        return list(cursor)

    def sort_by(self , sort_key , ascending=True):
        sort_order = pymongo.ASCENDING if ascending else pymongo.DESCENDING
        results = self.collection.find().sort([(sort_key , sort_order)])
        return list(results)

    def count(self , query={}):
        return self.collection.count_documents(query)

    def fetch_values_by_key(self , key_name):
        values = []
        for document in self.collection.find():
            if key_name in document:
                values.append(document[key_name])
        return values
