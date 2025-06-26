from pyannote.audio import Pipeline
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 1. Transcrição com OpenAI
def transcrever_com_openai(caminho_audio):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open(caminho_audio, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",  # importante para pegar timestamps
            language="pt"
        )
    return response

# 2. Diarização com pyannote
def diarizar_voz(caminho_audio):
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=hf_token)
    diarization = pipeline(caminho_audio)
    
    segmentos = []
    for turn in diarization.itertracks(yield_label=True):
        start = turn[0].start
        end = turn[0].end
        speaker = turn[2]
        segmentos.append({
            "start": start,
            "end": end,
            "speaker": speaker
        })
    return segmentos

# 3. Combina transcrição e falantes
def combinar(transcricao, diarizacao):
    # Converter o objeto TranscriptionVerbose para dict
    transcricao_dict = transcricao.dict()
    
    texto_final = []
    for segmento in transcricao_dict["segments"]:
        trecho_inicio = segmento["start"]
        trecho_fim = segmento["end"]
        texto = segmento["text"]

        # Busca o falante que corresponde ao intervalo
        falante = "Desconhecido"
        for d in diarizacao:
            if d["start"] <= trecho_inicio <= d["end"]:
                falante = d["speaker"]
                break

        texto_final.append(f"- {falante}: {texto}")
    
    return "\n".join(texto_final)


# 4. Executa tudo
if __name__ == "__main__":
    caminho_audio = "audios/limpo.mp3"
    print("[1️⃣] Transcrevendo com OpenAI...")
    transcricao = transcrever_com_openai(caminho_audio)

    print("[2️⃣] Rodando diarização com pyannote...")
    diarizacao = diarizar_voz(caminho_audio)

    print("[3️⃣] Combinando transcrição com falantes...")
    saida_formatada = combinar(transcricao, diarizacao)

    print("\n💬 Conversa formatada:\n")
    print(saida_formatada)