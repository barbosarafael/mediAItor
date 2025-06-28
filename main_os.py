from transcriber_os import transcrever_audio_local
from optimize_audio import otimizar_e_dividir
from app.services.summarizer import gerar_resumo
from pathlib import Path

if __name__ == "__main__":
    caminho_audio = "audios/Primeira consulta gestacional - Equipe de Enfermagem.mp3"

    if not Path(caminho_audio).exists():
        raise FileNotFoundError("❌ Áudio não encontrado.")

    caminho_transcricao = transcrever_audio_local(caminho_audio = caminho_audio, nome_base = "Primeira consulta gestacional - Equipe de Enfermagem - Audio cleaned")