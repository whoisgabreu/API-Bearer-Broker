import os
import shutil
import uuid
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from time import sleep

class ProjetoBroker:

    def __init__(self):
        base_dir = os.path.join(os.path.dirname(__file__), "chrome_user_data")
        print(webdriver.__version__)

        # Configuração do Selenium
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless=new")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--window-size=800,600")

        self.options.add_argument(f'--user-data-dir={base_dir}')
        self.options.add_argument(f'--profile-directory=Default')  # Isso garante que use a Default

    def iniciar_driver(self):
        driver = webdriver.Chrome(service=Service(), options=self.options)
        return driver

    def extrair_bearer(self):


        def trocar_janela(driver, titulo_janela):
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                if titulo_janela in driver.title:
                    break
                


        driver = self.iniciar_driver()
        actionChains = ActionChains(driver)
        try:
            url = 'https://lead.brokers.mktlab.app/'
            driver.get(url)
            sleep(3)
            # breakpoint()
            try:
                if driver.current_url == url:

                    driver.find_element(By.TAG_NAME, "iframe").click()

                    trocar_janela(driver, "Fazer login nas Contas do Google")
                    
                    logado = False if driver.find_element(By.TAG_NAME, "h1").text in ["Fazer login","Sign in"] else True
                    print(logado)
                    if logado:
                        actionChains.send_keys(Keys.TAB)
                        actionChains.send_keys(Keys.TAB)
                        actionChains.send_keys(Keys.ENTER)
                        actionChains.perform()
                        sleep(5)
                        trocar_janela(driver, "Lead Broker - V4 Company")
                    
                    else:

                        driver.find_element(By.TAG_NAME, "input").send_keys("martins.gabriel@v4company.com")
                        sleep(1)
                        driver.find_elements(By.TAG_NAME, "button")[3].click()
                        sleep(1)
                        driver.find_element(By.TAG_NAME, "input").send_keys("987456123G@briel")
                        sleep(1)
                        driver.find_elements(By.TAG_NAME, "button")[3].click()
                        sleep(1)
                        trocar_janela(driver, "Lead Broker - V4 Company")



            except Exception as e:
                print(f"Erro ao realizar login: {e}")


        finally:
            # Captura dos cookies (após tentativa de login ou se já logado)
            cookies = driver.get_cookies()
            driver.quit()
            if cookies:
                return f"Bearer {cookies[0]['value']}"