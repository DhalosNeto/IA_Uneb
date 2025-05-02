from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from models.lojaModel import Loja
from repositories.lojaRepository import LojaRepository
from services.busca import Busca
import logging

logging.basicConfig(level=logging.INFO)

repo = LojaRepository()
busca = Busca()

def iniciar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def buscar_lojas_google_maps():
    driver = iniciar_driver()
    driver.get("https://www.google.com/maps/search/lojas+em+alagoinhas+ba")
    sleep(5)

    # Scroll para carregar mais resultados
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 1000);")
        sleep(2)

    resultados = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')  # cada cartão de loja

    for elemento in resultados:
        try:
            nome = elemento.find_element(By.CSS_SELECTOR, 'a.hfpxzc').text.strip()
            endereco = elemento.find_element(By.CSS_SELECTOR, 'div.W4Efsd').text.strip()

            if busca.loja_existe(nome, endereco):
                logging.info(f"Loja já existe: {nome}")
                continue

            loja = Loja(nome=nome, endereco=endereco, email=None)  # email é difícil de extrair
            logging.info(f"Inserindo loja: {loja.nome} - {loja.endereco}")
            repo.salvar(loja)
        except Exception as e:
            logging.error(f"Erro ao processar resultado: {e}")

    driver.quit()

if __name__ == "__main__":
    buscar_lojas_google_maps()
