from faker import Faker
from faker.providers import BaseProvider

class AlagoinhasProvider(BaseProvider):
    def alagoinhas_endereco(self):
        # Lista de ruas e bairros fictícios de Alagoinhas
        rua = [
            "Rua São Paulo",
            "Avenida Getúlio Vargas",
            "Rua da Matriz",
            "Travessa dos Ferroviários",
            "Praça Ruy Barbosa",
            "Avenida João Durval",
            "Rua Coronel Filomeno",
            "Beco da Cultura"
        ]
        bairro = [
            "Centro",
            "Santa Terezinha",
            "Brasília",
            "Catu",
            "São José",
            "Fonte Nova"
        ]
        street = self.random_element(rua)
        bairro_name = self.random_element(bairro)
        number = self.random_int(min=1, max=1000)
        return f"{street}, {number}, {bairro_name}, Alagoinhas - BA"


class GeradorDeDados:
    # Inicializa o gerador de dados com localização em português do Brasil
    def __init__(self):
        self.fake = Faker('pt_BR')
        self.fake.add_provider(AlagoinhasProvider)  # Cria uma instância do Faker para dados brasileiros
    
    # Método para gerar dados de uma loja fictícia
    def geradorDeLoja(self):
        return {
            'id': self.fake.cnpj(),
            'nome': self.fake.company(),  # Gera o nome da loja
            'endereco': self.fake.alagoinhas_endereco(),  # Gera um endereço completo
            'email': self.fake.company_email()  # Corrigido o typo 'emial' e usa email corporativo
        }
    
    # Método para gerar múltiplas lojas
    def gerarLojas(self, quantidade=1):
        # Usa list comprehension para gerar a quantidade especificada de lojas
        return [self.geradorDeLoja() for _ in range(quantidade)]