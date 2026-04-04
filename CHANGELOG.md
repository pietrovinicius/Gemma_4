# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-04-03
### Added
- **Alerta Crítico**: Implementado botão condicional de notificação assíncrona ao plantonista quando o motor IA (Gemma 4) detecta `🔴 PIORA`. 
  - `notifications.py`: Módulo mock do disparo de alerta para o WhatsApp (`send_whatsapp_alert`). Coberto por testes do `test_mvp.py` (simulando payloads lib `requests`).

## [0.2.0] - 2026-04-03
### Changed
- **UX/UI e Clean Code no Streamlit**: 
  - `app.py`: Refatoração baseada em Clean Code, extraindo componentes de renderização para funções modulares (`render_metrics`, `render_patient_card`). Uso aprimorado do `st.session_state` e `st.columns`/`st.metrics`.
  - `mock_data.py`: Inclusão da estrutura aninhada de `sinais_vitais` no mock para servir componentes numéricos diretos da UI.
  - **Identidade Visual**: Implementação de badges e emojis nativos (🟢 Melhora, 🟡 Estagnado, 🔴 Piora) para processamento rápido de status dinâmico.

## [0.1.0] - 2026-04-03
### Added
- **MVP Monitor CTI**: Criação da base estrutural da aplicação Streamlit.
  - `mock_data.py`: Geração de dados de pacientes sintéticos em memória (cenários de Ontem e Hoje).
  - `prompt_engine.py`: Motor de templates focado na estruturação do raciocínio analítico para o LLM.
  - `llm_client.py`: Integração do Ollama via streaming, consumindo a engine local `gemma4:4b`.
  - `app.py`: Fluxo completo do Streamlit, com login mockado, visualização modular de mapa de leitos e inferência.
- **Suíte de Testes**: Implementação de testes robustos (TDD) para validar os componentes do core.
  - `test_mvp.py`: Cobertura automatizada no diretório `mvp_monitor`, validando extração de dados e integridade de chamadas HTTP para API Ollama (com mocks).
