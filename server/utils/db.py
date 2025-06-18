from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["UserReportStorage"]
users_collection = db["Users"]
pitt_walktimes_collection = db["SchoolLocationsData"]