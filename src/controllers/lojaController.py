from services.geradorDeDados import GeradorDados
from models.lojaModel import Loja

class LojaController:
    def __init__(self):
        self.geradorDeDados = GeradorDados()
        self.lojas = []
    
    def criarLoja(self, loja: Loja):
        if loja is None:
            loja = self.geradorDeDados.geradorDeLoja()
        novaLoja = Loja(**loja)
        self.lojas.append(novaLoja)
        return novaLoja

    def criarVariasLojas(self, quantidade):
        lojas = self.geradorDeDados.gerarLojas(quantidade)
        return [self.criarLoja(loja) for loja in lojas]