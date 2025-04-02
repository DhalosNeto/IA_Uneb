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
        
        # Configurações do banco (lidas do ambiente)
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'meu_banco'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgres'),
            'port': os.getenv('DB_PORT', '5432')
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

    def fetch_data(self, query, params=None):
        """Busca dados do banco"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            return None