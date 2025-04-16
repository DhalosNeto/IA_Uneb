from repositories.lojaRepository import LojaRepository
from controllers.lojaController import LojaController
from views.lojaView import LojaView

lojaRepository = LojaRepository()
lojaController = LojaController()
lojaView = LojaView()



while True:
    print("\nMenu:")
    print("1. Gerar lojas aleatórias")
    print("2. Gerar múltiplas lojas aleatórias")
    print("3. listar todas as lojas")
    print("4. Buscar loja por nome")
    print("5. Fazer pergunta")
    print("6. Sair")

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
        nome = input("Digite o nome da loja para buscar: ")
        lojas = lojaController.buscarLojaPorNome(nome)
        lojaView.mostrarVariasLojas(lojas)

    elif escolha == "5":
        pergunta = input("Digite sua pergunta: ")
        resposta = lojaController.responder_pergunta(pergunta)
        print("Resposta:", resposta)

    elif escolha == "6":
        print("Saindo...")
        break

    else:
        print("Opção inválida. Tente novamente.")

