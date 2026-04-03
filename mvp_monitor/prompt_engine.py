def build_clinical_prompt(patient):
    d1 = patient['dados_d1']
    d0 = patient['dados_d0']
    
    prompt = f"""Você é um sistema sênior de raciocínio clínico intensivo. Analise a evolução do paciente do Dia-1 para o Dia-0 e classifique a tendência clínica atual.

REGRAS ESTRITAS:
1. Retorne APENAS o bloco formatado abaixo, sem introdução ou conclusão.
2. Nas opções de [TENDÊNCIA], use estritamente: MELHORA, PIORA ou ESTAGNADO.
3. [JUSTIFICATIVA] deve ter de 2 a 3 linhas pontuando mudanças ou ausência de mudanças baseadas nas evidências clínicas apresentadas.

Referencial Clínico:
- MELHORA: Redução de Drogas Vasoativas (DVA), extubação/melhora ventilatória, melhora neurológica, hemodinâmica alvo alcançada.
- ESTAGNADO: Mesmos suportes (doses críticas inalteradas), estabilidade nos parâmetros (nem melhorou para desmame, nem apresentou choque novo).
- PIORA: Necessidade aumentada de DVA, queda abrupta de consciência, oligúria instalada, febre nova.

DADOS PACIENTE:
--- DIA -1 (Ontem) ---
Evolução Médica: {d1['medica']}
Evolução Enfermagem: {d1['enfermagem']}
Prescrição Crítica: {d1['prescricao']}

--- DIA 0 (Hoje) ---
Evolução Médica: {d0['medica']}
Evolução Enfermagem: {d0['enfermagem']}
Prescrição Crítica: {d0['prescricao']}

Por favor, forneça o veredito no seguinte formato:
CLASSIFICACAO: [TENDÊNCIA]
JUSTIFICATIVA: [JUSTIFICATIVA]
"""
    return prompt
