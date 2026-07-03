import streamlit as st
from database.connection import engine
from utils.logger import logger

def render_sidebar():
    """Desenha a barra lateral informativa e conexões."""
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3004/3004613.png", width=80)
        st.title("Painel de Controle")
        st.markdown("---")
        st.subheader("🌐 Status do Sistema")
        
        # Testador dinâmico de conexão em tempo real com Neon.tech
        try:
            with engine.connect() as conn:
                st.success("Neon.tech: Conectado")
        except Exception as e:
            st.error("Neon.tech: Desconectado")
            logger.critical(f"Falha na conexão do painel visual: {str(e)}")
            
        st.markdown("---")
        st.markdown("### Configurações de IA")
        st.info("Visão Computacional Local ativa. Pronto para expansões corporativas.")