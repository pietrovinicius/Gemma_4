def build_clinical_prompt(patient):
    from database import get_melhores_exemplos, get_ultimas_correcoes
    from custom_logger import logger
    
    d1 = patient['dados_d1']
    d0 = patient['dados_d0']
    
    exemplos = get_melhores_exemplos(limit=3)
    exemplos_str = ""
    
    if exemplos:
        logger.info(f"Otimizando prompt com {len(exemplos)} exemplos aprovados pelo RLHF (Few-Shot)")
        exemplos_str = "\n\nEXEMPLOS DE ANÁLISES APROVADAS PELO CORPO MÉDICO:\n"
        for i, ex in enumerate(exemplos):
            exemplos_str += f"""
--- Exemplo {i+1} ---
Paciente: {ex['paciente_nome']}
CLASSIFICACAO: {ex['tendencia']}
JUSTIFICATIVA: {ex['justificativa']}
"""
            
    correcoes = get_ultimas_correcoes(limit=2)
    correcoes_str = ""
    
    if correcoes:
        logger.info(f"Otimizando prompt com {len(correcoes)} correcoes médicas baseadas em disliks (Negative Few-Shot)")
        correcoes_str = "\n\nAPRENDIZADO POR CORREÇÃO MÉDICA:\nAtenção: Em casos anteriores, o corpo médico corrigiu suas falhas. Use as correções abaixo como guia do que NÃO fazer e qual o raciocínio correto esperado:\n"
        for i, corr in enumerate(correcoes):
            correcoes_str += f"""
--- Erro {i+1} ---
Paciente: {corr['paciente_nome']}
Assumiu Tendência: {corr['tendencia']}
Raciocínio Falho: {corr['justificativa']}
Correção Final do Médico: {corr['feedback_motivo']}
"""

    prompt = f"""Você é um sistema sênior de raciocínio clínico intensivo. Analise a evolução do paciente do Dia-1 para o Dia-0 e classifique a tendência clínica atual.

REGRAS ESTRITAS:
1. Retorne APENAS o bloco formatado abaixo, sem introdução ou conclusão.
2. Nas opções de [TENDÊNCIA], use estritamente: MELHORA, PIORA ou ESTAGNADO.
3. [JUSTIFICATIVA] deve ter de 2 a 3 linhas pontuando mudanças ou ausência de mudanças baseadas nas evidências clínicas apresentadas.

Referencial Clínico:
- MELHORA: Redução de Drogas Vasoativas (DVA), extubação/melhora ventilatória, melhora neurológica, hemodinâmica alvo alcançada.
- ESTAGNADO: Mesmos suportes (doses críticas inalteradas), estabilidade nos parâmetros (nem melhorou para desmame, nem apresentou choque novo).
- PIORA: Necessidade aumentada de DVA, queda abrupta de consciência, oligúria instalada, febre nova.{exemplos_str}{correcoes_str}

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
