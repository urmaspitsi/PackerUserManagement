import os
# source: https://sabuhish.github.io/fastapi-mail/example/

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.responses import JSONResponse
#from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import List
from utils import get_env_variable
#from fastapi_mail.email_utils import DefaultChecker

def mail_service_conf():
  return ConnectionConfig(
      MAIL_USERNAME = get_env_variable("MAIL_USERNAME"),
      MAIL_PASSWORD = get_env_variable("MAIL_PASSWORD"),
      MAIL_FROM = get_env_variable("MAIL_USERNAME"),
      MAIL_PORT = 587,
      MAIL_SERVER = "smtp.gmail.com",
      MAIL_FROM_NAME="Packer Solver",
      MAIL_TLS = True,
      MAIL_SSL = False,
      USE_CREDENTIALS = True,
      VALIDATE_CERTS = True
    )

async def send_test_email(recipients: List[EmailStr]) -> JSONResponse:
  try:
    message = MessageSchema(subject="fastapi_mail Test", recipients=recipients, body="Hello!")
    fm = FastMail(mail_service_conf())
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
  except Exception as ex:
    return JSONResponse(status_code=400, content={"message": f"{ex}"})

async def send_to_one(recipient: EmailStr, subject: str, body: str) -> JSONResponse:
  try:
    message = MessageSchema(
        subject = subject,
        recipients = [recipient],
        body = body
      )

    fm = FastMail(mail_service_conf())
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": f"email has been sent to {recipient}"})

  except Exception as ex:
    return JSONResponse(status_code=400, content={"message": f"{ex}"})
