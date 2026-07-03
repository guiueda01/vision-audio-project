# VisionAI Engine — Streamlit Computer Vision & Audio Hub

Aplicação corporativa de alto desempenho para orquestração de rotinas em Visão Computacional (via OpenCV) e processamento automatizado de voz (Speech to Text usando o modelo otimizado `faster-whisper`), utilizando persistência relacional serverless no Neon.tech e infraestrutura PaaS na Render.

## 🚀 Tecnologias Empregadas
* **Linguagem:** Python 3.12+
* **Interface do Usuário:** Streamlit
* **Motores Analíticos:** OpenCV, NumPy, Pillow, Faster-Whisper
* **Mapeamento de Dados & ORM:** SQLAlchemy
* **Drivers de Conexão:** Psycopg (v3)
* **Banco de Dados:** PostgreSQL (Neon.tech Cloud Serverless)

## 🏢 Arquitetura de Software
O ecossistema segue rigorosamente os preceitos de modularidade e separação de conceitos inspirados na **Clean Architecture**:
* **UI Layer (`app.py`, `components/`)**: Renderização de tela livre de regras de negócio.
* **Controller Layer (`controllers/`)**: Orquestrador central que recebe os eventos e despacha fluxos.
* **Service Layer (`services/`)**: Implementação pura dos algoritmos de vídeo e áudio.
* **Repository Layer (`repositories/`)**: Encapsulamento de código SQL/ORM para persistência atômica.
* **Infrastructure Layer (`database/`, `config/`)**: Conexões de rede e chaves secretas.

## 📦 Instalação e Execução Local

1. Instale todas as dependências declaradas no arquivo de manifesto do projeto:
```bash
pip install -r requirements.txt