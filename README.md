# SoraDB

[![Python Versions](https://img.shields.io/pypi/pyversions/pymongo)](https://pypi.org/project/pymongo)

## 🌐 contact me:

[![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?logo=Instagram&logoColor=white)](https://instagram.com/mrtg_coder)
[![Telegram](https://img.shields.io/badge/Telegram-blue?logo=telegram)](https://t.me/MrTG_Coder)

## About

SoraDB is a Python wrapper for MongoDB operations, leveraging the power of the `pymongo` library. It simplifies database interactions, providing a seamless interface for performing essential CRUD (Create, Read, Update, Delete) operations. With SoraDB, developers can easily manage and manipulate data within their MongoDB collections, making it ideal for both simple and complex database tasks.

### Key Features:
◘ Easy Connection Management: Simplifies connecting to MongoDB databases.

◘ CRUD Operations: Perform basic CRUD operations effortlessly.

* Insert single or multiple documents.

* Find single or multiple documents with flexible query options.

* Update single or multiple documents.

* Delete single or multiple documents.

* Collection Management: Drop collections with ease.

◘ Sorting Capabilities: Sort documents by specified fields in ascending or descending order.


## How to get db url and collection

### Video Tutorial
For a detailed video tutorial, check out this link: [video](https://youtu.be/mD9veNL7KoE?si=nTb5GbfDINNy5TCQ)

## Difference 

## Differences Between `pymongo` and `SoraDB`

| Feature            | pymongo                                           | SoraDB                                       |
|--------------------|---------------------------------------------------|----------------------------------------------|
| **Library Type**   | Low-level MongoDB driver                          | High-level wrapper for `pymongo`             |
| **Usage**          | Directly interacts with MongoDB                   | Simplified methods for common operations     |
| **Flexibility**    | Complete control over MongoDB operations          | Abstracts complexity, less granular control  |
| **Error Handling** | Developers implement their own error handling     | Built-in error handling                      |
| **Code Complexity**| More complex and verbose                          | User-friendly and concise                    |


## Installation

Make sure you have `soradb` installed. You can install it using pip if you haven't already:

```sh
pip install soradb
```

# Usage

## Importing the Library

```python
import sora
from sora import Soradb
```

## Connecting to the Database

To connect to your MongoDB database, use the `connect` method:

```python
import sora
from sora import Soradb

db_url = "your_mongodb_url"
db_password = "your_db_password"
db_collection = "your_db_collection"

db = Soradb()
db.connect(db_url, db_password, db_collection)
```

## Inserting Documents

Insert a single document:

```python
import sora
from sora import Soradb

document = {"name": "Alice", "age": 30, "city": "New York"}
inserted_id = db.insert_one(document)
print("Inserted document with ID:", inserted_id)
```

Insert multiple documents:

```python
import sora
from sora import Soradb

documents = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Los Angeles"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]
inserted_ids = db.insert_many(documents)
print("Inserted document IDs:", inserted_ids)
```

## Finding Documents

Find a single document:

```python
import sora
from sora import Soradb

query = {"name": "Alice"}
result = db.find_one(query)
print("Found document:", result)
```

Find multiple documents:

```python
import sora
from sora import Soradb

query = {"age": {"$gt": 25}}
results = db.find_many(query)
print("Found documents:", results)
```

## Updating Documents

Update a single document:

```python
import sora
from sora import Soradb

filter = {"name": "Alice"}
update = {"$set": {"city": "Los Angeles"}}
updated_count = db.update_one(filter, update)
print("Updated documents:", updated_count)
```

Update multiple documents:

```python
import sora
from sora import Soradb

filter = {"city": "New York"}
update = {"$set": {"city": "New York City"}}
updated_count = db.update_many(filter, update)
print("Updated documents:", updated_count)
```

## Deleting Documents

Delete a single document:

```python
import sora
from sora import Soradb

filter = {"name": "Alice"}
deleted_count = db.delete_one(filter)
print("Deleted documents:", deleted_count)
```

Delete multiple documents:

```python
import sora
from sora import soradb

filter = {"age": {"$lt": 25}}
deleted_count = db.delete_many(filter)
print("Deleted documents:", deleted_count)
```

## Sorting Documents

Sort documents by a field in ascending order:

```python
import sora
from sora import soradb

results = db.sort_by("age", True)
print("Sorted by age (ascending):", results)
```

Sort documents by a field in descending order:

```python
import sora
from sora import soradb

results = db.sort_by("name", False)
print("Sorted by name (descending):", results)
```

## Dropping a Collection

To drop a collection, use the drop_collection method:

```python
import sora
from sora import soradb

db.drop_collection("soradb")
print("Collection 'soradb' dropped successfully.")
```

## Example Code
```python
import sora
from sora import soradb

db_url = "your_mongodb_url"
db_password = "your_db_password"
db_collection = "your_db_collection"

db = Soradb()
db.connect(db_url, db_password, db_collection)

# Insert a document
document = {"name": "Alice", "age": 30, "city": "New York"}
inserted_id = db.insert_one(document)
print("Inserted document with ID:", inserted_id)

# Find a document
query = {"name": "Alice"}
result = db.find_one(query)
print("Found document:", result)

# Find multiple documents
query = {"age": {"$gt": 25}}
results = db.find_many(query)
print("Found documents:", results)

# Update a document
filter = {"name": "Alice"}
update = {"$set": {"city": "Los Angeles"}}
updated_count = db.update_one(filter, update)
print("Updated documents:", updated_count)

# Delete a document
filter = {"name": "Alice"}
deleted_count = db.delete_one(filter)
print("Deleted documents:", deleted_count)

# Insert multiple documents
documents = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Los Angeles"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]
inserted_ids = db.insert_many(documents)
print("Inserted document IDs:", inserted_ids)

# Find multiple documents
query = {"age": {"$gt": 25}}
results = db.find_many(query)
print("Found documents:", results)

# Update multiple documents
filter = {"city": "New York"}
update = {"$set": {"city": "New York City"}}
updated_count = db.update_many(filter, update)
print("Updated documents:", updated_count)

# Delete multiple documents
filter = {"age": {"$lt": 25}}
deleted_count = db.delete_many(filter)
print("Deleted documents:", deleted_count)

# Sort documents by age
results = db.sort_by("age", True)
print("Sorted by age (ascending):", results)

# Sort documents by name
results = db.sort_by("name", False)
print("Sorted by name (descending):", results)

# Drop a collection
db.drop_collection("soradb")
print("Collection 'soradb' dropped successfully.")

```
