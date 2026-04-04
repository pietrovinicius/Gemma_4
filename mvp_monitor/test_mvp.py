import pytest
from unittest.mock import patch, MagicMock
import json

from mock_data import get_sectors, get_patients_by_sector, get_patient_by_id, get_mock_patients
from prompt_engine import build_clinical_prompt
from llm_client import stream_llm_analysis

def test_mock_data_get_sectors():
    sectors = get_sectors()
    assert isinstance(sectors, list)
    assert "CTI Geral" in sectors

def test_mock_data_get_patients_by_sector():
    patients = get_patients_by_sector("CTI Geral")
    assert isinstance(patients, list)
    assert all(p["setor"] == "CTI Geral" for p in patients)

def test_mock_data_get_patient_by_id():
    patient = get_patient_by_id(1)
    assert patient is not None
    assert patient["nome"] == "João Silva"
    
    # Assert vitals structure is present for UI metrics
    assert "sinais_vitais" in patient["dados_d1"]
    assert "fc" in patient["dados_d1"]["sinais_vitais"]
    assert "pa" in patient["dados_d1"]["sinais_vitais"]
    assert "temp" in patient["dados_d1"]["sinais_vitais"]
    
    patient_not_found = get_patient_by_id(999)
    assert patient_not_found is None

def test_prompt_engine_structure():
    patient = get_patient_by_id(1)
    prompt = build_clinical_prompt(patient)
    assert "Evolução Médica" in prompt
    assert patient['dados_d1']['medica'] in prompt
    assert patient['dados_d0']['medica'] in prompt
    assert "MELHORA" in prompt
    assert "CLASSIFICACAO:" in prompt

@patch("llm_client.requests.post")
def test_stream_llm_analysis_success(mock_post):
    mock_response = MagicMock()
    
    mock_lines = [
        json.dumps({"response": "CLASSIFICACAO: "}).encode('utf-8'),
        json.dumps({"response": "MELHORA\n"}).encode('utf-8'),
        json.dumps({"response": "JUSTIFICATIVA: "}).encode('utf-8'),
        json.dumps({"response": "Redução da noradrenalina."}).encode('utf-8')
    ]
    mock_response.iter_lines.return_value = mock_lines
    mock_response.raise_for_status = MagicMock()
    
    mock_post.return_value = mock_response
    
    prompt = "Teste"
    result = list(stream_llm_analysis(prompt))
    
    assert len(result) == 5
    assert result[0] == "CLASSIFICACAO: "
    assert result[1] == "MELHORA\n"
    assert isinstance(result[-1], dict)
    assert "time_taken" in result[-1]
    mock_post.assert_called_once()

@patch("llm_client.requests.post")
def test_stream_llm_analysis_exception(mock_post):
    import requests
    mock_post.side_effect = requests.exceptions.ConnectionError("Failed to connect")
    
    prompt = "Teste"
    result = list(stream_llm_analysis(prompt))
    
    assert len(result) == 1
    assert "Erro ao conectar" in result[0]

@patch("notifications.requests.post")
def test_send_whatsapp_alert_success(mock_post):
    from notifications import send_whatsapp_alert
    
    # Mocking standard WhatsApp API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": 200, "message": "Enviado com sucesso"}
    mock_post.return_value = mock_response
    
    response = send_whatsapp_alert("João Silva", "CTI Geral", "Piora aguda detectada")
    
    assert response["status"] == 200
    assert "sucesso" in response["message"].lower()
    mock_post.assert_called_once()

def test_logger_format_and_file():
    from custom_logger import get_logger
    import os
    import re
    import time
    
    # Log path is at project root
    log_path = "/Users/pietrodapenhadelima/Projetos/Gemma_4/log.txt"
    if os.path.exists(log_path):
        os.remove(log_path)
    
    logger = get_logger("TEST_LOGGER")
    logger.info("Verificando formato estrito de log yyyy/mm/dd")
    
    assert os.path.exists(log_path)
    with open(log_path, "r") as f:
        content = f.read()
        
    # Check "yyyy/mm/dd HH:MM:SS - [INFO] - "
    match = re.search(r"(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) - \[(INFO)\] - (.*)", content)
    assert match is not None, "Log did not match the strict format requirement"
    assert "Verificando formato estrito" in match.group(3)

def test_database_creation_and_insertion():
    from database import get_connection, init_db, log_analysis_result
    import sqlite3
    
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    
    log_analysis_result(
        conn=conn,
        usuario="Dr. Pietro",
        modelo="gemma4:e4b",
        paciente="João Silva",
        tendencia="MELHORA",
        justificativa="Redução de aminas..."
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM historico_analises")
    rows = cursor.fetchall()
    
    assert len(rows) == 1
    assert rows[0][2] == "Dr. Pietro"
    assert rows[0][4] == "João Silva"
    assert rows[0][5] == "MELHORA"
    conn.close()

    # Remove old untested test assert analises[0]["paciente_nome"] == "Teste2"
def test_paginated_patient_history():
    from database import init_db, log_analysis_result, get_analises_paciente, count_analises_paciente
    import sqlite3
    
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    
    for i in range(3):
        log_analysis_result(
            conn=conn, usuario="Dr. Pietro", modelo="gemma4", paciente="João",
            tendencia="MELHORA", justificativa=f"Teste {i}"
        )
    log_analysis_result(
        conn=conn, usuario="Dr. Pietro", modelo="gemma4", paciente="Maria",
        tendencia="PIORA", justificativa="Teste Maria"
    )
    
    count_joao = count_analises_paciente("João", conn)
    assert count_joao == 3
    
    page_1 = get_analises_paciente("João", 2, 0, conn)
    assert len(page_1) == 2
    
    page_2 = get_analises_paciente("João", 2, 2, conn)
    assert len(page_2) == 1
    
    conn.close()

def test_rlhf_feedback():
    from database import init_db, log_analysis_result, salvar_feedback
    import sqlite3
    
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    
    analise_id = log_analysis_result(
        conn=conn, usuario="Dr. Pietro", modelo="gemma4", paciente="João",
        tendencia="MELHORA", justificativa="Teste RLHF"
    )
    
    assert analise_id is not None
    
    # Primeiro envio aceito
    success = salvar_feedback(analise_id, "LIKE", "", conn=conn)
    assert success is True
    
    # Envio duplo mitigado
    success_dup = salvar_feedback(analise_id, "DISLIKE", "Erro posterior", conn=conn)
    assert success_dup is False
    
    cursor = conn.cursor()
    cursor.execute("SELECT feedback_tipo FROM historico_analises WHERE id = ?", (analise_id,))
    tipo = cursor.fetchone()[0]
    
    assert tipo == "LIKE"
    conn.close()


