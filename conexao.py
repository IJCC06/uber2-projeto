from os import environ
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def criar_conexao():
    conn = psycopg2.connect(
        host = environ.get("DB_HOST"),
        database = environ.get("DB_NAME"),
        user=environ.get("DB_USER"),
        password = environ.get("DB_PASSWORD")
    )
    return conn