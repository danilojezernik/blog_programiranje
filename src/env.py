import os

from dotenv import load_dotenv

load_dotenv()
DB_CLUSTER = os.getenv('DB_CLUSTER')
DB_NAME = os.getenv('DB_NAME')