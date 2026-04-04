import urllib.parse

def generate_whatsapp_link(patient_nome, tendencia, justificativa):
    """
    Gera link real do WhatsApp Web com alerta clínico estruturado.
    """
    telefone = "5521998175736"
    texto = f"""🚨 *ALERTA CRÍTICO CTI*
Paciente: {patient_nome}
Tendência: {tendencia}
Justificativa: {justificativa}"""
    
    texto_codificado = urllib.parse.quote(texto)
    return f"https://wa.me/{telefone}?text={texto_codificado}"
