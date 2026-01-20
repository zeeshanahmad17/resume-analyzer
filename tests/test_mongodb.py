from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
def test_mongodb_connection():
    """Test MongoDB Atlas connection"""
    try:
        # Get connection string
        mongodb_uri = os.getenv('MONGODB_URI')
        
        if not mongodb_uri:
            print("❌ MONGODB_URI not found in .env file")
            return False
        
        # Connect
        print("Connecting to MongoDB Atlas...")
        client = MongoClient(mongodb_uri)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        
        # List databases
        dbs = client.list_database_names()
        print(f"Available databases: {dbs}")
        
        # Check if our database exists
        db = client.resume_analyzer
        collections = db.list_collection_names()
        print(f"Collections in 'resume_analyzer': {collections}")
        
        # Test insert
        test_collection = db.resume_chunks
        test_doc = {"test": "connection", "type": "test"}
        result = test_collection.insert_one(test_doc)
        print(f"✅ Test insert successful! ID: {result.inserted_id}")
        
        # Clean up test document
        test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Test cleanup successful!")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False
if __name__ == "__main__":
    print("=" * 50)
    print("Testing MongoDB Atlas Connection")
    print("=" * 50 + "\n")
    
    success = test_mongodb_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ MongoDB setup complete!")
    else:
        print("❌ MongoDB setup failed - check your connection string")
    print("=" * 50)
