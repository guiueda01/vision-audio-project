from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from database.connection import Base
import datetime

class AnaliseModel(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    image_path = Column(String(500), nullable=False)
    descricao = Column(String(1000), nullable=True)
    objetos = Column(Text, nullable=True)  # Armazenado como string separada por vírgula
    quantidade_pessoas = Column(Integer, default=0)
    rostos = Column(Integer, default=0)
    idade = Column(String(50), nullable=True)
    emocao = Column(String(50), nullable=True)
    cores = Column(String(200), nullable=True)
    luminosidade = Column(String(50), nullable=True)
    nitidez = Column(String(50), nullable=True)
    transcricao = Column(Text, nullable=True)
    json_resultado = Column(JSON, nullable=True)