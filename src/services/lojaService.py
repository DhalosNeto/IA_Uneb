from repositories.lojaRepository import LojaRepository

class LojaService:
    def __init__(self):
        self.lojaRepository = LojaRepository()
    
    def salvarLoja(self, loja):
        """Salva uma loja no repositório"""
        return self.lojaRepository.salvar(loja)

    def buscarLojaPorNome(self, nome):
        """Busca uma loja pelo nome"""
        lojas = self.lojaRepository.buscar_por_nome(nome)
        if lojas:
            return lojas
        else:
            print(f"Nenhuma loja encontrada com o nome: {nome}")
            return None
    
    def buscarLojaPorId(self, id):
        """Busca uma loja pelo ID"""
        loja = self.lojaRepository.buscar_por_id(id)
        if loja:
            return loja
        else:
            print(f"Nenhuma loja encontrada com o ID: {id}")
            return None
    def buscarTodasLojas(self):
        """Busca todas as lojas"""
        lojas = self.lojaRepository.buscar_todas()
        if lojas:
            return lojas
        else:
            print("Nenhuma loja encontrada")
            return []
        
    def loja_existe(self, endereco):
        """Verifica se uma loja com endereço já existe"""
        lojas = self.buscarTodasLojas()
        for loja in lojas:
                if loja.endereco.strip().lower() == endereco.strip().lower():
                    return True
        return False