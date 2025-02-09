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
    logger.info("🌸 Successfully connected to MongoDB!")
except Exception as e:
    logger.error(f"❌ MongoDB connection failed: {str(e)}")

# Database collections
users = db.users if db else None
groups = db.groups if db else None
warns = db.warns if db else None
filters = db.filters if db else None
afk = db.afk if db else None
gbans = db.gbans if db else None
couples = db.couples if db else None
broadcasts = db.broadcasts if db else None
messages = db.messages if db else None

async def test_db_connection():
    try:
        await client.admin.command('ping')
        logger.info("🌸 MongoDB connection verified!")
        return True
    except Exception as e:
        logger.error(f"❌ MongoDB ping failed: {str(e)}")
        return False
