from faker import Faker

class GeradorDeDados:
    def __init__(self):
        self.fake = Faker('pt_BR')
    
    def geradorDeLoja(self):
        return {
            'nome': self.fake.name, # Percebi agora que esse nome é de pessoa
            'endereco': self.fake.address,
            'emial' : self.fake.email
        }
    def gerarLojas(self, quantidade=1):
        return [self.geradorDeLoja() for _ in range(quantidade)]