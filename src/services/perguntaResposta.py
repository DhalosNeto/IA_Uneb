import logging
from ollama import chat

class IAResposta:
    def __init__(self, modelo: str = "mistral"):
        self.modelo = modelo
        self.limite_contexto = 1000  # Limite de caracteres para o contexto
        logging.basicConfig(level=logging.INFO)

    def responder(self, pergunta: str, contexto: str) -> str:
        # Limita o tamanho do contexto se necessário
        # contexto = contexto[:self.limite_contexto]

        prompt = f"""
Você é um assistente inteligente. Use o contexto abaixo para responder a pergunta do usuário com precisão.

Contexto:
{contexto}

Pergunta:
{pergunta}

Responda com base apenas nas informações do contexto.
"""

        try:
            resposta = chat(
                model=self.modelo,
                messages=[{"role": "user", "content": prompt}]
            )
            return resposta['message']['content'].strip()
        except Exception as e:
            logging.error(f"Erro ao responder pergunta: {e}")
            return "Ocorreu um erro ao tentar responder sua pergunta."
