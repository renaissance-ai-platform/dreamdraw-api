
from fastapi import APIRouter, status, Depends, Body, Header
from fastapi.exceptions import HTTPException
from dreamdraw_api.services import security
from dreamdraw_api.db.models.users import (
	UserBase,
	UserInResponse,
	UserWithToken,
	UserInLogin,
	UserInRegister,
	UserInUpdate
)
from dreamdraw_api.db import get_database
from dreamdraw_api import config

users_api = APIRouter()

@users_api.post(
	"/register",
	status_code=status.HTTP_201_CREATED,
	response_model=UserInResponse,
	name="users:register",
	tags=["authentication"]
)
async def register_user(
	user_register: UserInRegister=Body(..., embed=True),
	db=Depends(get_database)
) -> UserInResponse:

	user = await db[config.USERS_COLLECTION].find_one({"email": user_register.email})
	if user:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists with this email")

	user_register.salt = security.generate_salt()
	user_register.password = security.get_password_hash(user_register.password + user_register.salt)

	new_user = await db[config.USERS_COLLECTION].insert_one(user_register.dict())

	token = security.create_access_token(user_register.dict(), str(config.SECRET_STR))

	return UserInResponse(
		user=UserWithToken(
			new_user.dict(),
			token=token
		)
	)

@users_api.post(
	"/login",
	status_code=status.HTTP_200_OK,
	response_model=UserInResponse,
	name="users:login",
	tags=["authentication"]
)
async def login(
	user_login: UserInLogin=Body(..., embed=True),
	db=Depends(get_database)
) -> UserInResponse:

	user = await db[config.USERS_COLLECTION].find_one({"email": user_login.email})
	if not user or not security.verify_password(user_login.password, user.password):
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

	token = security.create_access_token(user.dict(), str(config.SECRET_STR))

	return UserInResponse(
		user=UserWithToken(
			user.dict(),
			token=token
		),
	)


@users_api.get(
	"/user",
	response_model=UserInResponse,
	tags=["user"],
	name="users:user"
)
async def current_user(user: UserBase=Depends(security.get_current_user_authorizer())) -> UserInResponse:
	return UserInResponse(user=user)

@users_api.put("/user", response_model=UserInResponse, name="users:user-update", tags=["users"])
async def update_current_user(
	user: UserInUpdate=Body(..., embed=True),
	current_user: UserBase=Depends(security.get_current_user_authorizer()),
	db=Depends(get_database)
):
	if user.username == current_user.username:
		user.username = None
	if user.email == current_user.email:
		user.email = None

	await security.check_free_username_and_email(db, user.username, user.email)

	db_user = await db[config.USERS_COLLECTION].find_one({'email': user.email})
	if db_user:
		db_user.username = user.username or db_user.username
		db_user.email = user.email or db_user.email
		db_user.name = user.name or db_user.name
		if user.password:
			db_user.password = security.get_password_hash(user.password)
		
		updated_at = await db[config.USERS_COLLECTION].update_one({"email": db_user.email}, {'$set': db_user.dict()})
		db_user.updated_at = updated_at

		return db_user
	
	return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")