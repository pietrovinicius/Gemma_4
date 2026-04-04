import pytest
from mock_data import get_patient_by_id
from prompt_engine import build_clinical_prompt
from llm_client import stream_llm_analysis

def test_ollama_real_integration():
    """
    Integration test calling the actual local Ollama server on localhost:11434
    Requires: Ollama running with 'gemma4:e4b' installed.
    """
    # 1. Fetch "Carlos Mendes" (ID 3)
    patient = get_patient_by_id(3)
    assert patient is not None, "Patient not found in mock data"
    assert patient["nome"] == "Carlos Mendes"

    # 2. Build the exact prompt used by the App
    prompt = build_clinical_prompt(patient)

    # 3. Request LLM generation via the real network stream
    chunks = list(stream_llm_analysis(prompt))
    
    # Check if we got the connection error fallback
    error_str = "Erro ao conectar"
    fallback_detected = any(error_str in chunk for chunk in chunks)
    
    # We should NOT get connection error in a real healthy environment
    assert not fallback_detected, "Could not connect to Ollama. Ensure localhost:11434 is running and model exists."
    
    # Output should not be empty
    full_text = "".join(chunks)
    assert len(full_text) > 10, "Response from Gemma is too short or empty."
    
    # Print for debugging context
    print("\n--- LLM REAL OUTPUT ---")
    print(full_text)
    print("-----------------------")
