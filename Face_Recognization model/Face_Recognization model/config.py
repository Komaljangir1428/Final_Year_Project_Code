"""Application configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "face_recognition_db")

# Face recognition settings (face-library embeddings - tune if needed)
TOLERANCE = 1.0  # Lower = stricter matching (face-library scale may differ from dlib)
