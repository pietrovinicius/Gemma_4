import streamlit as st
from mock_data import get_sectors, get_patients_by_sector, get_patient_by_id
from prompt_engine import build_clinical_prompt
from llm_client import stream_llm_analysis

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
    for key, value in kwargs.items():
        st.session_state[key] = value
    st.session_state.current_page = page
    st.rerun()

# --- TELAS DA MVP ---
def view_login():
    st.title("🏥 Acesso Restrito: Monitor CTI")
    st.info("Utilize **admin** e **1234** para entrar no protótipo.")
    
    with st.container():
        user = st.text_input("Usuário", value="admin")
        pwd = st.text_input("Senha", type="password", value="1234")
        if st.button("Autenticar 🔓", type="primary"):
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
            if st.button(sec, use_container_width=True, key=sec):
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
        with st.container(border=True):
            col_nome, col_info, col_status, col_acao = st.columns([3, 2, 2, 2])
            col_nome.subheader(p["nome"])
            col_info.write(f"Idade: {p['idade']} | {p['leito']}")
            col_status.write(f"Status: **{p['status_anterior']}**")
            with col_acao:
                if st.button("Analisar Evolução 🧠", key=p["id"]):
                    go_to("analysis", selected_patient_id=p["id"])

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
        st.subheader("DIA -1 (Ontem)")
        st.info(f"**Médica:** {d1['medica']}")
        st.warning(f"**Enfermagem:** {d1['enfermagem']}")
        st.error(f"**Prescrição:** {d1['prescricao']}")

    with col_d0:
        st.subheader("DIA 0 (Hoje)")
        st.info(f"**Médica:** {d0['medica']}")
        st.warning(f"**Enfermagem:** {d0['enfermagem']}")
        st.error(f"**Prescrição:** {d0['prescricao']}")

    st.divider()
    
    # LLM Interaction
    st.subheader("🤖 Inferência de Tendência (Gemma 4)")
    if st.button("Processar com IA Local", type="primary"):
        with st.spinner("Motor IA Analisando prontuário..."):
            prompt = build_clinical_prompt(p)
            
            # Caixa estilizada onde montaremos o streaming da IA
            response_box = st.empty()
            full_response = ""
            
            for chunk in stream_llm_analysis(prompt):
                full_response += chunk
                # Adiciona o cursor piscante "▌" simulando terminal
                response_box.markdown(f"### Parecer IA \n\n {full_response}▌")
            
            # Remove o cursor pós-término
            response_box.success(f"### Parecer Consolidado \n {full_response}")

# --- ROTEADOR ---
if not st.session_state.auth_status:
    view_login()
elif st.session_state.current_page == "sectors":
    view_sectors()
elif st.session_state.current_page == "patients":
    view_patients()
elif st.session_state.current_page == "analysis":
    view_analysis()
