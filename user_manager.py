import os
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager
from pydantic.networks import EmailStr

from db import get_user_db
from db_models import UserCreate, UserDB
import emailer as ms
from utils import get_env_variable
class UserManager(BaseUserManager[UserCreate, UserDB]):
  user_db_model = UserDB
  reset_password_token_secret = get_env_variable("RESET_PASSWORD_TOKEN_SECRET")
  verification_token_secret = get_env_variable("VERIFICATION_TOKEN_SECRET")

  async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
    print(f"User {user.id} has registered.")
    res = await ms.send_to_one(
        recipient=EmailStr(user.email),
        subject="Welcome to PackerSolver!",
        body = f"You have been successfully registered as PackerSolver user. Your username is {user.email}"
      )

  async def on_after_forgot_password(
      self, user: UserDB, token: str, request: Optional[Request] = None
    ):
      print(f"User {user.id} has forgot their password. Reset token: {token}")
      res = await ms.send_to_one(
          recipient=EmailStr(user.email),
          subject="PackerSolver password reset",
          body = f"Your secret reset token is: {token}"
        )

  async def on_after_request_verify(
      self, user: UserDB, token: str, request: Optional[Request] = None
    ):
    print(f"Verification requested for user {user.id}. Verification token: {token}")
    res = await ms.send_to_one(
        recipient=EmailStr(user.email),
        subject="PackerSolver user verification request",
        body = f"Your secret verification token is: {token}"
      )


async def get_user_manager(user_db=Depends(get_user_db)):
  yield UserManager(user_db)

