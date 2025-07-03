from db.config import DatabaseConfig

class RepositorioPerguntaResposta:
    def __init__(self):
        self.db = DatabaseConfig()
        self.db.connect()
        self.db.criar_tabela_perguntas_respostas()

    def salvar_resposta(self, pergunta, resposta, correta=None):
        query = """
        INSERT INTO perguntas_respostas (pergunta, resposta, correta)
        VALUES (%s, %s, %s)
        ON CONFLICT (pergunta) DO UPDATE SET resposta = EXCLUDED.resposta, correta = EXCLUDED.correta;
        """
        self.db.execute_query(query, (pergunta, resposta, correta))

    def buscar_resposta(self, pergunta):
        resultado = self.db.fetch_data(
            "SELECT resposta FROM perguntas_respostas WHERE pergunta = %s;",
            (pergunta,)
        )
        return resultado[0][0] if resultado else None

    def atualizar_correcao(self, pergunta, correta):
        if not self.buscar_resposta(pergunta):
            print("⚠️ Tentando corrigir uma pergunta que não está salva. Ignorando.")
            return
        query = """
        UPDATE perguntas_respostas
        SET correta = %s
        WHERE pergunta = %s;
        """
        self.db.execute_query(query, (correta, pergunta))

