import whisper
import os

from optimize_audio import otimizar_e_dividir, limpar_partes_otimizadas

def transcrever_audio_local(caminho_audio: str, nome_base: str) -> str:
    print("[🔁] Otimizando áudio para transcrição local com Whisper...")
    caminhos_segmentos = otimizar_e_dividir(caminho_audio)

    model = whisper.load_model("large")  # ou "small", "medium", "large"
    transcricao_final = ""

    for i, caminho_parte in enumerate(caminhos_segmentos):
        print(f"[🧠] Transcrevendo parte {i+1}/{len(caminhos_segmentos)}: {os.path.basename(caminho_parte)}")
        result = model.transcribe(caminho_parte, language="pt")
        transcricao_final += result["text"].strip() + "\n\n"

    # Salvar o texto final da transcrição
    pasta_destino = "transcribe_audios_os"
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_txt = os.path.join(pasta_destino, f"{nome_base}.txt")

    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(transcricao_final.strip())

    print(f"[✅] Transcrição salva em: {caminho_txt}")

    # Limpar arquivos temporários
    limpar_partes_otimizadas(caminhos_segmentos)

    return caminho_txt
