# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.17.0] - 2026-04-03
### Added
- **Expansão Dinâmica do Tracking de Comunicação**:
  - Removido o filtro rígido de "Apenas PIORA" na Interface do `app.py`. Agora, independentemente do veredito (Melhora, Estagnado ou Piora), a plataforma oferece um trigger acoplado para notificar via WhatsApp Web com botões adaptativos de UX (vermelho para perigo, cinza para informes tranquilos).
  - O cabeçalho na URL de `notifications.py` tornou-se inteligente convertendo "ALERTA CRÍTICO" em "BOLETIM DE MELHORA" conforma o status atual do banco.
  - A lógica unificada atualiza todos os laudos no histórico para ✅ / ❌ ao invés de pular o checklist visual para pacientes estáveis.

## [0.16.1] - 2026-04-03
### Changed
- **Automação Combinada UI/UX**:
  - Transformação do fluxo fragmentado ("Gerar Link" vs "Registrar") em um único botão atômico de Interface: `Disparar Alerta WhatsApp e Selar Registro`.
  - Processo engatilha assincronamente a marcação da Flag no SQLite `confirmar_envio_whatsapp(analise_id_ativa)` e simultaneamente força a injeção do componente front end custom em JS renderizando a API nativa de WhatsApp.
  - O DataFrame histórico processa o update vertical instantaneamente garantindo que a Tabela Histórica inferior identifique "Enviado" logo ao redesenhar sem st.reruns abruptos.

## [0.16.0] - 2026-04-03
### Added
- **Rastreio Operacional de Alertas Críticos**:
  - Tabela `historico_analises` evoluída (ALTER TABLE nativo em `init_db`) adicionando coluna de flag `whatsapp_enviado`.
  - Frontend remodelado no `app.py` com separação de fluxo ("🔗 Abrir WhatsApp Web" e "✅ Registrar Envio Concluído") garantindo isolamento da API nativa de mensageria com o log auditável do sistema.
  - Tabela de Histórico (DataFrame de baixo nível) interceptando as colunas e inserindo status visuais (`❌ Pendente` \ `✅ Enviado`) automaticamente após chamadas de `st.rerun()`. Teste validado via suíte fechada em `test_whatsapp_tracking`.

## [0.15.0] - 2026-04-03
### Added
- **Rastreabilidade Dinâmica via WhatsApp**:
  - Incorporada Injeção Dinâmica dos metadados de auditoria. Agora todas as notificações emitidas contam com timestamp e Solicitante no cabeçalho embutidos no corpo do HTTPS, extraídos dos logs ativos e do `session_state`.
  - Tratamento contínuo de safe parsing garantido contra falsos decodings Unicode em modais externos.

## [0.14.1] - 2026-04-03
### Fixed
- **Encoding de URL do WhatsApp**:
  - Corrigida fragilidade de compatibilidade no `urllib.parse` onde quebras de linha (`\n`) e emojis complexos (🔴, 📈) podiam quebrar a concatenação da rota API em modais ou devices mais estritos. Adicionado mapeamento via `quote(safe='')` forçando o parse universal de caracteres unicode no formato percent-encoding `%0A`.

## [0.14.0] - 2026-04-03
### Refactor
- **Template Whatsapp de Alta Performance**:
  - Reformulação do `notifications.py` implementando expressões regulares (`re.search()`) para extrair a Noradrenalina da prescrição médica, mapeando se subiu (⬆️), caiu (⬇️) ou acompanhou (➖) dentro das tramas de texto cru de mock\_data.
  - O script passa a montar um painel formatado de Plantão resgatando o dict completo de paciente via `kwargs` em `app.py`. A URL incorpora suporte a sinais vitais em linha como PA, FC, Temp e SpO2 com blocos de separador visual para Leitura Rápida durante Intercorrência de CTI.

## [0.13.0] - 2026-04-03
### Changed
- **Integração Real de Gatilhos de Alerta via WhatsApp Web**:
  - Conversão do simulador estático HTTP para um construtor nativo via `urllib.parse` para montagem dinâmica de links HTTPS da API do WhatsApp.
  - Na tela de Piora Clínica, o botão genérico Streamlit foi injetado como um `st.link_button`. 
  - Ao invés de uma chamada falsa, clicar propaga o Plantonista direto para seu App de Mensagens com um template pré-preenchido repassando a TENDÊNCIA, o NOME DO PACIENTE e a JUSTIFICATIVA EXATA elaborada pela IA.

## [0.12.0] - 2026-04-03
### Added
- **Painel de Confronto de Ideias (Transparência Cognitiva)**:
  - Adicionada lógica visual condicional com DataFrames híbridos em `app.py`. Para cada feedback contendo uma divergência (`DISLIKE`), as tabelas expandem debaixo dos panos o painel lado a lado "⚠️ Divergência Clínica Detectada (IA vs Médico)".
  - A arquitetura projeta em Vermelho a lógica do erro previsional da Gemma 4, e em Verde a intervenção que o médico submeteu ensinando a engine.
  - Implementado TDD `test_historico_traz_feedback` chancelando integridade de dados ao trafegar colunas de RLHF até as camadas de Front-End no SQLite.

## [0.11.0] - 2026-04-03
### Added
- **LLM Correction-Aware Prompting (Negative Few-Shot)**:
  - Base de dados equipada com `get_ultimas_correcoes(limit=2)`, lendo com assertividade os metadados do form de '*DISLIKE*'.
  - Instruções sistêmicas agora protegem contra falsos positivos: Injetam obrigatoriamente um log "APRENDIZADO POR CORREÇÃO MÉDICA" contendo a tríade de dados (Diagnóstico Inicial x Justificativa Falha x Correção Apontada).
  - TDD em dia validando isolamento entre tipos de feedbacks e mitigando strings nulas.

## [0.10.0] - 2026-04-03
### Added
- **LLM Prompting Otimizado (RLHF Fechando o Ciclo)**:
  - Integração total de **Dynamic Few-Shot Prompting**: A engine (`prompt_engine.py`) agora se reconecta no back-end com um smart filter iterativo suportando fallback (`get_melhores_exemplos(limit=3)`).
  - Antes de qualquer inferência, o app coleta retroativamente as justificativas que o Corpo Clínico ratificou (deu *"LIKE" / 👍 Útil*).
  - Modelos Injetados: Até 3 exemplos são concatenados no rodapé das instruções Sistêmicas (System Prompt), condicionando a IA a seguir exatamante o padrão que agradou a chefia sem necessidade de Fine-Tuning de rede complexo.

## [0.9.3] - 2026-04-03
### Refactor
- **Refatoração Streamlit**:
  - Eliminação de logs e *Deprecation Warnings*. Substituída a nomenclatura descontinuada `use_container_width` iterativamente em loops de setores, tabelas e RLHF pelas variáveis equivalentes da padronização 2026 (`width="stretch"`).

## [0.9.2] - 2026-04-03
### Changed
- **UX do Histórico**:
  - Limite de paginação do banco de dados alterado de `2` para `10` linhas por página em `app.py`, aumentando a densidade visual e analítica de retornos. Testes no pipeline parametrizados adequadamente.

## [0.9.1] - 2026-04-03
### Fixed
- **Bugs Visuais no RLHF**:
  - Corrigido problema gravíssimo de UX onde clicar nos botões de feedback provocava a limpeza de toda a inferência recém processada via Ollama. Resolvido acoplando uma persistência agressiva do `full_response` + `verdict_time` dentro do `st.session_state` nativo com identificador restrito por leito do paciente.

## [0.9.0] - 2026-04-03
### Added
- **Componente de Feedback RLHF**:
  - Incorporada arquitetura de aprovação clínica (RLHF) em tempo real após as inferências do LLM utilizando as restrições e painéis interativos de UI (`st.columns` e `st.form`).
  - Banco remodelado on-the-fly (`ALTER TABLE`) via SQLite injetando suporte robusto as métricas: `feedback_tipo`, `feedback_motivo` e `feedback_data`.
  - API Interna de mitigação em transações: rejeita com segurança tentativas repetitivas do mesmo client/plantonista para a mesma chave de inferência (previsibilidade via `test_mvp.py`).

## [0.8.0] - 2026-04-03
### Changed
- **UX do Histórico & Paginação (SQLite)**:
  - Removido o routing isolado do painel genérico. O histórico agora compõe nativamente o final da tela de **Análise Clínica** garantindo tracking de evolução isolado por leito.
  - Implementado sistema de query nativa paginada em `database.py` suportando `LIMIT`/`OFFSET` via parâmetros Streamlit `st.session_state`.
  - Controle interativo fluído e limpo contendo botões 'Anterior' e 'Próxima' sob o *dataframe* atrelado à validação (100%) em `test_mvp.py`.

## [0.7.0] - 2026-04-03
### Added
- **Painel de Histórico**:
  - Nova interface dedicada para listagem tabular das inferências (`st.dataframe` com Pandas bridge nativo do Streamlit).
  - TDD Completo: `test_mvp.py` verificando a capacidade do ORM manual em iterar decrescentemente sobre os retornos do `sqlite3.Row` na tabela `historico_analises` em memória.

## [0.6.0] - 2026-04-03
### Added
- **Documentação Master**: 
  - `README.md`: Estruturado panorama de Stack (Ollama Local, Gemma 4, Streamlit, SQLite, Pytest), workflow de instalação segura com Virtual Env e descritivos das Features Arquiteturais do projeto.
  - `CONTRIBUTING.md`: Manifesto estrito p/ Open Source impondo uso do Conventional Commits e passagem em suítes em TDD (100% Passed) atráves de PRs.

## [0.5.0] - 2026-04-03
### Added
- **Persistência de Dados (SQLite)**:
  - `database.py`: Módulo implementado usando `sqlite3` nativo que gerencia a tabela `historico_analises` no arquivo `monitor.db` (acoplado com auditoria via log).
  - Integrado diretamente no fluxo do `app.py`: após calcular o Benchmark do Ollama, todos os dados clínicos de inferência gerados (Paciente, Tendência, Time e Justificativa, sob perfil mockado 'Dr. Pietro') são agora gravados com rigor no banco com formato timestamp `yyyy/mm/dd HH:MM:SS`. Todas as operações sobem para o `log.txt` global. Coberto 100% via memória (`:memory:`) por `pytest`.

## [0.4.0] - 2026-04-03
### Added
- **Global Logging & Benchmarking**:
  - `custom_logger.py`: Módulo nativo Python para instanciar logger customizado. Integração de `StreamHandler` e `FileHandler` criando um log unificado na raiz do projeto (`log.txt`).
  - **Identidade de Log**: Mensagens obrigatoriamente tipificadas e contendo timestamp (`yyyy/mm/dd HH:MM:SS - [NÍVEL] - Mensagem`).
  - **Inference Benchmark**: O app coleta ativamente o frame inicial e frame final via `time.time()` ao invocar o Gemma_4 no Ollama Localmente, adicionando uma etiqueta com a métrica descritiva do tempo consumido pela transação (`⏱️ Tempo de inferência: X segundos`) renderizado ativamente na UI via Streamlit para auditorias de CTI e melhoria UX.

## [0.3.2] - 2026-04-03
### Fixed
- **Motor IA & Teste Real**: 
  - `llm_client.py`: Corrigido erro `404` alterando o nome do modelo apontado de `gemma4:4b` para o target local correto `gemma4:e4b`.
  - `test_integration.py`: Adicionado teste TDD validando o circuito fechado real de requests streaming no modelo Ollama rodando localmente (resposta efetiva capturada para 'PIORA' paciente 3).

## [0.3.1] - 2026-04-03
### Fixed
- **Infraestrutura**: Adicionado `requirements.txt` para gestão padronizada de dependências locais (streamlit, requests, pytest). Verificado isolamento de pastas de ambiente virtual (`.venv`, `env`) e `__pycache__` no `.gitignore`.

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
