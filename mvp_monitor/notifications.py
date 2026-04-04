from urllib.parse import quote
import re

def extract_nora(text):
    match = re.search(r'Noradrenalina\s*([0-9.,]+)', text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1).replace(',', '.'))
        except:
            return 0.0
    return 0.0

def generate_whatsapp_link(patient, tendencia, justificativa, usuario="Dr. Pietro", data="N/D"):
    """
    Gera link real do WhatsApp Web com alerta clínico estruturado e painéis comparativos.
    """
    telefone = "5521998175736"
    
    if "PIORA" in tendencia.upper():
        emoji_trend = "\U0001F534"
        trend_icon = "\U0001F4C9"
        header = "ALERTA CRÍTICO CTI"
    elif "MELHORA" in tendencia.upper():
        emoji_trend = "\U0001F7E2"
        trend_icon = "\U0001F4C8"
        header = "BOLETIM DE MELHORA CLÍNICA"
    else:
        emoji_trend = "\U0001F7E1"
        trend_icon = "\u2796"
        header = "INFORME CLÍNICO CTI"
        
    sinais = patient.get('dados_d0', {}).get('sinais_vitais', {})
    pa = sinais.get('pa', 'N/D')
    fc = sinais.get('fc', 'N/D')
    spo2 = sinais.get('spo2', 'N/D')
    temp = sinais.get('temp', 'N/D')

    d1_presc = patient.get('dados_d1', {}).get('prescricao', '')
    d0_presc = patient.get('dados_d0', {}).get('prescricao', '')
    nora_d1 = extract_nora(d1_presc)
    nora_d0 = extract_nora(d0_presc)
    
    nora_line = ""
    if nora_d0 > 0 or nora_d1 > 0:
        if nora_d0 > nora_d1:
            nora_status = "\u2B06\uFE0F subiu"
        elif nora_d0 < nora_d1:
            nora_status = "\u2B07\uFE0F caiu"
        else:
            nora_status = "\u2796 manteve"
        nora_line = f"\n- Noradrenalina: {nora_d0} mcg/kg/min ({nora_status})"
        
    texto = f"""{emoji_trend} *{header}*
-----------------------
*Data:* {data}
*Solicitante:* {usuario}
*Paciente:* {patient.get('nome', 'Desconhecido')} ({patient.get('leito', 'N/D')})
*Tendência:* {tendencia} {trend_icon}
-----------------------
*Sinais Atuais:*
- PA: {pa} mmHg
- FC: {fc} bpm | SpO2: {spo2}% | Temp: {temp}C{nora_line}
-----------------------
*Justificativa:* {justificativa}
-----------------------
\U0001F517 Acesse o painel: http://localhost:8501"""
    
    raw_msg = texto
    encoded_msg = quote(raw_msg.encode('utf-8'), safe='')
    return f"https://wa.me/{telefone}?text={encoded_msg}"
