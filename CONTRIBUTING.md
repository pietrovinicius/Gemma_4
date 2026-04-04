# Guia de Contribuição 🤝

Nós abraçamos a comunidade Open Source de tecnologia atrelada a saúde! Siga as diretrizes rígidas abaixo para evoluirmos juntos o **Monitor de Tendência CTI**:

## ⚙️ Rodando Localmente
1. Faça o **Fork** do repositório via Github.
2. Clone seu fork para a máquina: `git clone https://github.com/SEU-USER/Gemma_4.git`
3. Crie e ative seu venv (`python3 -m venv .venv && source .venv/bin/activate`).
4. Instale o core de dependências: `pip install -r requirements.txt`
5. Certifique-se de subir o node local da IA (`ollama serve` & pull do modelo isolado `gemma4:e4b`).

## 🧪 Regra Estrita: Test-Driven Development (TDD)
Aqui construímos código crítico hospitalar guiado proeminentemente por baterias de testes e mocks limpos (`test_mvp.py`). 
A cultura de TDD e Clean Code não é negociável:
- **Todo Pull Request DEVE contam obrigatoriamente com a validação automatizada prévia.**
- Nenhuma linha de produção (UI, LLM, Queries) é unificada na Main se não houver um teste equivalente (Pytest) validando sua eficácia sistêmica.
- Veja os testes falharem intencionalmente (Fase RED) antes de cobrir o refactoring (Fase GREEN).
- O PR só é mergeado se sua verificação relatar 100% de sucesso rodando `python -m pytest`.

## 🏷️ Padrão de Commits
Utilize sempre o enquadramento de **Conventional Commits** clássico para submeter suas pull requests, nos assegurando um versionamento legível e passível de CI/CD:
Exemplos da nossa base: 
- `feat: adiciona componente de pressao arterial via st.metrics`
- `fix: formata schema dos dados D-1 perdidos`
- `docs: adiciona guia de troubleshooting`
- `test: isola o banco sqlite em memória com fixtures`

Bem-vindo(a) e boas contribuições seguras para os leitos!
