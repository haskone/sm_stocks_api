from pymongo import MongoClient
from utils import get_config

config = get_config()
client = MongoClient(config['mongourl'])
db = client.stocks
companies = db.companies

def save(obj):
    companies.insert_one(obj)
