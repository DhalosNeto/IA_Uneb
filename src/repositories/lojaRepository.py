import psycopg2
from typing import List, Optional
from models.lojaModel import Loja

class LojaRepository:
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def salvar(self, loja: Loja) -> Optional[Loja]:
        """Salva uma loja no banco de dados e retorna com ID"""
        query = """
        INSERT INTO lojas (nome, endereco, email)
        VALUES (%s, %s, %s)
        RETURNING id
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (loja.nome, loja.endereco, loja.email))
                loja.id = cursor.fetchone()[0]
                self.conn.commit()
                return loja
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao salvar loja: {e}")
            return None
    
    def buscar_por_id(self, id: int) -> Optional[Loja]:
        """Busca uma loja pelo ID"""
        query = "SELECT id, nome, endereco, email FROM lojas WHERE id = %s"
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
        query = "SELECT id, nome, endereco, email FROM lojas"
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
        SET nome = %s, endereco = %s, email = %s
        WHERE id = %s
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (loja.nome, loja.endereco, loja.email, loja.id))
                self.conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao atualizar loja: {e}")
            return False