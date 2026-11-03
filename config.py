import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-development-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/uber2_v2",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
