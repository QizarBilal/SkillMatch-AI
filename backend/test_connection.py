from pymongo import MongoClient
from urllib.parse import quote_plus

username = "bilalqizar"
password = "bilalqizar"
cluster = "techportfoliohub.s3pd6uw.mongodb.net"

uri = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@{cluster}/?appName=TechPortfolioHub"

print(f"Testing connection with:")
print(f"  Username: {username}")
print(f"  Cluster: {cluster}")
print(f"  URI (sanitized): mongodb+srv://***:***@{cluster}/?appName=TechPortfolioHub")
print()

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    
    print("Attempting to connect...")
    server_info = client.server_info()
    
    print("✓ SUCCESS! Connected to MongoDB Atlas")
    print(f"  MongoDB Version: {server_info.get('version')}")
    
    print(f"\nAvailable databases:")
    for db in client.list_database_names():
        print(f"  - {db}")
    
    db = client["SkillMatch"]
    print(f"\nCollections in 'SkillMatch' database:")
    collections = db.list_collection_names()
    if collections:
        for col in collections:
            print(f"  - {col}")
    else:
        print("  (no collections yet - this is normal for new database)")
    
    print("\n✓ Connection test PASSED!")
    
except Exception as e:
    print(f"✗ FAILED: {e}")
    print(f"\nError details: {type(e).__name__}")
    print("\nTroubleshooting:")
    print("1. In MongoDB Atlas → Database Access:")
    print("   - Click 'Edit' on user 'bilalqizar'")
    print("   - Click 'Edit Password' and set it to: bilalqizar")
    print("   - Click 'Update User'")
    print("2. Wait 30 seconds and try again")
