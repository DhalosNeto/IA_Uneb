from transformers import pipeline
import logging

class IAResposta:
    def __init__(self):
        # Carrega o modelo apenas uma vez
        self.qa_pipeline = pipeline(
            "question-answering",
            model="pierreguillou/bert-base-cased-squad-v1.1-portuguese",
            tokenizer="pierreguillou/bert-base-cased-squad-v1.1-portuguese"
        )
        self.limite_contexto = 2000  # Limite seguro de caracteres (~512 tokens)
        logging.basicConfig(level=logging.INFO)
    
    def responder(self, pergunta: str, contexto: str) -> str:
        # Reduz o contexto se estiver muito grande
        contexto = contexto[:self.limite_contexto]

        try:
            resultado = self.qa_pipeline({
                'question': pergunta,
                'context': contexto
            })

            # Se a confiança for baixa, não responder
            if resultado['score'] < 0.3:
                logging.warning(f"Resposta de baixa confiança: {resultado}")
                return "Desculpe, não encontrei uma resposta clara para isso."

            return resultado['answer']
        except Exception as e:
            logging.error(f"Erro ao responder pergunta: {e}")
            return "Ocorreu um erro ao tentar responder sua pergunta."
