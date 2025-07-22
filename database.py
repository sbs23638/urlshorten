import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
