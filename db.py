from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from db_models import UserDB, User

#import db_adapters.db_sqlite as db_source
import db_adapters.db_postgres as db_source

Base: DeclarativeMeta = declarative_base()

class UserTable(Base, SQLAlchemyBaseUserTable):
  # source: https://stackoverflow.com/questions/63894605/fastapi-users-auth-cant-add-extra-fields-for-register
  meta_data = Column(JSON)

engine = db_source.engine

Base.metadata.create_all(engine)

users = UserTable.__table__

database = db_source.database

async def get_user_db():
  yield SQLAlchemyUserDatabase(UserDB, database, users)
