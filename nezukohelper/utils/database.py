import motor.motor_asyncio
import os
import logging
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI")
client = None
db = None

async def init_db():
    """Initialize MongoDB connection asynchronously"""
    global client, db
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        db = client["NezukoHelper"]  # Database name
        await client.admin.command('ping')
        logger.info("🌸 MongoDB Connected Successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ MongoDB Connection Failed: {str(e)}")
        logger.error(traceback.format_exc())  # Detailed traceback
        client = None
        db = None
        return False

def get_collection(name: str):
    """Safely get collection with connection check"""
    if db is None:
        logger.warning(f"⚠️ Trying to access '{name}' collection before DB initialization!")
        return None
    return db[name]

# Collections initialization with safety checks
users = get_collection("users") or logger.error("❌ 'users' collection unavailable!")
groups = get_collection("groups") or logger.error("❌ 'groups' collection unavailable!")
messages = get_collection("messages") or logger.error("❌ 'messages' collection unavailable!")

async def test_db_connection():
    """Test and reinitialize connection if needed"""
    try:
        if not client:
            await init_db()
        await client.admin.command('ping')
        logger.info("✅ MongoDB Connection Verified!")
        return True
    except Exception as e:
        logger.error(f"❌ Connection Test Failed: {str(e)}")
        return False
