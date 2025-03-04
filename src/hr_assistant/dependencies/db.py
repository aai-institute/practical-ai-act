import psycopg2

from hr_assistant.config import settings


def db_conn() -> psycopg2.extensions.connection:
    conn = psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
    )
    return conn
