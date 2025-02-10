import motor.motor_asyncio
import os
import logging
import traceback
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# MongoDB setup with type hints
client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
db: Optional[motor.motor_asyncio.AsyncIOMotorDatabase] = None

async def init_db():
    """Initialize MongoDB connection and collections"""
    global client, db
    
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
        db = client["NezukoHelper"]
        
        # Initialize all collections here
        global users, groups, messages
        users = db.users
        groups = db.groups
        messages = db.messages
        
        await client.admin.command('ping')
        logger.info("✅ Database & Collections Initialized!")
        return True
    except Exception as e:
        logger.error(f"❌ DB Init Failed: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def get_collection(name: str):
    """Safely access collections with lazy initialization"""
    if db is None:
        logger.warning(f"⚠️ Accessing '{name}' before DB init!")
        return None
    return db[name]

async def test_db_connection():
    """Test connection with auto-reconnect"""
    try:
        if not client:
            await init_db()
        await client.admin.command('ping')
        return True
    except:
        return False
