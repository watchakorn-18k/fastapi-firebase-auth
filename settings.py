import dotenv
import os

dotenv.load_dotenv("_env")

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
