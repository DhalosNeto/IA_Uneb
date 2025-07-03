# 🤖 IA UNEB - Perguntas e Respostas com Interface PyQt6

Este é um projeto interativo de interface gráfica desenvolvido em **Python com PyQt6**, que permite ao usuário fazer **perguntas para uma IA** baseada em LLM local (via Ollama) com contexto vindo de um **banco de dados de lojas**. O sistema otimiza o tempo de resposta utilizando cache em um banco PostgreSQL.

---

## 🧠 Funcionalidades

- ✅ Interface moderna em PyQt6
- 🧾 Consulta a IA com contexto das lojas cadastradas
- 💾 Banco de dados PostgreSQL com persistência de:
  - Perguntas e respostas
  - Avaliação do usuário sobre a resposta (correta/incorreta)
- ⚡ Cache inteligente:
  - Respostas já fornecidas pela IA são reaproveitadas automaticamente
- 🧑‍🏫 Correção manual:
  - Se a IA errar, o usuário pode digitar a resposta certa e salvá-la

---

## 🖥️ Telas do sistema

| Tela de pergunta | Tela de resposta | Correção manual |
|------------------|------------------|------------------|
| Usuário digita sua pergunta e envia para IA | A IA responde; usuário avalia se está correta | Se clicar "Errado", pode digitar a resposta correta |

---

## 🧪 Como executar

1. **Clone o projeto:**

```bash
git clone https://github.com/seu-usuario/ia-uneb.git
cd ia-uneb
```

2. **Configure o ambiente:**
Crie um arquivo .env com suas credenciais PostgreSQL:
```bash
DB_HOST=seu_host
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_PORT=5432
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Inicie o servidor da IA (Ollama):**
```bash
ollama run mistral
```

5. **Execute a aplicação:**
```bash
python src/main.py
```
## 🧠 Modelos de IA usados
Atualmente, o sistema usa:

- [Mistral (via Ollama)](https://ollama.com/library/mistral)

Você pode modificar facilmente o modelo no perguntaResposta.py.