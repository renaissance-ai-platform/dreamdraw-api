
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field, BaseConfig
from bson import ObjectId

class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class DBModelMixin(BaseModel):
    created_at: Optional[datetime]=datetime.utcnow()
    updated_at: Optional[datetime]=datetime.utcnow()
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')

class UserBase(DBModelMixin):
    name: str = Field(...)
    username:str = Field(...)
    email:EmailStr = Field(...)

class UserWithToken(UserBase):
    token: str=Field(...)

class UserInResponse(RWModel):
    user: UserWithToken

class UserInLogin(DBModelMixin):
    email: EmailStr=Field(...)
    password: str=Field(...)

class UserInRegister(UserInLogin):
    name: str = Field(...)
    username:str = Field(...)
    salt:str=None

class UserInUpdate(BaseModel):
    username: Optional[str] = Field(...)
    email: Optional[EmailStr] = Field(...)
    password: Optional[str] = Field(...)
    name: Optional[str] = Field(...)

class TokenPayload(RWModel):
    username: str = ""