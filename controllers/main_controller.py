from database.connection import SessionLocal
from repositories.analise_repository import AnaliseRepository
from services.vision_service import VisionService
from services.audio_service import AudioService
from models.analise import AnaliseModel
from utils.logger import logger
import datetime
from typing import List, Optional

class MainController:
    def __init__(self):
        self.vision_service = VisionService()
        self.audio_service = AudioService()

    def processar_fluxo_completo(self, image_bytes: bytes, audio_bytes: Optional[bytes]) -> Optional[dict]:
        """Orquestra o ciclo completo de negócio: Processamento CV -> Transcrição -> Persistência."""
        db = SessionLocal()
        try:
            # 1. Pipeline de Visão
            res_vision = self.vision_service.process_and_save(image_bytes)
            
            # 2. Pipeline de Áudio (se fornecido)
            transcricao_texto = ""
            if audio_bytes:
                transcricao_texto = self.audio_service.transcribe_audio_bytes(audio_bytes)
            
            # 3. Modelagem e Persistência
            analise_model = AnaliseModel(
                image_path=res_vision["image_path"],
                descricao=res_vision["descricao"],
                objetos=res_vision["objetos"],
                quantidade_pessoas=res_vision["quantidade_pessoas"],
                rostos=res_vision["rostos"],
                idade=res_vision["idade"],
                emocao=res_vision["emocao"],
                cores=res_vision["cores"],
                luminosidade=res_vision["luminosidade"],
                nitidez=res_vision["nitidez"],
                transcricao=transcricao_texto,
                json_resultado=res_vision
            )
            
            repo = AnaliseRepository(db)
            saved_model = repo.save(analise_model)
            
            res_vision["id"] = saved_model.id
            res_vision["transcricao"] = transcricao_texto
            return res_vision
            
        except Exception as e:
            logger.error(f"Falha de execução no fluxo orquestrado pelo Controller: {str(e)}")
            return None
        finally:
            db.close()

    def listar_historico(self, query: Optional[str] = None, start: Optional[datetime.date] = None, end: Optional[datetime.date] = None) -> List[AnaliseModel]:
        db = SessionLocal()
        try:
            repo = AnaliseRepository(db)
            return repo.get_all(search_query=query, start_date=start, end_date=end)
        finally:
            db.close()

    def excluir_registro(self, analise_id: int) -> bool:
        db = SessionLocal()
        try:
            repo = AnaliseRepository(db)
            return repo.delete(analise_id)
        finally:
            db.close()