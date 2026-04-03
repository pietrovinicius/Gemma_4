import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:4b"

def stream_llm_analysis(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "temperature": 0.1 # Temperatura baixa = menos alucinação, mais focado nos fatos
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line.decode('utf-8'))
                if "response" in decoded_line:
                    yield decoded_line["response"]
                    
    except requests.exceptions.RequestException as e:
        yield f"⚠️ Erro ao conectar no Gemma 4 local. Certifique-se que o Ollama está rodando e o modelo '{MODEL_NAME}' está no seu localhost:11434. \n\nErro interno: {str(e)}"
