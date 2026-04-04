import requests
import json
import time
from custom_logger import logger

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:e4b"

def stream_llm_analysis(prompt):
    logger.info(f"Iniciando chamada HTTP assíncrona para LLM {MODEL_NAME}")
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "temperature": 0.1
    }
    
    start_time = time.time()
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line.decode('utf-8'))
                if "response" in decoded_line:
                    yield decoded_line["response"]
                    
        elapsed = time.time() - start_time
        logger.info(f"Inferência concluída. Tempo total: {elapsed:.2f}s")
        yield {"time_taken": elapsed}
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Falha de conexão com API do Ollama: {str(e)}")
        yield f"⚠️ Erro ao conectar no Gemma 4 local. Certifique-se que o Ollama está rodando e o modelo '{MODEL_NAME}' está no seu localhost:11434. \n\nErro interno: {str(e)}"
