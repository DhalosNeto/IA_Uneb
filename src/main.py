from repositories.lojaRepository import LojaRepository
from controllers.lojaController import LojaController
from db.config import DatabaseConfig
from views.lojaView import LojaView

db_config = DatabaseConfig()
db_config.connect()

lojaRepository = LojaRepository(db_config.connection)
lojaController = LojaController()
lojaView = LojaView()



while True:
    print("\nMenu:")
    print("1. Gerar lojas aleatórias")
    print("2. Gerar múltiplas lojas aleatórias")
    print("3. listar todas as lojas")
    print("4. Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        loja = lojaController.criarLoja()
        lojaRepository.salvar(loja)
        print("Loja criada com sucesso")

    elif escolha == "2":
        quantidade = lojaView.get_loja_quanti()
        if quantidade > 0:
            lojaController.criarVariasLojas(quantidade)
            print(f'{quantidade} lojas geradas com sucesso!')

    elif escolha == "3":
        lojas = lojaController.mostrarLojas()
        lojaView.mostrarVariasLojas(lojas)

    elif escolha == "4":
        db_config.disconnect()
        print("Saindo...")
        break

    else:
        print("Opção inválida. Tente novamente.")

