import streamlit as st
from app.services.transcriber import transcrever_audio_openai
from app.services.summarizer import gerar_resumo
from pathlib import Path
import os

# Dados fixos de login
USUARIO_CORRETO = os.getenv("LOGIN")
SENHA_CORRETA = os.getenv("PASSWORD")

def login():
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            st.session_state["logado"] = True
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")

def logout():
    if st.button("Sair"):
        st.session_state["logado"] = False
        st.rerun()

def main_app():
    st.title("Plataforma de transcrição de consultas")

    logout()

    st.write("Faça upload da gravação da consulta médica para gerar a transcrição e o resumo.")

    audio_file = st.file_uploader("Selecione o arquivo de áudio (mp3, wav)", type=["mp3", "wav"])

    if audio_file is not None:
        # Salvar temporariamente o arquivo para processar
        pasta_audios = "uploaded_audios"
        os.makedirs(pasta_audios, exist_ok=True)
        caminho_audio = os.path.join(pasta_audios, audio_file.name)

        with open(caminho_audio, "wb") as f:
            f.write(audio_file.getbuffer())
            
        # Processar transcrição e resumo
        caminho_transcricao = transcrever_audio_openai(caminho_audio, nome_base = 'asdf')
        caminho_resumo = gerar_resumo(caminho_transcricao)

        # Ler resumo e mostrar
        with open(caminho_resumo, "r", encoding="utf-8") as f:
            resumo_texto = f.read()

        with st.expander("🔍 Ver resumo da consulta"):
            st.markdown(resumo_texto)
        
        # Ler resumo e mostrar
        with open(caminho_transcricao, "r", encoding="utf-8") as f:
            texto = f.read()
        
        with st.expander("🔍 Ver consulta completa"):
            st.text_area("", texto, height=400)


if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
else:
    main_app()
