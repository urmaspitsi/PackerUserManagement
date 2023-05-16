import databases
import sqlalchemy

DATABASE_URL = "sqlite:////tmp/users.db" #Local location C:\temp, gcloud location: /tmp
# source: https://cloud.google.com/appengine/docs/standard/python3/using-temp-files

database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
