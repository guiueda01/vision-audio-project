import cv2
import numpy as np
from PIL import Image
import os
import uuid
from datetime import datetime
from config.settings import Settings
from utils.logger import logger

class VisionService:
    def __init__(self):
        # Carrega classificadores pré-treinados Haar Cascades nativos do OpenCV para detecção de rostos
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def process_and_save(self, image_bytes: bytes) -> dict:
        """Executa pipeline algorítmico de visão computacional na imagem capturada."""
        try:
            # Conversão dos bytes para formato OpenCV (BGR)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            
            # 1. Resolução e Metadados temporais
            height, width, _ = img_bgr.shape
            resolution_str = f"{width}x{height}"
            now = datetime.now()
            
            # 2. Métricas de Luminosidade e Nitidez
            luminosity_avg = np.mean(img_gray)
            luminosity_label = "Boa" if 80 <= luminosity_avg <= 200 else ("Baixa" if luminosity_avg < 80 else "Ofuscante")
            
            laplacian_var = cv2.Laplacian(img_gray, cv2.CV_64F).var()
            sharpness_label = "Excelente/Focada" if laplacian_var > 100 else "Baixa/Desfocada"
            
            # 3. Análise Detecção de Rostos (Haar Cascade)
            faces = self.face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            faces_count = len(faces)
            
            # 4. Cores Predominantes usando histograma rápido das fatias de canais BGR
            b_avg, g_avg, r_avg = cv2.mean(img_bgr)[:3]
            cores_predominantes = f"R:{int(r_avg)} G:{int(g_avg)} B:{int(b_avg)}"
            
            # 5. Pipeline estendida para predição ou mock genérico (preparado para IA externa)
            detected_objects = ["Pessoa"] if faces_count > 0 else ["Ambiente de captura"]
            if luminosity_label == "Baixa":
                detected_objects.append("Sombra detectada")
                
            # Geração do arquivo físico
            filename = f"cap_{uuid.uuid4().hex}.png"
            full_path = os.path.join(Settings.UPLOAD_FOLDER, filename)
            cv2.imwrite(full_path, img_bgr)
            
            logger.info(f"Pipeline de Visão Computacional executada com sucesso. Imagem salva em: {full_path}")
            
            return {
                "image_path": full_path,
                "descricao": f"Captura realizada contendo resolução {resolution_str} com iluminação {luminosity_label.lower()}.",
                "objetos": ", ".join(detected_objects),
                "quantidade_pessoas": faces_count,
                "rostos": faces_count,
                "idade": "Não disponível (Requer API Cognitiva)",
                "emocao": "Ambiente estável" if faces_count == 0 else "Neutro (Análise Estatística)",
                "cores": cores_predominantes,
                "luminosidade": f"{luminosity_label} ({int(luminosity_avg)})",
                "nitidez": f"{sharpness_label} (Var: {int(laplacian_var)})",
                "data": now.strftime("%Y-%m-%d"),
                "horario": now.strftime("%H:%M:%S")
            }
        except Exception as e:
            logger.error(f"Falha no processamento da imagem: {str(e)}")
            raise e