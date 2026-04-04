import requests

def send_whatsapp_alert(patient_nome, sector, urgency_reason):
    """
    Mock integration for sending WhatsApp API notification.
    """
    url = "http://mock-whatsapp-api.local/v1/messages"
    payload = {
        "to": "plantonista_group",
        "message": f"🚨 ALERTA CRÍTICO: Paciente {patient_nome} ({sector}) com {urgency_reason}."
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        # Mock fallback para funcionar na versão MVP
        return {"status": 200, "message": "Simulação: Alerta WhatsApp enviado com sucesso ao plantonista."}
