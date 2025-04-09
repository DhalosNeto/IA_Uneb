from faker import Faker

class GeradorDeDados:
    # Inicializa o gerador de dados com localização em português do Brasil
    def __init__(self):
        self.fake = Faker('pt_BR')  # Cria uma instância do Faker para dados brasileiros
    
    # Método para gerar dados de uma loja fictícia
    def geradorDeLoja(self):
        return {
            'id': self.fake.cnpj(),
            'nome': self.fake.company(),  # Gera o nome da loja
            'endereco': self.fake.address().split(' / ')[1],  # Gera um endereço completo
            'email': self.fake.company_email()  # Corrigido o typo 'emial' e usa email corporativo
        }
    
    # Método para gerar múltiplas lojas
    def gerarLojas(self, quantidade=1):
        # Usa list comprehension para gerar a quantidade especificada de lojas
        return [self.geradorDeLoja() for _ in range(quantidade)]