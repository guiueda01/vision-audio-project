import os
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "images")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-dev-key")

    @classmethod
    def validate(cls):
        if not cls.DATABASE_URL:
            logger.error("A variável de ambiente DATABASE_URL não foi definida.")
            raise ValueError("DATABASE_URL crítica está ausente.")
        if not os.path.exists(cls.UPLOAD_FOLDER):
            os.makedirs(cls.UPLOAD_FOLDER)
            logger.info(f"Diretório de upload criado em: {cls.UPLOAD_FOLDER}")

Settings.validate()