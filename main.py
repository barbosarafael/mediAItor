from app.services.transcriber import transcrever_audio_openai
from app.services.summarizer import gerar_resumo
from pathlib import Path

if __name__ == "__main__":
    caminho_audio = "audios/Primeira consulta gestacional - Equipe de Enfermagem.mp3"

    if not Path(caminho_audio).exists():
        raise FileNotFoundError("❌ Áudio não encontrado.")

    caminho_transcricao = transcrever_audio_openai(caminho_audio)
    caminho_resumo = gerar_resumo(caminho_transcricao)