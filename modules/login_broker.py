# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# import os
# from time import sleep
# from threading import Lock
# import json

# # from modules.get_razao_social import search_name
# # from modules.read_sheet import read_sheet, update_data

# class ProjetoBroker():

#     def __init__(self):

#         self.selenium_lock = Lock()

#         self.userData = None
#         self.authToken = None

#         self.url = 'https://lead.brokers.mktlab.app/'

#         self.options = webdriver.ChromeOptions()
#         self.options.add_argument("--disable-blink-features=AutomationControlled")
#         self.options.add_argument("--ignore-certificate-errors")
#         # self.options.add_argument("--timeout=120")
#         self.options.add_argument("--headless=new")
#         self.options.add_argument("--window-position=0,0")
#         self.options.add_argument("--window-size=800,600")

#         self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         self.options.add_experimental_option("useAutomationExtension", False)
#         self.downloadDir = os.path.join(os.path.expanduser('~'),'Downloads')
#         prefs = {
#                 "profile.default_content_settings.popups": 0,
#                 "download.default_directory": self.downloadDir,
#                 "download.prompt_for_download": False,
#                 "download.directory_upgrade": True
#                 }
#         self.options.add_experimental_option("prefs",prefs)
#         # user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data", "Projetos Matriz")
#         user_data_dir = os.path.join(os.path.dirname(__file__), "chrome_user_data", "Projetos Matriz")
#         self.options.add_argument(f"--user-data-dir={user_data_dir}")
#         self.options.add_argument(f"--profile-directory=Default")
#         self.options.add_argument("--disable-notifications")

#     def extrair_bearer(self):
        
#         with self.selenium_lock:

#             self.driver = webdriver.Chrome(service=Service(), options=self.options)
#             self.driver.get(self.url)
#             self.action_chain = ActionChains(self.driver)
#             while True:

#                 sleep(3)

#                 if self.driver.current_url == self.url:

#                     self.driver.find_element(By.TAG_NAME, "iframe").click()
                    
#                     for handle in self.driver.window_handles:
#                         self.driver.switch_to.window(handle)
#                         if "Fazer login nas Contas do Google" in self.driver.title:
#                             break


#                     self.driver.find_element(By.TAG_NAME, "input").send_keys("martins.gabriel@v4company.com")
#                     sleep(1)
#                     self.driver.find_elements(By.TAG_NAME, "button")[3].click()
#                     sleep(1)

#                     self.driver.find_element(By.TAG_NAME, "input").send_keys("987456123G@briel")
#                     sleep(1)
#                     self.driver.find_elements(By.TAG_NAME, "button")[3].click()
#                     sleep(1)

#                     self.driver.switch_to.default_content()
#                     sleep(5)

#                     cookies = self.driver.get_cookies()

#                     self.driver.quit()
#                     return f"Bearer {cookies[0]["value"]}"

#                 else:
#                     cookies = self.driver.get_cookies()
#                     self.driver.quit()
#                     return f"Bearer {cookies[0]["value"]}"



import os
import shutil
import uuid
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from time import sleep

class ProjetoBroker:

    def __init__(self):
        base_dir = os.path.join(os.path.dirname(__file__), "chrome_user_data")
        self.base_default = os.path.join(base_dir, "Default")

        # Cria uma pasta temporária ao lado da original
        temp_default_name = f"Default_Temp_{uuid.uuid4().hex[:8]}"
        self.temp_default = os.path.join(base_dir, temp_default_name)
        shutil.copytree(self.base_default, self.temp_default, dirs_exist_ok=True)

        # Configuração do Selenium
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless=new")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--window-size=800,600")
        # self.options.add_argument(f'--user-data-dir={os.path.dirname(self.temp_default)}')
        # self.options.add_argument(f'--profile-directory={os.path.basename(self.temp_default)}')  # Isso garante que use a nova Default_Temp_X

        self.options.add_argument(f'--user-data-dir={base_dir}')
        self.options.add_argument(f'--profile-directory=Default')  # Isso garante que use a nova Default_Temp_X

        # print(os.path.dirname(self.temp_default))
        # print(os.path.basename(self.temp_default))

    def iniciar_driver(self):
        driver = webdriver.Chrome(service=Service(), options=self.options)
        return driver

    # def extrair_bearer(self):
    #     driver = self.iniciar_driver()
    #     try:
    #         url = 'https://lead.brokers.mktlab.app/'
    #         driver.get(url)
    #         action_chain = ActionChains(driver)

    #         while True:
    #             sleep(3)

    #             if driver.current_url == url:
    #                 try:
    #                     driver.find_element(By.TAG_NAME, "iframe").click()

    #                     for handle in driver.window_handles:
    #                         driver.switch_to.window(handle)
    #                         if "Fazer login nas Contas do Google" in driver.title:
    #                             break
    #                     driver.find_element(By.TAG_NAME, "input").send_keys("martins.gabriel@v4company.com")
    #                     sleep(1)
    #                     driver.find_elements(By.TAG_NAME, "button")[3].click()
    #                     sleep(1)

    #                     driver.find_element(By.TAG_NAME, "input").send_keys("987456123G@briel")
    #                     sleep(1)
    #                     driver.find_elements(By.TAG_NAME, "button")[3].click()
    #                     sleep(1)

    #                     driver.switch_to.default_content()
    #                     sleep(5)

    #                     breakpoint()
    #                 except Exception as e:
    #                     print(f"Erro ao realizar login: {e}")

    #                 # Captura dos cookies
    #                 cookies = driver.get_cookies()
    #                 if cookies:
    #                     return f"Bearer {cookies[0]['value']}"

    #             else:
    #                 cookies = driver.get_cookies()
    #                 if cookies:
    #                     return f"Bearer {cookies[0]['value']}"

    #     finally:
    #         driver.quit()
    #         print(self.temp_default)
    #         shutil.rmtree(self.temp_default, ignore_errors=True)


    def extrair_bearer(self):
        driver = self.iniciar_driver()
        try:
            url = 'https://lead.brokers.mktlab.app/'
            driver.get(url)
            sleep(3)

            try:
                if driver.current_url == url:
                    # Tentativa de login via iframe
                    driver.find_element(By.TAG_NAME, "iframe").click()

                    for handle in driver.window_handles:
                        driver.switch_to.window(handle)
                        if "Fazer login nas Contas do Google" in driver.title:
                            break

                    driver.find_element(By.TAG_NAME, "input").send_keys("martins.gabriel@v4company.com")
                    sleep(1)
                    driver.find_elements(By.TAG_NAME, "button")[3].click()
                    sleep(1)

                    driver.find_element(By.TAG_NAME, "input").send_keys("987456123G@briel")
                    sleep(1)
                    driver.find_elements(By.TAG_NAME, "button")[3].click()
                    sleep(1)

                    driver.switch_to.default_content()
                    sleep(5)

                    breakpoint()

            except Exception as e:
                print(f"Erro ao realizar login: {e}")

            # Captura dos cookies (após tentativa de login ou se já logado)
            cookies = driver.get_cookies()
            if cookies:
                return f"Bearer {cookies[0]['value']}"

        finally:
            driver.quit()
            print(self.temp_default)
            shutil.rmtree(self.temp_default, ignore_errors=True)