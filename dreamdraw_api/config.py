from enum import Enum

class DeploymentMode(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"

ENVIRONMENT:str = DeploymentMode.DEV
IMAGESERVER_URL:str = 'http://localhost:3000/images'
SAVE_DIR:str = 'static'
HUGGINGFACE_TOKEN: str = "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"

# API PREFIX
API_PREFIX = "/api/v1"

# JWT
JWT_SUBJECT = 'dreamdraw-access'
JWT_ALGO = 'HS256'
ACCESS_TOKEN_EXPIRE_MINS = 60 * 14 * 7 # one week
SECRET_STR = "secret"

# MONGO DB
MONGODB_URL = 'mongodb://localhost:27017'
MONGODB_NAME = 'dreamdraw_db'
USERS_COLLECTION = 'users'