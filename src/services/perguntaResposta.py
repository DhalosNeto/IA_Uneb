import logging
from ollama import chat
from repositories.perguntasRepository import RepositorioPerguntaResposta

class IAResposta:
    def __init__(self, modelo: str = "mistral"):
        self.modelo = modelo
        self.limite_contexto = 1000  # Limite de caracteres para o contexto
        self.repositorio = RepositorioPerguntaResposta()
        logging.basicConfig(level=logging.INFO)

    def responder(self, pergunta: str, contexto: str) -> str:
        # 1. Verifica se a pergunta já tem resposta salva no banco
        resposta_existente = self.repositorio.buscar_resposta(pergunta)
        if resposta_existente:
            logging.info("Resposta recuperada do banco de dados (sem usar IA)")
            return resposta_existente

        # 2. Gera a resposta com IA
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
            )['message']['content'].strip()

            # 3. Salva a resposta no banco
            self.repositorio.salvar_resposta(pergunta, resposta)
            logging.info("Resposta gerada pela IA")
            return resposta

        except Exception as e:
            logging.error(f"Erro ao responder pergunta: {e}")
            return "Ocorreu um erro ao tentar responder sua pergunta."
