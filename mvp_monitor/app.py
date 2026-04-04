import streamlit as st
from mock_data import get_sectors, get_patients_by_sector, get_patient_by_id
from prompt_engine import build_clinical_prompt
from llm_client import stream_llm_analysis
from custom_logger import logger
from database import init_db, log_analysis_result

# Inicializa schema do BD e arquivo .db
init_db()

STATUS_EMOJI = {
    "Melhora": "🟢",
    "Estagnado": "🟡",
    "Piora": "🔴"
}

st.set_page_config(page_title="Monitor CTI", page_icon="🏥", layout="wide")

# --- GERENCIAMENTO DE ESTADO (ROTAS) ---
if "auth_status" not in st.session_state:
    st.session_state.auth_status = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "selected_sector" not in st.session_state:
    st.session_state.selected_sector = None
if "selected_patient_id" not in st.session_state:
    st.session_state.selected_patient_id = None

# --- FUNÇÕES DE NAVEGAÇÃO ---
def go_to(page, **kwargs):
    logger.info(f"Navegando para página: {page}")
    for key, value in kwargs.items():
        st.session_state[key] = value
    st.session_state.current_page = page
    st.rerun()

# --- COMPONENTES UI MODULARES ---
def render_metrics(title, vitals):
    st.subheader(title)
    cols = st.columns(4)
    cols[0].metric("PA (mmHg)", vitals.get("pa", "-"))
    cols[1].metric("FC (bpm)", vitals.get("fc", "-"))
    cols[2].metric("Temp (°C)", vitals.get("temp", "-"))
    cols[3].metric("SpO2 (%)", vitals.get("spo2", "-"))

def render_patient_card(patient):
    with st.container(border=True):
        col_nome, col_info, col_status, col_acao = st.columns([3, 2, 2, 2])
        col_nome.subheader(patient["nome"])
        col_info.write(f"Idade: {patient['idade']} | {patient['leito']}")
        
        status = patient.get("status_anterior", "Estagnado")
        emoji = STATUS_EMOJI.get(status, "🔵")
        col_status.write(f"Status Atual: {emoji} **{status}**")
        
        with col_acao:
            if st.button("Analisar Evolução 🧠", key=patient["id"]):
                go_to("analysis", selected_patient_id=patient["id"])

# --- TELAS DA MVP ---
def view_login():
    st.title("🏥 Acesso Restrito: Monitor CTI")
    st.info("Utilize **admin** e **1234** para entrar no protótipo.")
    
    with st.container():
        user = st.text_input("Usuário", value="admin")
        pwd = st.text_input("Senha", type="password", value="1234")
        if st.button("Autenticar 🔓", type="primary"):
            logger.info(f"Tentativa de login com usuário: {user}")
            if user == "admin" and pwd == "1234":
                go_to("sectors", auth_status=True)
            else:
                st.error("Credenciais inválidas.")

def view_sectors():
    st.title("🗂️ Seleção de Setores")
    sectors = get_sectors()
    cols = st.columns(len(sectors))
    
    for i, sec in enumerate(sectors):
        with cols[i]:
            if st.button(sec, width="stretch", key=sec):
                go_to("patients", selected_sector=sec)

def view_patients():
    sector = st.session_state.selected_sector
    st.button("⬅️ Trocar Setor", on_click=lambda: go_to("sectors"))
    
    st.title(f"🛏️ Mapa de Leitos - {sector}")
    patients = get_patients_by_sector(sector)
    
    if not patients:
        st.warning("Nenhum paciente neste setor no momento.")
        return
        
    for p in patients:
        render_patient_card(p)

def view_analysis():
    st.button("⬅️ Retornar aos Pacientes", on_click=lambda: go_to("patients"))
    p = get_patient_by_id(st.session_state.selected_patient_id)
    
    if not p:
        st.error("Paciente não encontrado.")
        return
        
    st.header(f"🩺 Análise Clínica Integrada - {p['nome']}")
    st.caption(f"{p['idade']} anos | Setor: {p['setor']} | {p['leito']}")
    
    d1 = p["dados_d1"]
    d0 = p["dados_d0"]
    
    # Prontuário Lado-a-Lado
    col_d1, col_d0 = st.columns(2)
    with col_d1:
        render_metrics("📊 Vitais D-1 (Ontem)", d1["sinais_vitais"])
        st.info(f"**Médica:** {d1['medica']}")
        st.warning(f"**Enfermagem:** {d1['enfermagem']}")
        st.error(f"**Prescrição:** {d1['prescricao']}")

    with col_d0:
        render_metrics("📊 Vitais D0 (Hoje)", d0["sinais_vitais"])
        st.info(f"**Médica:** {d0['medica']}")
        st.warning(f"**Enfermagem:** {d0['enfermagem']}")
        st.error(f"**Prescrição:** {d0['prescricao']}")

    st.divider()
    
    # LLM Interaction
    st.subheader("🤖 Inferência de Tendência (Gemma 4)")
    cache_key = f"cache_analise_{p['nome']}"
    
    if st.button("Processar com IA Local", type="primary"):
        with st.spinner("Motor IA Analisando prontuário..."):
            prompt = build_clinical_prompt(p)
            
            response_box = st.empty()
            full_response = ""
            verdict_time = None
            
            for chunk in stream_llm_analysis(prompt):
                if isinstance(chunk, dict) and "time_taken" in chunk:
                    verdict_time = chunk["time_taken"]
                else:
                    full_response += chunk
                    response_box.markdown(f"### Parecer IA \n\n {full_response}▌")
            
            # Limpa block temporario do stream
            response_box.empty()
            
            # Post-Process: assign matching visual badge block based on veredict
            status_badge = ""
            st.session_state.last_veredict_piora = False
            raw_status = "DESCONHECIDO"
            if "MELHORA" in full_response.upper():
                status_badge = "🟢 **TENDÊNCIA: MELHORA**"
                raw_status = "MELHORA"
            elif "PIORA" in full_response.upper():
                status_badge = "🔴 **TENDÊNCIA: PIORA**"
                raw_status = "PIORA"
                st.session_state.last_veredict_piora = True
            elif "ESTAGNADO" in full_response.upper():
                status_badge = "🟡 **TENDÊNCIA: ESTAGNADO**"
                raw_status = "ESTAGNADO"
                    
            analise_id = log_analysis_result(
                usuario="Dr. Pietro", # mock for phase 1 requirements
                modelo="gemma4:e4b",
                paciente=p["nome"],
                tendencia=raw_status,
                justificativa=full_response
            )
            st.session_state[f"last_analise_id_{p['nome']}"] = analise_id
            
            logger.info(f"Presistindo estado de sessao ux para analise de {p['nome']}")
            st.session_state[cache_key] = {
                "full_response": full_response,
                "status_badge": status_badge,
                "verdict_time": verdict_time
            }

    # -- Renderizacao Persistida da Analise --
    if cache_key in st.session_state:
        cd = st.session_state[cache_key]
        st.success(f"### Parecer Consolidado \n {cd['status_badge']} \n\n {cd['full_response']}")
        if cd['verdict_time'] is not None:
             st.caption(f"⏱️ Tempo de Inferência: **{cd['verdict_time']:.2f} segundos**")

    # Notificação do Plantonista para Piora
    if st.session_state.get("last_veredict_piora", False) and cache_key in st.session_state:
        st.warning("⚠️ **Alerta:** Riscos de Instabilidade Aguda detectados no raciocínio base.")
        from notifications import generate_whatsapp_link
        
        cd = st.session_state[cache_key]
        wpp_link = generate_whatsapp_link(
            patient_nome=p["nome"],
            tendencia="PIORA",
            justificativa=cd['full_response']
        )
        st.link_button("📲 Notificar Plantonista via WhatsApp", url=wpp_link, type="primary")
            
    st.divider()
    
    # Bloco RLHF
    analise_id_ativa = st.session_state.get(f"last_analise_id_{p['nome']}")
    if analise_id_ativa:
        fb_key = f"fb_{analise_id_ativa}"
        st.subheader("💡 Avalie a Resposta da IA (RLHF)")
        
        if st.session_state.get(f"{fb_key}_done"):
            st.success("Obrigado pelo seu feedback! Ele está nos ajudando a guiar melhores inferências clínicas futuras.")
        else:
            col_like, col_dislike, col_empty = st.columns([1, 1, 4])
            with col_like:
                if st.button("👍 Útil", key=f"btn_like_{analise_id_ativa}", width="stretch"):
                    from database import salvar_feedback
                    salvar_feedback(analise_id_ativa, "LIKE", "")
                    st.session_state[f"{fb_key}_done"] = True
                    st.rerun()
            with col_dislike:
                if st.button("👎 Precisa Melhorar", key=f"btn_dislike_{analise_id_ativa}", width="stretch"):
                    st.session_state[f"{fb_key}_show_motivo"] = True
                    
            if st.session_state.get(f"{fb_key}_show_motivo"):
                with st.form(key=f"form_dislike_{analise_id_ativa}"):
                    motivo = st.text_area("Descreva a análise clínica correta para que a IA aprenda com este erro:")
                    if st.form_submit_button("Submeter Crítica", type="primary"):
                        from database import salvar_feedback
                        salvar_feedback(analise_id_ativa, "DISLIKE", motivo)
                        st.session_state[f"{fb_key}_done"] = True
                        st.rerun()
                        
    st.divider()
    render_historico_paginado(p["nome"])

# --- COMPONENTE DE PAGINAÇÃO ---
def render_historico_paginado(paciente_nome):
    from database import get_analises_paciente, count_analises_paciente
    import pandas as pd
    import math
    st.subheader(f"📚 Histórico Retroativo de Consultas IA")
    
    if "pagina_historico" not in st.session_state:
        st.session_state.pagina_historico = 0
    
    limit = 10
    total = count_analises_paciente(paciente_nome)
    
    if total == 0:
        st.info("Nenhuma análise prévia para este paciente.")
        return
        
    total_pages = math.ceil(total / limit)
    offset = st.session_state.pagina_historico * limit
    
    analises = get_analises_paciente(paciente_nome, limit, offset)
    
    if analises:
        df = pd.DataFrame(analises)
        # Select clean columns to avoid clutter natively
        colunas_suportadas = ['id', 'data_hora', 'versao_modelo', 'tendencia', 'justificativa']
        df_visivel = df[[c for c in colunas_suportadas if c in df.columns]]
        st.dataframe(df_visivel, width="stretch", hide_index=True)
        
        for reg in analises:
            if reg.get("feedback_tipo") == "DISLIKE":
                with st.expander("⚠️ Divergência Clínica Detectada (IA vs Médico)"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.error("🤖 Parecer Original da IA")
                        st.write(reg.get("justificativa", ""))
                    with c2:
                        st.success("👨‍⚕️ Correção do Plantonista")
                        st.write(reg.get("feedback_motivo", ""))
                    if reg.get("feedback_data"):
                        st.caption(f"🗓️ Revisado em {reg['feedback_data']} — Aprendizado assimilado pelo Sistema.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Anterior", disabled=st.session_state.pagina_historico == 0):
            st.session_state.pagina_historico -= 1
            st.rerun()
    with col2:
        st.write(f"Página {st.session_state.pagina_historico + 1} de {total_pages}")
    with col3:
        if st.button("Próxima ➡️", disabled=st.session_state.pagina_historico >= total_pages - 1):
            st.session_state.pagina_historico += 1
            st.rerun()

# --- ROTEADOR ---
if not st.session_state.auth_status:
    view_login()
elif st.session_state.current_page == "sectors":
    view_sectors()
elif st.session_state.current_page == "patients":
    view_patients()
elif st.session_state.current_page == "analysis":
    view_analysis()
