import psycopg2
from typing import List, Optional
from models.lojaModel import Loja
from db.config import DatabaseConfig
from dotenv import load_dotenv
from psycopg2 import OperationalError

db_config = DatabaseConfig()
class LojaRepository:
    def __init__(self):
        self.db_config = db_config
        self.conn = None
        self._conectar()
        if db_config.existeTabelaLoja() == False:
            db_config.criacaoTabelaLoja()
    
    def _conectar(self):
        """Estabelece a conexão com o banco"""
        try:
            self.db_config.connect()
            self.conn = self.db_config.connection
            if not self.conn or self.conn.closed:
                raise ConnectionError("Falha ao estabelecer conexão com o banco de dados")
        except Exception as e:
            print(f"Erro de conexão: {e}")
            self.conn = None
    
    def _verificar_conexao(self):
        """Verifica e reconecta se necessário"""
        if not self.conn or self.conn.closed:
            self._conectar()
    
    def salvar(self, loja: Loja) -> Optional[Loja]:
        self._verificar_conexao()
        if not self.conn:
            print("Não há conexão com o banco de dados")
            return None
        
        query = """
        INSERT INTO lojas (nome, endereco)
        VALUES (%s, %s)
        RETURNING id
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (loja.nome, loja.endereco))
                loja.id = cursor.fetchone()[0]
                self.conn.commit()
                return loja
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao salvar loja: {e}")
            return None
    
    def buscar_por_id(self, id: int) -> Optional[Loja]:
        """Busca uma loja pelo ID"""
        query = "SELECT id, nome, endereco FROM lojas WHERE id = %s"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (id,))
                resultado = cursor.fetchone()
                if resultado:
                    return Loja(*resultado)
                return None
        except Exception as e:
            print(f"Erro ao buscar loja: {e}")
            return None
    
    def buscar_todas(self) -> List[Loja]:
        """Retorna todas as lojas cadastradas"""
        query = "SELECT * FROM lojas"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                return [Loja(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao buscar lojas: {e}")
            return []
    
    def deletar(self, id: int) -> bool:
        """Remove uma loja pelo ID"""
        query = "DELETE FROM lojas WHERE id = %s"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (id,))
                self.conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao deletar loja: {e}")
            return False
    
    def atualizar(self, loja: Loja) -> bool:
        """Atualiza os dados de uma loja"""
        query = """
        UPDATE lojas
        SET nome = %s, endereco = %s
        WHERE id = %s
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (loja.nome, loja.endereco, loja.id))
                self.conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao atualizar loja: {e}")
            return False
        
    def buscar_por_nome(self, nome) -> List[Loja]:
        query = "SELECT id, nome, endereco FROM lojas WHERE nome ILIKE %s"
        try:
            resultados = []
            with self.conn.cursor() as cursor:
                cursor.execute(query, (f'%{nome}%',))
                resultados = cursor.fetchall()
            return [Loja(*row) for row in resultados]
        except Exception as e:
            print(f"Erro ao buscar loja por nome: {e}")
        return []