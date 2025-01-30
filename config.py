import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "ZTkwYTdiZjc1ZDkyMjczZmFhMjNjM2NjY2YyM2FjM2JlYzQ=")
ALGORITHM = os.getenv("ALGORITHM")  # Used for JWT encoding
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expiration time
DATABASE_URL = os.getenv("DATABASE_URL")
