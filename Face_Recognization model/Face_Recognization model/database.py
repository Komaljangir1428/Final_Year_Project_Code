"""MongoDB database connection and utilities."""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

from config import MONGODB_URI, MONGODB_DB_NAME

# Global client and database instances
client: AsyncIOMotorClient = None
db = None

PERSONS_COLLECTION = "persons"
ATTENDANCE_COLLECTION = "attendance"


async def connect_to_db():
    """Establish connection to MongoDB."""
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[MONGODB_DB_NAME]
    # Create index for faster lookups
    await db[PERSONS_COLLECTION].create_index([("name", ASCENDING)])
    await db[ATTENDANCE_COLLECTION].create_index([("date", ASCENDING)])
    print("Connected to MongoDB successfully")


async def close_db_connection():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_db():
    """Get database instance."""
    return db
