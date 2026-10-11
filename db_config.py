import os
from dotenv import load_dotenv
import psycopg2


def get_connection():
    load_dotenv()
    DATABASE_PASS = os.getenv("DATABASE_PASSWORD")

    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "recommander_system"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "DATABASE_PASS"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
    )
