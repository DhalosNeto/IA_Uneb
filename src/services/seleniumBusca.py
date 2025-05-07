from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from services.lojaService import LojaService
from selenium.webdriver.common.by import By
from models.lojaModel import Loja
from selenium import webdriver
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)

servico_loja  = LojaService()            

def iniciar_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

def buscar_lojas_google_maps(cidade="alagoinhas ba"):
    driver = iniciar_driver()

    driver.get(f"https://www.google.com/maps/search/lojas+em+{cidade.replace(' ', '+')}")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.Nv2PK.THOPZb.CpccDe ")))


    print('Carregando mais resultados...')
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)

        
    resultados = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK.THOPZb.CpccDe ")
    
    total_inseridas = 0
    for elemento in resultados:

        try:
            nome = elemento.find_element(By.CSS_SELECTOR, "a.hfpxzc").get_attribute("aria-label").strip()
            
            if not nome:
                continue

            endereco = None
            spans = elemento.find_elements(By.CSS_SELECTOR, "span")
            for span in spans:
                texto = span.text.strip()
                
                if any(p in texto.lower() for p in ["rua", "av", "alagoinhas", "bairro", "travessa", "praça", "r."]):
                    endereco = texto[2::]
                    break

            if not endereco:
                logging.warning(f"Endereço não encontrado para: {nome}")
                continue

            if servico_loja.loja_existe(endereco):
                logging.info(f"Loja já existe: {nome} - {endereco}")
                continue

            loja = Loja(nome=nome, endereco=endereco)

            servico_loja.salvarLoja(loja)
            total_inseridas += 1
            logging.info(f"Inserida: {loja.nome} - {loja.endereco}")


        except Exception as e:
            logging.error(f"Erro ao processar resultado: {e}")

    driver.quit()

    logging.info(f"Busca concluída. {total_inseridas} novas lojas inseridas.")


