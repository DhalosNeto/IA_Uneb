class LojaView:
    @staticmethod
    def mostrarLoja(loja):
        print("--- Dados da Loja ---")
        print(f'Nome:     {loja.nome}')
        print(f'Endereco: {loja.endereco}')
        print(f'Email:    {loja.email}')
    
    @staticmethod
    def mostrarVariasLojas(lojas):
        print(f'== Lista de Lojas ===')
        for i, loja in enumerate(lojas, 1):
            print(f'Loja #{i}')
            LojaView.mostrarLoja(loja)
    
    @staticmethod
    def get_loja_quanti():
        try:
            return int(input("Quantas você deseja gerar? "))
        except ValueError:
            print("Por favor, digite um número válido")
            return 0
        
    @staticmethod    
    def get_nome_loja(self):
        return input("Digite o nome da loja para buscar: ")