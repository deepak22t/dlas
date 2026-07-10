from sqlalchemy import text
from app.database.session import engine

def check_database_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
