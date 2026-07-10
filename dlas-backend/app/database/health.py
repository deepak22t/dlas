from sqlalchemy import text
from app.database.session import engine

def check_database_connection():
    try:
        with engine.connect() as connection:
          connection.execute(text("SELECT 1"))
          print("Database Connected")
    except Exception as e:
        print("Database Connection Failed")
        raise
