# Monitor de Tendência CTI com IA Local 🏥🤖

O **Monitor de Tendência CTI** é um MVP focado em saúde digital que atua como um sistema de suporte à decisão clínica assistido por Inteligência Artificial (LLM). O projeto propõe analisar prontuários e a evolução das últimas 24h a 48h de pacientes internados em terapia intensiva para determinar tendências clínicas críticas (🟢 Melhora, 🟡 Estagnado, 🔴 Piora), tudo processado de forma 100% segura, com IA local para proteger dados de saúde.

## 🛠️ Tech Stack
- **Linguagem**: Python 3.9+
- **Frontend / UX**: Streamlit
- **Motor de IA**: Modelo `Gemma 4` (`gemma4:e4b`) servido dinamicamente via Ollama
- **Database**: SQLite3 nativo
- **Testes & Qualidade**: Pytest (com rigoroso Test-Driven Development)

## 🚀 Como instalar e rodar

1. **Clone do repositório**
   ```bash
   git clone https://github.com/pietrovinicius/Gemma_4.git
   cd Gemma_4
   ```

2. **Suba o Ollama (servidor de IA local)**
   Certifique-se de que possui o Ollama instalado. Inicie o modelo de predição:
   ```bash
   ollama run gemma4:e4b
   ```
   *(O servidor expõe localmente a API na porta `11434` padrão)*

3. **Configure o ambiente virtual**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Inicie o App Streamlit**
   ```bash
   streamlit run mvp_monitor/app.py
   ```
   *Entre como usuário `admin` e senha `1234` na tela de Mock Login!*

## 📁 Estrutura do Projeto (Core Features)
- **Persistência (SQLite)**: As análises (vereditos clínicos do LLM, usuário plantonista e latência da inferência) são processadas em Stream e imediatamente salvas e seladas no `monitor.db` contendo todo o histórico do CTI (`database.py`).
- **Global Logging & Benchmarking**: Toda operação sensível transita por nosso logger customizado e salva a trilha de forma contínua em formato ANSI date em `log.txt`. Adicionado framework de benchmark que devolve tempo de request assíncrono para a tela.
- **100% Test-Driven (TDD)**: Garantia de Clean Code forçado! O núcleo base, dos mocks falsos do WhatsApp aos saves InMemory (`:memory:`) do BD foram codados partindo de blocos falhos (Red -> Green). Rode via `pytest`.
