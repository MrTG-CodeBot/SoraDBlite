import pymongo
from pymongo import MongoClient

class SoraDBLiteError(Exception):
    """
    Custom exception for SoraDBlite errors.

    Attributes:
        message (str): The error message.
    """

    def __init__(self, message):
        super().__init__(message)

class SoraDBlite:
    def __init__(self):
        # Initialize the MongoDB client, database, collection, and set up pymongo reference
        self.client = None
        self.db = None
        self.collection = None
        self.sora = pymongo

    def check_url(self, url):
        """
        Checks the MongoDB connection URL.

        Args:
            url (str): The MongoDB connection URL.

        Returns:
            MongoClient: The MongoDB client if the connection is successful, otherwise None.
        """
        try:
            client = MongoClient(url)
            client.admin.command("ping")
            return client
        except pymongo.errors.PyMongoError as e:
            print(f"Connection error: {e}")
            return None

    def connect(self, db_url, db_password, db_collection):
        """
        Establishes a connection to the MongoDB server and selects the database and collection.

        Args:
            db_url (str): The MongoDB connection string URL.
            db_password (str): The database name to connect to.
            db_collection (str): The collection name to use within the database.

        Raises:
            SoraDBLiteError: If the connection fails.
        """
        try:
            self.client = self.check_url(db_url)
            if self.client is None:
                raise SoraDBLiteError(f"Failed to connect to MongoDB: {db_url}")

            self.db = self.client[db_password]
            self.collection = self.db[db_collection]
            print("Connected to MongoDB database successfully.")
        except Exception as e:
            raise SoraDBLiteError(f"Error connecting to MongoDB: {e}")

    def drop_collection(self , collection_name):
        """
        Drop the specified collection from the database.

        Parameters:
        collection_name (str): The name of the collection to be dropped.
        Raises:
            SoraDBLiteError: If the dropping fails.
        """
        try:
            collection = self.db[collection_name]
            collection.drop()
            print(f"Collection '{collection_name}' dropped successfully.")
        except Exception as e:
            raise SoraDBLiteError(f"Error dropping collection '{collection_name}': {e}")

    # Basic CRUD Operations

    def insert_one(self , document):
        """
        Insert a single document into the collection.

        Parameters:
        document (dict): The document to be inserted.

        Returns:
        ObjectId: The ID of the inserted document.
        Raises:
            SoraDBLiteError: If the inserting fails.
        """
        try:
            result = self.collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            raise SoraDBLiteError(f"Error inserting document: {e}")

    def insert_many(self , documents):
        """
        Insert multiple documents into the collection.

        Parameters:
        documents (list): The list of documents to be inserted.

        Returns:
        list: A list of IDs of the inserted documents.
        Raises:
            SoraDBLiteError: If the inserting fails.
        """
        try:
            result = self.collection.insert_many(documents)
            return result.inserted_ids
        except Exception as e:
            raise SoraDBLiteError(f"Error inserting document: {e}")

    def find_one(self , query={}):
        """
        Find a single document in the collection that matches the query.

        Parameters:
        query (dict): The query to match documents against.

        Returns:
        dict: The first document that matches the query.
        Raises:
            SoraDBLiteError: If the finding fails.
        """
        try:
            result = self.collection.find_one(query)
            return result
        except Exception as e:
            raise SoraDBLiteError(f"Error finding document: {e}")

    def find_many(self , query={} , projection={}):
        """
        Find multiple documents in the collection that match the query.

        Parameters:
        query (dict): The query to match documents against.
        projection (dict): The fields to include or exclude in the returned documents.

        Returns:
        list: A list of documents that match the query.
        """
        try:
            results = self.collection.find(query , projection)
            return list(results)
        except Exception as e:
            raise SoraDBLiteError(f"Error finding document: {e}")

    def update_one(self , filter , update):
        """
        Update a single document in the collection that matches the filter.

        Parameters:
        filter (dict): The filter criteria to match documents.
        update (dict): The update operations to apply to the matching document.

        Returns:
        int: The number of documents modified.
        Raises:
            SoraDBLiteError: If the updating fails.
        """
        try:
            result = self.collection.update_one(filter , update)
            return result.modified_count
        except Exception as e:
            raise SoraDBLiteError(f"Error updating document: {e}")

    def delete_one(self , filter):
        """
        Delete a single document in the collection that matches the filter.

        Parameters:
        filter (dict): The filter criteria to match documents.

        Returns:
        int: The number of documents deleted.
        Raises:
            SoraDBLiteError: If the deleting fails.
        """
        try:
            result = self.collection.delete_one(filter)
            return result.deleted_count
        except Exception as e:
            raise SoraDBLiteError(f"Error deleting document: {e}")

    def update_many(self , filter , update):
        """
        Update multiple documents in the collection that match the filter.

        Parameters:
        filter (dict): The filter criteria to match documents.
        update (dict): The update operations to apply to the matching documents.

        Returns:
        int: The number of documents modified.
        Raises:
            SoraDBLiteError: If the updating fails.
        """
        try:
            result = self.collection.update_many(filter , update)
            return result.modified_count
        except Exception as e:
            raise SoraDBLiteError(f"Error updating document: {e}")

    def delete_many(self , filter):
        """
        Delete multiple documents in the collection that match the filter.

        Parameters:
        filter (dict): The filter criteria to match documents.

        Returns:
        int: The number of documents deleted.
        Raises:
            SoraDBLiteError: If the deleting fails.
        """
        try:
            result = self.collection.delete_many(filter)
            return result.deleted_count
        except Exception as e:
            raise SoraDBLiteError(f"Error deleting document: {e}")

    def find(self , query={} , projection={} , sort=None , limit=None):
        """
        Find documents in the collection that match the query, with optional projection, sorting, and limiting.

        Parameters:
        query (dict): The query to match documents against.
        projection (dict): The fields to include or exclude in the returned documents.
        sort (dict or list): The sort order for the results.
        limit (int): The maximum number of documents to return.

        Returns:
        list: A list of documents that match the query.
        """
        cursor = self.collection.find(query , projection)

        if sort:
            if isinstance(sort , dict):
                cursor = cursor.sort(sort)
            elif isinstance(sort , list):
                cursor = cursor.sort(sort)
            else:
                raise ValueError("Sort parameter must be a dict or list")

        if limit:
            cursor = cursor.limit(limit)

        return list(cursor)

    def sort_by(self , sort_key , ascending=True):
        """
        Sort documents in the collection by a specified key in ascending or descending order.

        Parameters:
        sort_key (str): The key to sort documents by.
        ascending (bool): Sort order. `True` for ascending, `False` for descending.

        Returns:
        list: A list of sorted documents.
        Raises:
            SoraDBLiteError: If the sorting fails.
        """
        try:
            sort_order = pymongo.ASCENDING if ascending else pymongo.DESCENDING
            results = self.collection.find().sort([(sort_key , sort_order)])
            return list(results)
        except pymongo.errors.PyMongoError as e:
            raise SoraDBLiteError(f"Error sorting document: {e}")

    def count(self , query={}):
        """
        Count the number of documents in the collection that match the query.

        Parameters:
        query (dict): The query to match documents against.

        Returns:
        int: The number of documents that match the query.
        Raises:
            SoraDBLiteError: If the counting fails.
        """
        try:
            return self.collection.count_documents(query)
        except pymongo.errors.PyMongoError as e:
            raise SoraDBLiteError(f"Error counting version: {e}")

    def fetch_values_by_key(self , key_name):
        """
        Fetch all values for a specified key from all documents in the collection.

        Parameters:
        key_name (str): The key to fetch values for.

        Returns:
        list: A list of values for the specified key.
        Raises:
            SoraDBLiteError: If the fetchin values by using key fails.
        """
        values = []
        try:
            for document in self.collection.find():
                if key_name in document:
                    values.append(document[key_name])
            return values
        except pymongo.errors.PyMongoError as e:
            raise SoraDBLiteError(f"Error fetching values by key: {e}")

    def version(self):
        """
        Print the version of pymongo and the version of SoraDB.


        Raises:
            SoraDBLiteError: If the version retrieving fails.
        """
        try:
            print(f"\nPymongo version: {pymongo.version}")
            print(f"Sora db: 1.0.0\n")
        except Exception as e:
            raise SoraDBLiteError(f"Error retrieving version: {e}")
