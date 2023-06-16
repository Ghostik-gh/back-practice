from pydantic import (
    BaseSettings,
)
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

class Settings(BaseSettings):

    DB_PASSWORD = os.getenv('DB_PASSWORD')
    MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')
    MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
    HOST = os.getenv('HOST')
    PORT_DB = os.getenv('PORT_DB')
    PORT_MINIO = os.getenv('PORT_MINIO')
    PORT_APP = os.getenv('PORT_APP')

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings=Settings()
