import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resumo(caminho_transcricao: str) -> str:
    
    print("[📝] Gerando resumo da transcrição...")

    with open(caminho_transcricao, "r", encoding="utf-8") as f:
        texto = f.read()

    prompt_sistema = """Você é um assistente especializado em saúde. Gere um resumo claro e objetivo da consulta, contendo:

                        1. Contexto clínico do(a) paciente
                        2. Sintomas e queixas principais
                        3. Procedimentos e condutas aplicadas
                        4. Encaminhamentos ou próximos passos

                        Escreva em português claro, com frases completas, no estilo de anotações clínicas."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": texto}
        ],
        temperature=0.3
    )

    resumo = response.choices[0].message.content.strip()

    pasta_destino = "resume_transcribed_audios"
    os.makedirs(pasta_destino, exist_ok=True)
    nome_base = os.path.splitext(os.path.basename(caminho_transcricao))[0]
    caminho_resumo = os.path.join(pasta_destino, f"{nome_base}_resumo.txt")

    with open(caminho_resumo, "w", encoding="utf-8") as f:
        f.write(resumo)
        
    print(f"[✅] Resumo salvo em: {caminho_resumo}")


    return caminho_resumo