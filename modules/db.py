from pymongo import MongoClient

from modules.constants import MONGO_DB_NAME, MONGO_INN_COLLECTION_NAME, MONGO_URL

client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]
inn_collection = db[MONGO_INN_COLLECTION_NAME]

