import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class DatabaseConfig:
    """Classe para configuração e gerenciamento de conexão com o banco de dados"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.db_url = os.getenv("POSTGRES_URL")
        # Configurações do banco (lidas do .env)
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT', 5432)
        }

    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            print("Conexão com o banco de dados estabelecida com sucesso!")
            return True
        except OperationalError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False

    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Conexão com o banco de dados encerrada.")

    def execute_query(self, query, params=None):
        """Executa uma query SQL"""
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Erro ao executar query: {e}")
            return False

    def criacaoTabelaLoja(self):
        """Cria a tabela Loja no banco de dados"""
        try:
            query = """
            CREATE TABLE IF NOT EXISTS lojas (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                endereco VARCHAR(255) NOT NULL
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("Tabela Loja criada com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")
            self.connection.rollback()

    def criar_tabela_perguntas_respostas(self):
        """Cria a tabela perguntas_respostas se não existir"""
        if self.existe_tabela_perguntas_respostas():
            return  # Já existe, não faz nada
        try:
            query = """
            CREATE TABLE perguntas_respostas (
                id SERIAL PRIMARY KEY,
                pergunta TEXT UNIQUE NOT NULL,
                resposta TEXT NOT NULL,
                correta BOOLEAN
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("Tabela perguntas_respostas criada com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabela perguntas_respostas: {e}")
            self.connection.rollback()


    def existe_tabela_perguntas_respostas(self):
        """Verifica se a tabela perguntas_respostas existe"""
        try:
            self.cursor.execute("SELECT to_regclass('public.perguntas_respostas');")
            result = self.cursor.fetchone()
            return result[0] is not None
        except Exception as e:
            print(f"Erro ao verificar tabela perguntas_respostas: {e}")
            return False


    def existeTabelaLoja(self):
        """Verifica se a tabela Loja existe"""
        try:
            self.cursor.execute("SELECT to_regclass('public.lojas');")
            result = self.cursor.fetchone()
            return result[0] is not None
        except Exception as e:
            print(f"Erro ao verificar tabela: {e}")
            return False

    def fetch_data(self, query, params=None):
        """Busca dados do banco"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            return None