from controllers.lojaController import LojaController
from views.lojaView import LojaView
from services.seleniumBusca import buscar_lojas_google_maps  # NOVO IMPORT

lojaController = LojaController()
lojaView = LojaView()

while True:
    print("\nMenu:")
    print("1. Listar todas as lojas")
    print("2. Buscar loja por nome")
    print("3. Fazer pergunta")
    print("4. Buscar lojas do Google Maps (Alagoinhas)")  
    print("5. Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        lojas = lojaController.mostrarLojas()
        lojaView.mostrarVariasLojas(lojas)

    elif escolha == "2":
        nome = input("Digite o nome da loja para buscar: ")
        lojas = lojaController.buscarLojaPorNome(nome)
        lojaView.mostrarVariasLojas(lojas)

    elif escolha == "3":
        pergunta = input("Digite sua pergunta: ")
        resposta = lojaController.responder_pergunta(pergunta)
        print("Resposta:", resposta)


    elif escolha == "4":
        print("Buscando lojas no Google Maps...")
        buscar_lojas_google_maps()
        print("Busca finalizada!")

    elif escolha == "5":
        print("Saindo...")
        break

    else:
        print("Opção inválida. Tente novamente.")
