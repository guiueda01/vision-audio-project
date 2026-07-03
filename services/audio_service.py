import os
import tempfile
from utils.logger import logger

class AudioService:
    def __init__(self):
        self.model = None
        self._initialized = False

    def _lazy_init(self):
        """Inicializa o modelo Whisper sob demanda para economizar RAM em inicialização fria."""
        if not self._initialized:
            try:
                from faster_whisper import WhisperModel
                # Usando tamanho mínimo (tiny) visando compatibilidade com limites de CPU/RAM gratuitos do Render
                self.model = WhisperModel("tiny", device="cpu", compute_type="float32")
                self._initialized = True
                logger.info("Modelo Faster-Whisper carregado dinamicamente com sucesso em CPU.")
            except Exception as e:
                logger.error(f"Erro ao carregar modelo Faster-Whisper: {str(e)}")
                self.model = None

    def transcribe_audio_bytes(self, audio_bytes: bytes) -> str:
        """Transcreve array de bytes brutos gravados diretamente do browser."""
        if not audio_bytes:
            return ""
        
        self._lazy_init()
        if not self.model:
            return "[Erro de infraestrutura: Modelo Whisper indisponível]"

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_bytes)
                temp_path = temp_audio.name

            # Execução do pipeline de reconhecimento de voz
            segments, info = self.model.transcribe(temp_path, beam_size=2)
            transcription = "".join([segment.text for segment in segments]).strip()
            
            try:
                os.remove(temp_path)
            except OSError:
                pass
                
            logger.info(f"Transcrição concluída com sucesso. Idioma detectado: {info.language}")
            return transcription if transcription else "[Áudio silencioso ou sem fala compreensível]"
        except Exception as e:
            logger.error(f"Erro durante a transcrição do áudio: {str(e)}")
            return f"[Falha ao transcrever: {str(e)}]"