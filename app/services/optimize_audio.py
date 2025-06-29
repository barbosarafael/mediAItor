from pydub import AudioSegment, silence
from pydub.effects import normalize
import os
from io import BytesIO

def reduzir_taxa_amostragem(audio: AudioSegment, taxa=16000) -> AudioSegment:
    return audio.set_frame_rate(taxa)

def converter_para_mono(audio: AudioSegment) -> AudioSegment:
    return audio.set_channels(1)

def normalizar_volume(audio: AudioSegment) -> AudioSegment:
    return normalize(audio)

def remover_silencios(audio: AudioSegment, limiar_db: int = -40, padding_ms: int = 300) -> AudioSegment:
    # Detectar segmentos não silenciosos
    silencios = silence.detect_nonsilent(audio, min_silence_len=700, silence_thresh=limiar_db)
    # Unir os segmentos com padding
    partes = [audio[max(inicio - padding_ms, 0):fim + padding_ms] for inicio, fim in silencios]
    if partes:
        return sum(partes)
    return audio  # Caso não encontre silêncio, retorna original

def dividir_audio(audio: AudioSegment, duracao_max_segundos: int = 20) -> list[BytesIO]:
    """Divide um áudio em partes de até `duracao_max_segundos` segundos."""
    partes = []
    duracao_ms = duracao_max_segundos * 1000  # conversão correta para milissegundos

    for i in range(0, len(audio), duracao_ms):
        parte = audio[i:i + duracao_ms]
        buffer = BytesIO()
        parte.export(buffer, format="wav")
        buffer.seek(0)
        partes.append(buffer)

    return partes

def otimizar_e_dividir(caminho_audio: str, remover_arquivos: bool = False) -> list[str]:
    print(f"[🎧] Otimizando e dividindo áudio: {os.path.basename(caminho_audio)}")

    audio = AudioSegment.from_file(caminho_audio)
    audio = reduzir_taxa_amostragem(audio)
    audio = converter_para_mono(audio)
    audio = normalizar_volume(audio)
    audio = remover_silencios(audio)

    partes = dividir_audio(audio, duracao_max_segundos = 60)

    # Salvar partes em disco
    caminhos_salvos = []
    pasta_destino = "audios_otimizados"
    os.makedirs(pasta_destino, exist_ok=True)

    base_nome = os.path.splitext(os.path.basename(caminho_audio))[0]

    for i, parte in enumerate(partes):
        caminho_arquivo = os.path.join(pasta_destino, f"{base_nome}_parte_{i+1:03}.wav")
        with open(caminho_arquivo, "wb") as f:
            f.write(parte.read())
        caminhos_salvos.append(caminho_arquivo)

    print(f"[✅] Geradas {len(caminhos_salvos)} partes otimizadas.")
    return caminhos_salvos

def limpar_partes_otimizadas(caminhos: list[str]) -> None:
    for caminho in caminhos:
        try:
            os.remove(caminho)
        except Exception as e:
            print(f"[⚠️] Falha ao remover {caminho}: {e}")
