from services.geradorDeDados import GeradorDeDados
from models.lojaModel import Loja
from repositories.lojaRepository import LojaRepository

lojaRepository = LojaRepository()

class LojaController:
    # Inicializa o controlador de lojas
    def __init__(self):
        self.geradorDeDados = GeradorDeDados()  # Instância do gerador de dados fakes
    
    # Cria uma nova loja (pode receber dados ou gerar automaticamente)
    def criarLoja(self, loja: Loja = None):
        # Se nenhuma loja for fornecida, gera dados fake
        if loja is None:
            loja = self.geradorDeDados.geradorDeLoja()
        
        # Cria instância de Loja com os dados (desempacotando o dicionário)
        novaLoja = Loja(**loja)
        
        return novaLoja  # Retorna a loja criada

    # Cria múltiplas lojas de uma vez
    def criarVariasLojas(self, quantidade):
        # Gera uma lista de dicionários com dados fake
        lojas = self.geradorDeDados.gerarLojas(quantidade)
        
        # Para cada loja gerada, chama o método criarLoja
        return [self.criarLoja(loja) for loja in lojas]

    def mostrarLojas(self):
        return lojaRepository.buscar_todas()
    