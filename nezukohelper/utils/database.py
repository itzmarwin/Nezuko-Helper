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
    db = client.NezukoHelper
    logger.info("🌸 MongoDB Connection Successful!")
except Exception as e:
    logger.error(f"❌ MongoDB Connection Failed: {e}")
    client = None
    db = None

# Database collections (SAFE INITIALIZATION)
users = db.users if db is not None else None
groups = db.groups if db is not None else None
warns = db.warns if db is not None else None
filters = db.filters if db is not None else None
afk = db.afk if db is not None else None
gbans = db.gbans if db is not None else None
couples = db.couples if db is not None else None
broadcasts = db.broadcasts if db is not None else None
messages = db.messages if db is not None else None

async def test_db_connection():
    if client is None:
        logger.error("❌ MongoDB client not initialized!")
        return False
    try:
        await client.admin.command('ping')
        logger.info("🌸 MongoDB connection verified!")
        return True
    except Exception as e:
        logger.error(f"❌ MongoDB ping failed: {str(e)}")
        return False
