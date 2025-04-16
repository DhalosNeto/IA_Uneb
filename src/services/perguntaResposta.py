from transformers import pipeline

class IAResposta:
    def __init__(self):
        
        self.qa_pipeline = pipeline(
            "question-answering",
            model="pierreguillou/bert-base-cased-squad-v1.1-portuguese",
            tokenizer="pierreguillou/bert-base-cased-squad-v1.1-portuguese"
        )

    def responder(self, pergunta: str, contexto: str) -> str:
        resposta = self.qa_pipeline({
            'question': pergunta,
            'context': contexto
        })
        return resposta['answer']