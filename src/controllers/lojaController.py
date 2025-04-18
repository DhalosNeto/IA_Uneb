from services.geradorDeDados import GeradorDeDados
from services.busca import Busca
from models.lojaModel import Loja


class LojaController:
    # Inicializa o controlador de lojas
    def __init__(self):
        self.geradorDeDados = GeradorDeDados()  # Instância do gerador de dados fakes
        self.busca = Busca()  # Instância do serviço de busca
    # Cria uma nova loja (pode receber dados ou gerar automaticamente)
    def criarLoja(self, loja: Loja = None):
        # Se nenhuma loja for fornecida, gera dados fake
        if loja is None:
            loja = self.geradorDeDados.geradorDeLoja()
        
        # Cria instância de Loja com os dados (desempacotando o dicionário)
        novaLoja = Loja(**loja)
        
        return self.busca.salvarLoja(novaLoja)  # Retorna a loja criada

    # Cria múltiplas lojas de uma vez
    def criarVariasLojas(self, quantidade):
        # Gera uma lista de dicionários com dados fake
        lojas = self.geradorDeDados.gerarLojas(quantidade)
        
        # Para cada loja gerada, chama o método criarLoja
        return [self.busca.salvarLoja(self.criarLoja(loja)) for loja in lojas]

    def mostrarLojas(self):
        return self.busca.buscarTodasLojas()
    
    def buscarLojaPorNome(self, nome):
        return self.busca.buscarLojaPorNome(nome)
    