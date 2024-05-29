import os
import dotenv

dotenv.load_dotenv()

# https://my.telegram.org/apps
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")
CSV_FILENAME = "messages.csv"