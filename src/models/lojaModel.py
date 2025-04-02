class Loja:
    def __init__(self, nome, endereco, email):
        self.nome = nome
        self.endereco = endereco
        self.email = email
    def infos_dic(self):
        return {
            'nome': self.nome,
            'endereco': self.endereco,
            'email': self.email
        }