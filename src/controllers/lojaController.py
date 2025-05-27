from services.seleniumBusca import buscar_lojas_google_maps
from models.lojaModel import Loja
from services.lojaService import LojaService
from services.perguntaResposta import IAResposta

class LojaController:
    def __init__(self):
        self.lojaService = LojaService()
        self.ia = IAResposta()

    def responder_pergunta(self, pergunta: str) -> str:
        contexto = self.gerar_contexto_lojas()
        return self.ia.responder(pergunta, contexto)

    def criarLoja(self, loja: Loja):
        return self.lojaService.salvarLoja(loja)

    def criarVariasLojas(self, lojas_data):
        # lojas_data deve ser uma lista de dicionários ou objetos Loja
        return [self.criarLoja(Loja(**dados)) for dados in lojas_data]

    def mostrarLojas(self):
        return self.lojaService.buscarTodasLojas()

    def gerar_contexto_lojas(self) -> str:
        lojas = self.lojaService.buscarTodasLojas()
        texto = "Na cidade de Alagoinhas, existem as seguintes lojas: "
        texto += f", ".join([f"{loja.nome} (localizada em {loja.endereco})" for loja in lojas])
        return texto

    def buscarLojaPorNome(self, nome):
        return self.lojaService.buscarLojaPorNome(nome)

    def salvar(self, loja):
        return self.lojaService.salvarLoja(loja)

    def buscar_e_salvar_lojas_google(self):
        buscar_lojas_google_maps()  # usa a função real com Selenium
