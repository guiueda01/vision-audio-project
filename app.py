import streamlit as st
from config.settings import Settings
from database.connection import init_db
from controllers.main_controller import MainController
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from streamlit_mic_recorder import mic_recorder
import os
import json
import pandas as pd
from PIL import Image

# Configuração global de layout da página
st.set_page_config(page_title="VisionAI Engine", layout="wide", initial_sidebar_state="expanded")

# Garantia estrutural na inicialização do script
init_db()
controller = MainController()

# Renderização do menu lateral fixo
render_sidebar()

st.title("🧠 VisionAI Pro — Hub de Visão Computacional & Áudio")
st.write("Mapeamento automatizado de ambiente por fotografia integrado com reconhecimento de fala.")

# Inicialização de SessionState para gerenciar dados transitórios
if "foto_capturada" not in st.session_state:
    st.session_state.foto_capturada = None
if "audio_capturado" not in st.session_state:
    st.session_state.audio_capturado = None
if "ultimo_resultado" not in st.session_state:
    st.session_state.ultimo_resultado = None

# Organização da tela principal em abas (Tabs) para maior usabilidade
tab_captura, tab_historico = st.tabs(["📸 Captura & Análise", "🗄️ Histórico & Métricas"])

with tab_captura:
    col_esquerda, col_direita = st.columns([1, 1])
    
    with col_esquerda:
        st.subheader("Entrada de Dados")
        
        # Componente Nativo do Streamlit para Webcam
        camera_input = st.camera_input("Alinhe a câmera para captura de telemetria")
        
        st.write("🎵 **Instruções de Áudio:** Se desejar descrever a imagem por voz, grave seu comentário abaixo ANTES ou DEPOIS de disparar a foto.")
        
        # Gravador de áudio otimizado via HTML5 WebRTC injetado pelo componente
        audio_feed = mic_recorder(
            start_prompt="🔴 Iniciar Gravação de Voz",
            stop_prompt="⏹️ Encerrar Gravação",
            key="recorder",
            just_once=True
        )
        
        if audio_feed:
            st.session_state.audio_capturado = audio_feed['bytes']
            st.success("Áudio indexado ao buffer temporário com sucesso.")
            
        if camera_input:
            st.session_state.foto_capturada = camera_input.getvalue()
            
        st.markdown("---")
        if st.button("🚀 Processar Fluxo e Persistir", use_container_width=True):
            if st.session_state.foto_capturada is None:
                st.error("Erro: É obrigatório possuir uma imagem capturada pela câmera.")
            else:
                with st.spinner("Executando pipelines de Inteligência Algorítmica..."):
                    resultado = controller.processar_fluxo_completo(
                        image_bytes=st.session_state.foto_capturada,
                        audio_bytes=st.session_state.audio_capturado
                    )
                    if resultado:
                        st.session_state.ultimo_resultado = resultado
                        st.success("Análise persistida com sucesso na infraestrutura do Neon.tech!")
                        # Limpa buffers após gravação segura
                        st.session_state.foto_capturada = None
                        st.session_state.audio_capturado = None
                    else:
                        st.error("Ocorreu uma exceção inesperada durante a execução da pipeline. Verifique logs.")

    with col_direita:
        st.subheader("Resultados da Análise Atual")
        if st.session_state.ultimo_resultado:
            res = st.session_state.ultimo_resultado
            
            # Exibição dos KPI extraídos do OpenCV
            st.metric(label="Rostos Mapeados", value=res["rostos"])
            
            st.markdown(f"**📝 Descrição:** {res['descricao']}")
            st.markdown(f"**📦 Objetos Encontrados:** {res['objetos']}")
            st.markdown(f"**🎨 Cromatologia (Cores Predominantes):** {res['cores']}")
            st.markdown(f"**💡 Nível de Iluminação:** {res['luminosidade']}")
            st.markdown(f"**🔍 Foco/Nitidez:** {res['nitidez']}")
            
            st.markdown("---")
            st.markdown("🗣️ **Transcrição do Áudio de Observação:**")
            if res["transcricao"]:
                st.info(res["transcricao"])
            else:
                st.warning("Nenhuma nota de voz foi gravada para esta execução.")
        else:
            st.info("Aguardando captura e processamento para exibição de métricas analíticas.")

with tab_historico:
    st.subheader("🔍 Filtros de Consulta")
    
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        search_tx = st.text_input("Buscar por termos na descrição/objetos/transcrição")
    with col_f2:
        d_inicio = st.date_input("Data Inicial", value=None)
    with col_f3:
        d_fim = st.date_input("Data Final", value=None)
        
    # Consulta reativa ao banco de dados via controller
    registros = controller.listar_historico(query=search_tx, start=d_inicio, end=d_fim)
    
    # Seção de Exportações em Massa
    if registros:
        col_exp1, col_exp2 = st.columns(2)
        
        # Conversão rápida para Pandas estruturado para facilitar downloads
        export_data = [{
            "ID": r.id, "Data": r.created_at, "Descricao": r.descricao, 
            "Objetos": r.objetos, "Pessoas": r.quantidade_pessoas, 
            "Rostos": r.rostos, "Transcricao": r.transcricao
        } for r in registros]
        df_export = pd.DataFrame(export_data)
        
        with col_exp1:
            st.download_button("📥 Exportar Histórico para CSV", data=df_export.to_csv(index=False).encode('utf-8'), file_name="historico_cv.csv", mime="text/csv", use_container_width=True)
        with col_exp2:
            st.download_button("📥 Exportar Histórico para JSON", data=json.dumps(export_data, default=str, indent=4).encode('utf-8'), file_name="historico_cv.json", mime="application/json", use_container_width=True)
            
    st.markdown("---")
    
    # Renderização da lista dinâmica
    for reg in registros:
        with st.container():
            col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
            
            with col_c1:
                if os.path.exists(reg.image_path):
                    try:
                        img_pil = Image.open(reg.image_path)
                        st.image(img_pil, width=150, use_container_width=False)
                    except:
                        st.error("Erro ao carregar miniatura.")
                else:
                    st.warning("Ficheiro físico ausente.")
                    
            with col_c2:
                st.markdown(f"#### Registro ID: #{reg.id} — `{reg.created_at.strftime('%d/%m/%Y %H:%M:%S')}`")
                st.markdown(f"**Descrição:** {reg.descricao}")
                st.markdown(f"**Objetos:** {reg.objetos} | **Pessoas:** {reg.quantidade_pessoas}")
                if reg.transcricao:
                    st.caption(f"🗣️ Transcrição associada: {reg.transcricao}")
                    
            with col_c3:
                # Botão para Download do binário da imagem individual
                if os.path.exists(reg.image_path):
                    with open(reg.image_path, "rb") as f:
                        st.download_button("Download Img", data=f.read(), file_name=os.path.basename(reg.image_path), mime="image/png", key=f"dl_{reg.id}")
                        
                # Operação destrutiva com confirmação implícita via clique do Streamlit
                if st.button("Remover Registro", key=f"del_{reg.id}", type="secondary"):
                    if controller.excluir_registro(reg.id):
                        st.rerun()
            st.markdown("<hr style='margin: 0.5em 0px; border-color: rgba(49, 51, 63, 0.2);'>", unsafe_allow_html=True)

    # Injeção e carregamento do Dashboard de Métricas
    st.markdown("---")
    render_dashboard(registros)