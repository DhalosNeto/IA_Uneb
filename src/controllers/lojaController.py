from services.geradorDeDados import GeradorDeDados
from services.lojaService import LojaService
from models.lojaModel import Loja



class LojaController:
    # Inicializa o controlador de lojas
    def __init__(self):
        self.geradorDeDados = GeradorDeDados()  # Instância do gerador de dados fakes
        self.busca = LojaService()  # Instância do serviço de busca
    # Cria uma nova loja (pode receber dados ou gerar automaticamente)
    
    def criarLoja(self, loja: Loja = None):
        # Se nenhuma loja for fornecida, gera dados fake
        if loja is None:
            loja = self.geradorDeDados.geradorDeLoja()
        
        # Cria instância de Loja com os dados (desempacotando o dicionário)
        
        
        return Loja(**loja)  # Retorna a loja criada

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
    
    def salvar(self, loja):
        return self.busca.salvarLoja(loja)
    