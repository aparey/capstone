# Quick test script - save as test_mongodb.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Your MongoDB connection string
    client = MongoClient(os.getenv('MONGODB_URI'))
    
    # Test the connection
    client.admin.command('ping')
    print("✅ MongoDB Atlas connected successfully!")
    
    # List your databases
    print("\nDatabases:")
    for db_name in client.list_database_names():
        print(f"  - {db_name}")
    
    # Check your NANDA database
    db = client['nanda']  # or whatever you named it
    print(f"\nCollections in 'nanda' database:")
    for collection in db.list_collection_names():
        print(f"  - {collection}")
        
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")