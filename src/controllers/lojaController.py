from services.geradorDeDados import GeradorDeDados
from models.lojaModel import Loja
from repositories.lojaRepository import LojaRepository
from services.perguntaResposta import IAResposta

lojaRepository = LojaRepository()

class LojaController:
    # Inicializa o controlador de lojas
    def __init__(self):
        self.geradorDeDados = GeradorDeDados()  # Instância do gerador de dados fakes
        self.ia = IAResposta()

    def responder_pergunta(self, pergunta: str) -> str:
        contexto = self.gerar_contexto_lojas()
        return self.ia.responder(pergunta, contexto)
    
    # Cria uma nova loja (pode receber dados ou gerar automaticamente)
    def criarLoja(self, loja: Loja = None):
        # Se nenhuma loja for fornecida, gera dados fake
        if loja is None:
            loja = self.geradorDeDados.geradorDeLoja()
        
        # Cria instância de Loja com os dados (desempacotando o dicionário)
        novaLoja = Loja(**loja)
        
        return lojaRepository.salvar(novaLoja)  # Retorna a loja criada

    # Cria múltiplas lojas de uma vez
    def criarVariasLojas(self, quantidade):
        # Gera uma lista de dicionários com dados fake
        lojas = self.geradorDeDados.gerarLojas(quantidade)
        
        # Para cada loja gerada, chama o método criarLoja
        return [lojaRepository.salvar(self.criarLoja(loja)) for loja in lojas]

    def mostrarLojas(self):
        return lojaRepository.buscar_todas()
    
    def buscarLojaPorNome(self, nome: str):
        return lojaRepository.buscar_por_nome(nome)
    
    def gerar_contexto_lojas(self) -> str:
        lojas = lojaRepository.buscar_todas()
        texto = ""
        for loja in lojas:
            texto += f"Nome: {loja.nome}. Endereço: {loja.endereco}. Email: {loja.email}.\n"
        return texto
    