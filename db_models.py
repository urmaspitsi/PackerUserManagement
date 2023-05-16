from typing import Dict, Optional
from fastapi_users import models as md
from pydantic.networks import EmailStr

class User(md.BaseUser):
  meta_data: Dict = {}

class UserCreate(md.CreateUpdateDictModel):
    email: EmailStr
    password: str

class UserUpdate(md.CreateUpdateDictModel):
  meta_data: Optional[Dict]

class UserDB(User, md.BaseUserDB):
  meta_data: Dict = {}

