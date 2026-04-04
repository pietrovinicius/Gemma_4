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

def generate_whatsapp_link(patient, tendencia, justificativa):
    """
    Gera link real do WhatsApp Web com alerta clínico estruturado e painéis comparativos.
    """
    telefone = "5521998175736"
    
    if "PIORA" in tendencia.upper():
        emoji_trend = "🔴"
        trend_icon = "📉"
    elif "MELHORA" in tendencia.upper():
        emoji_trend = "🟢"
        trend_icon = "📈"
    else:
        emoji_trend = "🟡"
        trend_icon = "➖"
        
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
            nora_status = "⬆️ subiu"
        elif nora_d0 < nora_d1:
            nora_status = "⬇️ caiu"
        else:
            nora_status = "➖ manteve"
        nora_line = f"\n- Noradrenalina: {nora_d0} mcg/kg/min ({nora_status})"
        
    texto = f"""{emoji_trend} *ALERTA CRÍTICO CTI*
-----------------------
*Paciente:* {patient.get('nome', 'Desconhecido')} ({patient.get('leito', 'N/D')})
*Tendência:* {tendencia} {trend_icon}
-----------------------
*Sinais Atuais:*
- PA: {pa} mmHg
- FC: {fc} bpm | SpO2: {spo2}% | Temp: {temp}C{nora_line}
-----------------------
*Justificativa:* {justificativa}
-----------------------
🔗 Acesse o painel: http://localhost:8501"""
    
    texto_codificado = quote(texto, safe='')
    return f"https://wa.me/{telefone}?text={texto_codificado}"
