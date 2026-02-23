from pymongo import MongoClient
from datetime import datetime
import os
from urllib.parse import quote_plus

MONGO_USERNAME = os.getenv("MONGO_USERNAME", "bilalqizar")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "bilalqizar")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER", "techportfoliohub.s3pd6uw.mongodb.net")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "SkillMatch")

MONGO_URI = f"mongodb+srv://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@{MONGO_CLUSTER}/?appName=TechPortfolioHub"


# Lazy MongoDB connection and collections
_mongo_client = None
_mongo_db = None
_collections = {}

def get_mongo_client():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
    return _mongo_client

def get_mongo_db():
    global _mongo_db
    if _mongo_db is None:
        _mongo_db = get_mongo_client()[MONGO_DATABASE]
    return _mongo_db

def get_collection(name):
    if name not in _collections:
        _collections[name] = get_mongo_db()[name]
    return _collections[name]

def test_connection():
    try:
        get_mongo_client().admin.command('ping')
        print(f"✓ Connected to MongoDB Atlas - Database: {MONGO_DATABASE}")
        return True
    except Exception as e:
        print(f"✗ MongoDB Connection Error: {e}")
        print("\nTo fix this, ensure:")
        print("1. MongoDB Atlas cluster is active")
        print("2. Database user exists with correct credentials")
        print("3. Your IP address is whitelisted (or use 0.0.0.0/0 for testing)")
        print("4. Network access is properly configured")
        return False

def quick_health_check():
    """Quick health check for Render - returns immediately if connection fails"""
    try:
        get_mongo_client().admin.command('ping', maxTimeMS=2000)
        return True
    except:
        return False

# Collection getters
def users_collection():
    return get_collection("users")
def submissions_collection():
    return get_collection("submissions")
def resumes_collection():
    return get_collection("resumes")
def job_descriptions_collection():
    return get_collection("job_descriptions")
def analysis_results_collection():
    return get_collection("analysis_results")

def init_indexes():
    users_collection().create_index("email", unique=True)
    users_collection().create_index("user_id", unique=True)
    submissions_collection().create_index("user_id")
    submissions_collection().create_index("submission_id", unique=True)
    resumes_collection().create_index("resume_id")
    job_descriptions_collection().create_index("jd_id")
    analysis_results_collection().create_index("analysis_id")
