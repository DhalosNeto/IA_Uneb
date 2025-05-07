from models.lojaModel import Loja
class LojaView:
    @staticmethod
    def mostrarLoja(loja: Loja):
        print()
        print(f"--- Dados da Loja #{loja.id} ---")
        print(f'Nome:     {loja.nome}')
        print(f'Endereco: {loja.endereco}')
    
    @staticmethod
    def mostrarVariasLojas(lojas):
        print(f'== Lista de Lojas ===')
        for i, loja in enumerate(lojas, 1):
            LojaView.mostrarLoja(loja)
