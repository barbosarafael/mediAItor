import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcrever_audio_openai(caminho_audio: str, idioma="pt") -> str:
    
    st.info("🔁 Enviando áudio para transcrição...")

    with open(caminho_audio, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=idioma,
            prompt="The next conversation is a medical consultation between a doctor and a patient or patients",
            response_format="text"
        )

    pasta_destino = "transcribe_audios"
    os.makedirs(pasta_destino, exist_ok=True)
    nome_base = os.path.splitext(os.path.basename(caminho_audio))[0]
    caminho_txt = os.path.join(pasta_destino, f"{nome_base}.txt")

    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(response)
        
    st.success(f"✅ Transcrição salva em: {caminho_txt}")


    return caminho_txt