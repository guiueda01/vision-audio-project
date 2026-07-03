from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import Settings
from utils.logger import logger

Base = declarative_base()

try:
    # Pool de conexões otimizado para arquiteturas Serverless como Neon.tech
    engine = create_engine(
        Settings.DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Engine de conexão do SQLAlchemy inicializada com sucesso para o Neon.tech.")
except Exception as e:
    logger.critical(f"Falha crítica ao inicializar banco de dados: {str(e)}")
    raise e

def init_db():
    """Garante a criação de todas as tabelas mapeadas automaticamente em runtime."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas do banco de dados validadas/criadas com sucesso via SQLAlchemy.")
    except Exception as e:
        logger.error(f"Erro ao inicializar tabelas (init_db): {str(e)}")
        raise e