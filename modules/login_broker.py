from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
from time import sleep
from threading import Lock
import tempfile
import shutil
import json

# from modules.get_razao_social import search_name
# from modules.read_sheet import read_sheet, update_data

class ProjetoBroker():

    def __init__(self):

        self.userData = None
        self.authToken = None

        self.url = 'https://lead.brokers.mktlab.app/'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--timeout=120")
        # self.options.add_argument("--headless=new")
        self.options.add_argument("--window-position=0,0")
        self.options.add_argument("--window-size=800,600")

        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        self.downloadDir = os.path.join(os.path.expanduser('~'),'Downloads')
        prefs = {
                "profile.default_content_settings.popups": 0,
                "download.default_directory": self.downloadDir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True
                }
        self.options.add_experimental_option("prefs",prefs)
        # user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data", "Projetos Matriz")
        user_data_dir = os.path.join(os.path.dirname(__file__), "chrome_user_data")
        self.temp_profile = tempfile.mkdtemp()
        shutil.copytree(user_data_dir, self.temp_profile, dirs_exist_ok=True)
        self.options.add_argument(f"--user-data-dir={self.temp_profile}")
        self.options.add_argument(f"--profile-directory=Default")
        self.options.add_argument("--disable-notifications")

    def extrair_bearer(self):
        

        self.driver = webdriver.Chrome(service=Service(), options=self.options)
        self.driver.get(self.url)
        self.action_chain = ActionChains(self.driver)

        try:
            sleep(3)

            if self.driver.current_url == self.url:

                self.driver.find_element(By.TAG_NAME, "iframe").click()
                
                for handle in self.driver.window_handles:
                    self.driver.switch_to.window(handle)
                    if "Fazer login nas Contas do Google" in self.driver.title:
                        break


                self.driver.find_element(By.TAG_NAME, "input").send_keys("martins.gabriel@v4company.com")
                sleep(1)
                self.driver.find_elements(By.TAG_NAME, "button")[3].click()
                sleep(1)

                self.driver.find_element(By.TAG_NAME, "input").send_keys("987456123G@briel")
                sleep(1)
                self.driver.find_elements(By.TAG_NAME, "button")[3].click()
                sleep(1)

                self.driver.switch_to.default_content()
                sleep(5)

                # cookies = self.driver.get_cookies()
                # self.driver.quit()
                # return f"Bearer {cookies[0]["value"]}"

        finally:
            cookies = self.driver.get_cookies()
            self.driver.quit()
            shutil.rmtree(self.temp_profile, ignore_errors = True)
            return f"Bearer {cookies[0]["value"]}"


# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.common.action_chains import ActionChains
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.support.wait import WebDriverWait
# # from selenium import webdriver
# # from webdriver_manager.chrome import ChromeDriverManager
# # from selenium.webdriver.chrome.service import Service
# # import os
# # import glob
# # from time import sleep
# # import tempfile
# # import shutil
# # import json

# # class ProjetoBroker():

# #     def __init__(self):
# #         self.userData = None
# #         self.authToken = None
# #         self.url = 'https://lead.brokers.mktlab.app/'

# #         self.user_data_dir = os.path.join(os.path.dirname(__file__), "chrome_user_data", "Projetos Matriz")
# #         self.downloadDir = os.path.join(os.path.expanduser('~'),'Downloads')

# #     def limpar_locks(self, user_data_dir):
# #         locks = glob.glob(os.path.join(user_data_dir, "Singleton*"))
# #         for lock in locks:
# #             try:
# #                 os.remove(lock)
# #             except Exception:
# #                 pass

# #     def iniciar_driver(self):
# #         # Limpa locks do perfil fixo para evitar travamentos
# #         self.limpar_locks(self.user_data_dir)

# #         # Cria pasta temporária para perfil clonando o fixo
# #         temp_profile = tempfile.mkdtemp()
# #         shutil.copytree(self.user_data_dir, temp_profile, dirs_exist_ok=True)

# #         # Cria ChromeOptions a cada execução para evitar acumulo de args
# #         options = webdriver.ChromeOptions()
# #         options.add_argument("--disable-blink-features=AutomationControlled")
# #         options.add_argument("--ignore-certificate-errors")
# #         options.add_argument("--headless=new")
# #         options.add_argument("--window-position=0,0")
# #         options.add_argument("--window-size=800,600")
# #         options.add_experimental_option("excludeSwitches", ["enable-automation"])
# #         options.add_experimental_option("useAutomationExtension", False)
# #         prefs = {
# #             "profile.default_content_settings.popups": 0,
# #             "download.default_directory": self.downloadDir,
# #             "download.prompt_for_download": False,
# #             "download.directory_upgrade": True
# #         }
# #         options.add_experimental_option("prefs", prefs)
# #         options.add_argument("--disable-notifications")

# #         # Usa o perfil temporário (cópia do fixo)
# #         options.add_argument(f"--user-data-dir={temp_profile}")

# #         driver = webdriver.Chrome(service=Service(), options=options)
# #         return driver, temp_profile

# #     def extrair_bearer(self):
# #         driver, temp_profile = self.iniciar_driver()
# #         try:
# #             driver.get(self.url)
# #             self.action_chain = ActionChains(driver)

# #             sleep(3)
# #             if driver.current_url == self.url:
# #                 driver.find_element(By.TAG_NAME, "iframe").click()

# #                 for handle in driver.window_handles:
# #                     driver.switch_to.window(handle)
# #                     if "Fazer login nas Contas do Google" in driver.title:
# #                         break

# #                 driver.find_element(By.TAG_NAME, "input").send_keys("martins.gabriel@v4company.com")
# #                 sleep(1)
# #                 driver.find_elements(By.TAG_NAME, "button")[3].click()
# #                 sleep(1)

# #                 driver.find_element(By.TAG_NAME, "input").send_keys("987456123G@briel")
# #                 sleep(1)
# #                 driver.find_elements(By.TAG_NAME, "button")[3].click()
# #                 sleep(1)

# #                 driver.switch_to.default_content()
# #                 sleep(5)


# #         finally:
# #             cookies = driver.get_cookies()
# #             driver.quit()
# #             shutil.rmtree(temp_profile, ignore_errors=True)
# #             return f"Bearer {cookies[0]['value']}"

