import motor.motor_asyncio
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = None
db = None

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client.get_database("NezukoHelper") if client else None
    logger.info("🌸 MongoDB Connected!")
except Exception as e:
    logger.error(f"❌ MongoDB Connection Failed: {str(e)}")
    client = None
    db = None

# Safely initialize collections
def get_collection(name: str):
    """Safely get a collection or return None"""
    return db[name] if db is not None else None

users = get_collection("users")
groups = get_collection("groups")
warns = get_collection("warns")
filters = get_collection("filters")
afk = get_collection("afk")
gbans = get_collection("gbans")
couples = get_collection("couples")
broadcasts = get_collection("broadcasts")
messages = get_collection("messages")

async def test_db_connection():
    if client is None:
        logger.error("❌ MongoDB Client Not Initialized!")
        return False
    try:
        await client.admin.command('ping')
        logger.info("🌸 MongoDB Connection Verified!")
        return True
    except Exception as e:
        logger.error(f"❌ MongoDB Ping Failed: {str(e)}")
        return False
