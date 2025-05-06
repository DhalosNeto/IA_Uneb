from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from models.lojaModel import Loja
from repositories.lojaRepository import LojaRepository
from services.lojaService import LojaService
import logging

logging.basicConfig(level=logging.INFO)

repo = LojaRepository()
servico_loja = LojaService()

def iniciar_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

def buscar_lojas_google_maps(cidade="alagoinhas ba"):
    driver = iniciar_driver()
    driver.get(f"https://www.google.com/maps/search/lojas+em+{cidade.replace(' ', '+')}")
    sleep(5)

    print('Carregando mais resultados...')
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 1200);")
        sleep(2)

    resultados = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")

    total_inseridas = 0
    for elemento in resultados:
        try:
            nome = elemento.find_element(By.CSS_SELECTOR, "a.hfpxzc").text.strip()
            if not nome:
                continue

            endereco = None
            try:
                endereco = elemento.find_element(By.CSS_SELECTOR, 'button[data-item-id="address"]').text.strip()
            except:
                spans = elemento.find_elements(By.CSS_SELECTOR, "span")
                for span in spans:
                    texto = span.text.strip()
                    if any(p in texto.lower() for p in ["rua", "av", "alagoinhas", "bairro", "travessa", "praça"]):
                        endereco = texto
                        break

            if not endereco:
                logging.warning(f"Endereço não encontrado para: {nome}")
                continue

            if servico_loja.loja_existe(nome, endereco):
                logging.info(f"Loja já existe: {nome} - {endereco}")
                continue

            loja = Loja(nome=nome, endereco=endereco, email=None)
            repo.salvar(loja)
            total_inseridas += 1
            logging.info(f"Inserida: {loja.nome} - {loja.endereco}")

        except Exception as e:
            logging.error(f"Erro ao processar resultado: {e}")

    driver.quit()
    logging.info(f"Busca concluída. {total_inseridas} novas lojas inseridas.")

if __name__ == "__main__":
    buscar_lojas_google_maps()
