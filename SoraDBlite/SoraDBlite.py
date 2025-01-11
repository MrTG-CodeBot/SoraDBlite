import pymongo
import subprocess
from pymongo import MongoClient
from pymongo import InsertOne
import google.generativeai as genai
import requests
from datetime import datetime
import json
from typing import Any , Dict , List , Optional , Union
import logging

logging.basicConfig(
    level=logging.INFO ,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SoraDBlite')

def sora_ai(prompt: str , safety_settings: Optional[Dict] = None) -> None:
    """
    Generates a response from Sora AI based on the given prompt and safety settings.

    Args:
        prompt (str): The input prompt for generating a response.
        safety_settings (Optional[Dict]): Safety settings for response generation.
    """
    try:
        genai.configure(api_key="YOUR_API_")

        generation_config = {
            "temperature": 1.0 ,
            "top_p": 0.95 ,
            "top_k": 64 ,
            "max_output_tokens": 8192 ,
            "response_mime_type": "text/plain" ,
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash" ,
            generation_config=generation_config ,
            safety_settings=safety_settings ,
        )
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(
            f"{prompt}\nfind the error, and give the solution in 2 sentences."
        )
        print(f"\n\nSora Ai: {response.text}")
    except Exception as e:
        logger.error(f"Error in Sora AI: {e}")
        raise

def update_SoraDBlite() -> None:
    """Updates SoraDBlite to the latest version."""
    try:
        url = "https://pypi.org/pypi/SoraDBlite/json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            latest_version = data["info"]["version"]
            subprocess.run(
                ["pip" , "install" , "--upgrade" , f"SoraDBlite=={latest_version}"] ,
                check=True
            )
            logger.info(f"SoraDBlite upgraded to {latest_version}")
    except Exception as e:
        logger.error(f"Error upgrading SoraDBlite: {e}")
        raise


def get_all_collection(db_url: str , db_pass: str) -> None:
    """Gets all collection names from a specified MongoDB database.

    Args:
        db_url (str): The MongoDB connection URI.
        db_pass (str): The name of the database.

    Returns:
        list: A list of collection names.
    """
    clienturi = MongoClient(db_url)
    dbpass = clienturi[db_pass]
    collection_names = dbpass.list_collection_names()

    for index , collection_name in enumerate(collection_names):
        print(f"{index}: {collection_name}")


def is_collection_available(db_url: str , db_pass: str , dp_collection_name: str) -> None:
    """
    Checks if a collection exists in the specified MongoDB database.

    Args:
        db_url (str): The MongoDB connection URL.
        db_pass (str): The database name.
        dp_collection_name (str): The collection name to check.

    Returns:
        None
    """
    clienturi = MongoClient(db_url)
    dbpass = clienturi[db_pass]
    c_name = dbpass.list_collection_names()
    if dp_collection_name in c_name:
        print(f"Collection name: {dp_collection_name} is exist")
    else:
        print(f"Collection name: {dp_collection_name} does not exist")


class SoraDBLiteError(Exception):
    """Custom exception for SoraDBlite errors."""
    pass

class SoraDBlite:
    def __init__(self):
        self.__client: Optional[MongoClient] = None
        self.__db = None
        self.__collection = None
        self.__audit_collection = None
        self.__cache: Dict[str , Any] = {}
        self.__cache_timeout = 300

    def connect(self , db_url: str , db_password: str , db_collection: str) -> None:
        """
        Establishes connection to MongoDB with enhanced features.

        Args:
            db_url (str): MongoDB connection URL
            db_password (str): Database name
            db_collection (str): Collection name
        """
        try:
            self.__client = MongoClient(db_url)
            self.__db = self.__client[db_password]
            self.__collection = self.__db[db_collection]
            self.__audit_collection = self.__db['audit_logs']
            logger.info("Connected to MongoDB successfully")

        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise SoraDBLiteError(f"Failed to connect: {e}")

    def __audit_log(self , operation: str , details: Dict) -> None:
        """Records audit log entry."""
        if self.__audit_collection is not None:
            log_entry = {
                'timestamp': datetime.utcnow() ,
                'operation': operation ,
                'details': details
            }
            self.__audit_collection.insert_one(log_entry)
        else:

            print("Audit collection not available for logging")

    def backup_collection(self , backup_name: str) -> None:
        """
        Creates a backup of the current collection.

        Args:
            backup_name (str): Name for the backup collection
        """
        try:
            backup_collection = self.__db[f"{backup_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"]
            for doc in self.__collection.find():
                backup_collection.insert_one(doc)
            logger.info(f"Backup created: {backup_collection.name}")
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise SoraDBLiteError(f"Backup failed: {e}")

    def export_to_json(self , filepath: str) -> None:
        """
        Exports collection data to JSON file.

        Args:
            filepath (str): Path to save the JSON file
        """
        try:
            data = list(self.__collection.find({} , {'_id': False}))
            with open(filepath , 'w') as f:
                json.dump(data , f , default=str)
            logger.info(f"Data exported to {filepath}")
        except Exception as e:
            logger.error(f"Export failed: {e}")
            raise SoraDBLiteError(f"Export failed: {e}")

    def import_from_json(self , filepath: str) -> None:
        """
        Imports data from JSON file.

        Args:
            filepath (str): Path to JSON file to import
        """
        try:
            with open(filepath , 'r') as f:
                data = json.load(f)
            if isinstance(data , list):
                self.__collection.insert_many(data)
            logger.info(f"Data imported from {filepath}")
        except Exception as e:
            logger.error(f"Import failed: {e}")
            raise SoraDBLiteError(f"Import failed: {e}")

    def get_audit_logs(self , start_date: Optional[datetime] = None ,
                       end_date: Optional[datetime] = None) -> List[Dict]:
        """
        Retrieves audit logs within date range.

        Args:
            start_date (Optional[datetime]): Start date for logs
            end_date (Optional[datetime]): End date for logs

        Returns:
            List[Dict]: Audit log entries
        """
        query = {}
        if start_date:
            query['timestamp'] = {'$gte': start_date}
        if end_date:
            query.setdefault('timestamp' , {})['$lte'] = end_date

        return list(self.__audit_collection.find(query).sort('timestamp' , -1))

    def get_collection_stats(self) -> Dict:
        """
        Returns statistics about the collection.

        Returns:
            Dict: Collection statistics
        """
        try:
            return self.__db.command('collstats' , self.__collection.name)
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            raise SoraDBLiteError(f"Failed to get collection stats: {e}")

    def insert_one(self , document: Dict) -> str:
        """Enhanced insert_one with audit logging."""
        try:
            document['created_at'] = datetime.utcnow()
            result = self.__collection.insert_one(document)
            self.__audit_log('insert_one' , {'document_id': str(result.inserted_id)})
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Insert failed: {e}")
            raise SoraDBLiteError(f"Insert failed: {e}")

    def find_one(self , query: Dict = {} , use_cache: bool = False) -> Optional[Dict]:
        """Enhanced find_one with caching support."""
        cache_key = f"find_one_{str(query)}"
        if use_cache and cache_key in self.__cache:
            return self.__cache[cache_key]

        result = self.__collection.find_one(query)
        if use_cache:
            self.__cache[cache_key] = result
        return result

    def drop_collection(self , collection_name: str) -> None:
        """
        Drop a collection from the database.

        Args:
            collection_name (str): Name of the collection to drop
        """
        try:
            collection = self.__db[collection_name]
            collection.drop()
            logger.info(f"Collection '{collection_name}' dropped successfully")
            self.__audit_log('drop_collection' , {'collection': collection_name})
        except Exception as e:
            logger.error(f"Error dropping collection: {e}")
            raise SoraDBLiteError(f"Error dropping collection '{collection_name}': {e}")

    def insert_many(self , documents: List[Dict]) -> List[str]:
        """
        Insert multiple documents into the collection.

        Args:
            documents (List[Dict]): List of documents to insert

        Returns:
            List[str]: List of inserted document IDs
        """
        try:
            result = self.__collection.insert_many(documents)
            self.__audit_log('insert_many' , {'count': len(documents)})
            return result.inserted_ids
        except Exception as e:
            logger.error(f"Error inserting documents: {e}")
            raise SoraDBLiteError(f"Error inserting documents: {e}")

    def find_many(self , query: Dict = None , projection: Dict = None) -> List[Dict[str , Any]]:
        """
        Find multiple documents matching the query.

        Args:
            query (Dict): Query filter
            projection (Dict): Fields to include/exclude

        Returns:
            List[Dict[str, Any]]: List of matching documents
        """
        try:
            query = query or {}
            projection = projection or {}
            results = self.__collection.find(query , projection)
            return list(results)
        except Exception as e:
            logger.error(f"Error finding documents: {e}")
            raise SoraDBLiteError(f"Error finding documents: {e}")

    def update_one(self , filter: Dict , update: Dict) -> int:
        """
        Update a single document in the collection.

        Args:
            filter (Dict): Query filter to match the document
            update (Dict): Update operations to apply

        Returns:
            int: Number of documents modified
        """
        try:
            result = self.__collection.update_one(filter , update)
            self.__audit_log('update_one' , {'filter': filter , 'update': update})
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            raise SoraDBLiteError(f"Error updating document: {e}")

    def delete_one(self , filter: Dict) -> int:
        """
        Delete a single document from the collection.

        Args:
            filter (Dict): Query filter to match the document

        Returns:
            int: Number of documents deleted
        """
        try:
            result = self.__collection.delete_one(filter)
            self.__audit_log('delete_one' , {'filter': filter})
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise SoraDBLiteError(f"Error deleting document: {e}")

    def update_many(self , filter: Dict , update: Dict) -> int:
        """
        Update multiple documents in the collection.

        Args:
            filter (Dict): Query filter to match documents
            update (Dict): Update operations to apply

        Returns:
            int: Number of documents modified
        """
        try:
            result = self.__collection.update_many(filter , update)
            self.__audit_log('update_many' , {'filter': filter , 'update': update})
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating documents: {e}")
            raise SoraDBLiteError(f"Error updating documents: {e}")

    def delete_many(self , filter: Dict) -> int:
        """
        Delete multiple documents from the collection.

        Args:
            filter (Dict): Query filter to match documents

        Returns:
            int: Number of documents deleted
        """
        try:
            result = self.__collection.delete_many(filter)
            self.__audit_log('delete_many' , {'filter': filter})
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            raise SoraDBLiteError(f"Error deleting documents: {e}")

    def sort_by(self , sort_key: str , ascending: bool = True) -> List[Dict]:
        """
        Sort documents by a specified key.

        Args:
            sort_key (str): Field to sort by
            ascending (bool): Sort order (True for ascending)

        Returns:
            List[Dict]: Sorted list of documents
        """
        try:
            sort_order = pymongo.ASCENDING if ascending else pymongo.DESCENDING
            results = self.__collection.find().sort([(sort_key , sort_order)])
            return list(results)
        except Exception as e:
            logger.error(f"Error sorting documents: {e}")
            raise SoraDBLiteError(f"Error sorting documents: {e}")

    def count(self , query: Dict = {}) -> int:
        """
        Count documents matching the query.

        Args:
            query (Dict): Query filter

        Returns:
            int: Number of matching documents
        """
        try:
            return self.__collection.count_documents(query)
        except Exception as e:
            logger.error(f"Error counting documents: {e}")
            raise SoraDBLiteError(f"Error counting documents: {e}")

    def fetch_values_by_key(self , key_name: str) -> List:
        """
        Fetch all values for a specific key across all documents.

        Args:
            key_name (str): Field name to fetch values for

        Returns:
            List: List of values for the specified key
        """
        try:
            values = []
            for document in self.__collection.find({} , {key_name: 1}):
                if key_name in document:
                    values.append(document[key_name])
            return values
        except Exception as e:
            logger.error(f"Error fetching values by key: {e}")
            raise SoraDBLiteError(f"Error fetching values by key: {e}")

    def version(self) -> None:
        """
        Prints version information of SoraDBlite and Pymongo.

        Returns:
            None
        """
        try:
            response = requests.get("https://pypi.org/pypi/SoraDBlite/json")
            if response.status_code == 200:
                data = response.json()
                latest_version = data["info"]["version"]
                print(f"\nSoraDBlite version:{latest_version}")
            print(f"Pymongo version: {pymongo.version}")
        except Exception as e:
            logger.error(f"Failed to get version info: {e}")
            raise SoraDBLiteError(f"Failed to get version info: {e}")
