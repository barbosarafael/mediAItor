import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
from app.services.optimize_audio import otimizar_e_dividir, limpar_partes_otimizadas

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcrever_audio_openai(caminho_audio: str, nome_base: str, idioma="pt") -> str:
    
    print("[🔁] Otimizando áudio para transcrição")
    
    caminhos_segmentos = otimizar_e_dividir(caminho_audio, remover_arquivos=True)
    
    transcricao_final = ""
    for i, caminho_parte in enumerate(caminhos_segmentos):
        print(f"[🧠] Transcrevendo parte {i+1}/{len(caminhos_segmentos)}: {os.path.basename(caminho_parte)}")

        with open(caminho_parte, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f, 
                language=idioma,
                prompt="The next conversation is a medical consultation between a doctor and a patient or patients",
                response_format="text"
            )
            transcricao_final += result + "\n\n"
    
    st.info("🔁 Enviando áudio para transcrição...")

    pasta_destino = "transcribe_audios"
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_txt = os.path.join(pasta_destino, f"{nome_base}.txt")

    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(transcricao_final.strip())
        
    st.success(f"✅ Transcrição salva em: {caminho_txt}")
    
    # Limpar arquivos temporários
    limpar_partes_otimizadas(caminhos_segmentos)

    return caminho_txt