from pydantic import (
    BaseSettings,
)
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

class Settings(BaseSettings):
    MINIO_ROOT_USER=os.getenv('MINIO_ROOT_USER')
    MINIO_ROOT_PASSWORD=os.getenv('MINIO_ROOT_PASSWORD')
    RABBITMQ_DEFAULT_USER=os.getenv('RABBITMQ_DEFAULT_USER')
    RABBITMQ_DEFAULT_PASS=os.getenv('RABBITMQ_DEFAULT_PASS')
    DSN_POSTGRE=os.getenv('DSN_POSTGRE')
    ENDPOINT_MINIO=os.getenv('ENDPOINT_MINIO')
    HOST_RABBITMQ=os.getenv('HOST_RABBITMQ')
    HOST=os.getenv('HOST')
    PORT_RABBITMQ=os.getenv('PORT_RABBITMQ')

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings=Settings()
