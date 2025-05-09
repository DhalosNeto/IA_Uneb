
class Loja:
    # Método construtor da classe Loja
    def __init__(self, id=None, nome='', endereco=''):
        self.id = id
        # Atribui o nome da loja
        self.nome = nome  
        # Atribui o endereço da loja
        self.endereco = endereco  

    # Método que retorna as informações da loja em formato de dicionário
    def infos_dic(self):
        return {
            'id': self.id,
            'nome': self.nome,       # Chave 'nome' com valor do atributo nome
            'endereco': self.endereco,  # Chave 'endereco' com valor do atributo endereco
        }