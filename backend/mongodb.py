from pymongo import MongoClient
from datetime import datetime
import os
from urllib.parse import quote_plus

MONGO_USERNAME = os.getenv("MONGO_USERNAME", "bilalqizar")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "bilalqizar")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER", "techportfoliohub.s3pd6uw.mongodb.net")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "SkillMatch")

MONGO_URI = f"mongodb+srv://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@{MONGO_CLUSTER}/?appName=TechPortfolioHub"

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
db = client[MONGO_DATABASE]

def test_connection():
    try:
        client.admin.command('ping')
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
        client.admin.command('ping', maxTimeMS=2000)
        return True
    except:
        return False

users_collection = db["users"]
submissions_collection = db["submissions"]
resumes_collection = db["resumes"]
job_descriptions_collection = db["job_descriptions"]
analysis_results_collection = db["analysis_results"]

def get_mongo_db():
    return db

def init_indexes():
    users_collection.create_index("email", unique=True)
    users_collection.create_index("user_id", unique=True)
    submissions_collection.create_index("user_id")
    submissions_collection.create_index("submission_id", unique=True)
    resumes_collection.create_index("resume_id")
    job_descriptions_collection.create_index("jd_id")
    analysis_results_collection.create_index("analysis_id")

try:
    init_indexes()
except:
    pass
