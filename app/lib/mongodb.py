from pymongo import MongoClient
from .config import app_config


mongodb = MongoClient(app_config["env"]["MONGODB_URI"]).get_database()
