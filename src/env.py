import os

from dotenv import load_dotenv

load_dotenv()
DB_CLUSTER = os.getenv('DB_CLUSTER')
DB_NAME = os.getenv('DB_NAME')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS').split(',')
