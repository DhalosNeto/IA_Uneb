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
<<<<<<< HEAD
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.Nv2PK.THOPZb.CpccDe ")))

=======
>>>>>>> feature/metodo_pergunta

    sleep(5)
    print('Carregando mais resultados...')
    painel = driver.find_element(By.XPATH, '//div[@role="feed"]')
<<<<<<< HEAD
    for _ in range(10):  
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", painel)
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
=======

    total_inseridas = 0
    tentativas_sem_novas = 0
    max_tentativas = 5  # segurança para evitar loop infinito

    while total_inseridas < 50 and tentativas_sem_novas < max_tentativas:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", painel)
        sleep(2)

        resultados = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
        novas_rodada = 0

        for elemento in resultados:
            try:
                nome = elemento.find_element(By.CSS_SELECTOR, "a.hfpxzc").text.strip()
                if not nome:
                    continue
>>>>>>> feature/metodo_pergunta

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

<<<<<<< HEAD
            if servico_loja.loja_existe(endereco):
                logging.info(f"Loja já existe: {nome} - {endereco}")
                continue

            loja = Loja(nome=nome, endereco=endereco)

            servico_loja.salvarLoja(loja)
            total_inseridas += 1
            logging.info(f"Inserida: {loja.nome} - {loja.endereco}")
=======
                if not endereco:
                    continue

                if servico_loja.loja_existe(nome, endereco):
                    continue

                loja = Loja(nome=nome, endereco=endereco, email=None)
                repo.salvar(loja)
>>>>>>> feature/metodo_pergunta

                total_inseridas += 1
                novas_rodada += 1
                logging.info(f"Inserida: {loja.nome} - {loja.endereco}")

                if total_inseridas >= 50:
                    break

            except Exception as e:
                logging.error(f"Erro ao processar resultado: {e}")

        if novas_rodada == 0:
            tentativas_sem_novas += 1
        else:
            tentativas_sem_novas = 0  # zera se encontrar novas

    driver.quit()
    logging.info(f"Busca concluída. {total_inseridas} novas lojas inseridas.")

<<<<<<< HEAD

=======
if __name__ == "__main__":
    buscar_lojas_google_maps()
>>>>>>> feature/metodo_pergunta
