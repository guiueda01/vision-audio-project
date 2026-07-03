from sqlalchemy.orm import Session
from models.analise import AnaliseModel
from utils.logger import logger
from typing import List, Optional
import datetime

class AnaliseRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, model: AnaliseModel) -> AnaliseModel:
        """Persiste um novo registro de análise no banco Neon.tech."""
        try:
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            logger.info(f"Registro ID {model.id} inserido com sucesso no PostgreSQL.")
            return model
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar análise no repositório: {str(e)}")
            raise e

    def get_all(self, search_query: Optional[str] = None, start_date: Optional[datetime.date] = None, end_date: Optional[datetime.date] = None) -> List[AnaliseModel]:
        """Recupera e filtra os registros com filtros aplicados dinamicamente."""
        try:
            query = self.db.query(AnaliseModel)
            
            if search_query:
                query = query.filter(
                    (AnaliseModel.descricao.ilike(f"%{search_query}%")) | 
                    (AnaliseModel.objetos.ilike(f"%{search_query}%")) |
                    (AnaliseModel.transcricao.ilike(f"%{search_query}%"))
                )
                
            if start_date:
                query = query.filter(AnaliseModel.created_at >= datetime.datetime.combine(start_date, datetime.time.min))
            if end_date:
                query = query.filter(AnaliseModel.created_at <= datetime.datetime.combine(end_date, datetime.time.max))
                
            return query.order_by(AnaliseModel.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Erro ao buscar registros no repositório: {str(e)}")
            return []

    def delete(self, analise_id: int) -> bool:
        """Deleta permanentemente o registro do banco."""
        try:
            model = self.db.query(AnaliseModel).filter(AnaliseModel.id == analise_id).first()
            if model:
                self.db.delete(model)
                self.db.commit()
                logger.info(f"Registro ID {analise_id} removido do banco.")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao deletar ID {analise_id}: {str(e)}")
            return False