
import bcrypt
import jwt
from fastapi import Depends, Header, status
from fastapi.exceptions import HTTPException

from typing import Optional
from pydantic import ValidationError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from dreamdraw_api.db import get_database
from dreamdraw_api.db.models.users import UserBase, TokenPayload
from dreamdraw_api import config

JWT_SUBJECT = config.JWT_SUBJECT
ALGO = config.JWT_ALGO
ACCESS_TOKEN_EXPIRE_MINS = config.ACCESS_TOKEN_EXPIRE_MINS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_salt() -> str:
    return bcrypt.gensalt().decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(
    *,
    jwt_content: dict,
    secret_key: str,
    expires_delta: timedelta=timedelta(ACCESS_TOKEN_EXPIRE_MINS),
) -> str:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "sub": JWT_SUBJECT})
    return jwt.encode(to_encode, secret_key, algorithm=ALGO)

def get_current_user_authorizer():
    return _get_current_user_authorizer

async def _get_current_user_authorizer(
    db=Depends(get_database),
    authorization: str=Header(...)
) -> UserBase:
    token_prefix, token = authorization.split(" ")
    if token_prefix != config.JWT_TOKEN_PREFIX:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization type")

    try:
        payload = jwt.decode(token, str(config.SECRET_STR), algorithm=[ALGO])
        token_data = TokenPayload(**payload)
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    user = await db[config.USERS_COLLECTION].find_one({"email": token_data.email})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = UserBase(**user.dict(), token=token)
    return user

async def check_free_username_and_email():
    pass