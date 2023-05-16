import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from pydantic import EmailStr, BaseModel
from db_models import User, UserCreate, UserUpdate, UserDB
from user_manager import get_user_manager
import emailer as ms
from db import database
from utils import get_env_variable

app = FastAPI(
    title="PackerUserManagement",
    description="Packer user management web api.",
    version="0.0.1",
  )

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://packer.ga",
    "https://packer.ga",
  ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
  )


JWT_SECRET = get_env_variable("JWT_SECRET")

jwt_authentication = JWTAuthentication(secret=JWT_SECRET, lifetime_seconds=4*3600)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
  )

# @app.on_event("startup")
# async def startup() -> None:
#     database_ = app.state.database
#     if not database_.is_connected:
#         await database_.connect()

# @app.on_event("shutdown")
# async def shutdown() -> None:
#     database_ = app.state.database
#     if database_.is_connected:
#         await database_.disconnect()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()




@app.get("/")
def index():
  return {
            "Hello": "Welcome to the PackerUserManagement!",
            "version" : app.version,
            "title" : app.title,
            "description" : app.description,
            "docs_url" : app.docs_url,
            "redoc_url" : app.redoc_url,
            "openapi_url" : app.openapi_url,
          }

app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"],
  )

app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
  )

app.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
  )

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
  )

app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
  )


@app.post("/email")
async def send_email_to_packersolver(text: str):
  res = await ms.send_to_one(
      recipient=EmailStr("packersolver@gmail.com"),
      subject="email from homepage",
      body=text
    )
  return res

# source: https://cloud.google.com/appengine/docs/standard/python3/configuring-warmup-requests
# @app.get("/_ah/warmup")
# def warmup():
#     # Handle your warmup logic here, e.g. set up a database connection pool
#     return "", 200, {}