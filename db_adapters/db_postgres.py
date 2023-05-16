import databases
import os
import sqlalchemy
from utils import get_env_variable

# localhost or gcloud appengine environment
USE_LOCALHOST = False if os.environ.get("GAE_ENV") == "standard" else True

db_public_ip = get_env_variable("DATABASE_IP_ADDRESS")
database_name = get_env_variable("DATABASE_NAME")
db_username = get_env_variable("DATABASE_USERNAME")
db_password = get_env_variable("DATABASE_PASSWORD")
db_server_port = get_env_variable("DATABASE_SERVER_PORT")

HOST_SERVER = "localhost" if USE_LOCALHOST else db_public_ip

DATABASE_URL = f"postgresql://{db_username}:{db_password}@{HOST_SERVER}:{db_server_port}/{database_name}"

engine = sqlalchemy.create_engine(DATABASE_URL) #, pool_size=5, max_overflow=0)

database = databases.Database(DATABASE_URL)

