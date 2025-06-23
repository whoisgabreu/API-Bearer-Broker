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
import threading
import json

# from modules.get_razao_social import search_name
# from modules.read_sheet import read_sheet, update_data

class ProjetoBroker():

    def __init__(self):

        self.selenium_lock = threading.Lock

        self.userData = None
        self.authToken = None

        self.url = 'https://lead.brokers.mktlab.app/'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--ignore-certificate-errors")
        # self.options.add_argument("--timeout=120")
        self.options.add_argument("--headless=new")
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
        user_data_dir = os.path.join(os.path.dirname(__file__), "chrome_user_data", "Projetos Matriz")
        self.options.add_argument(f"--user-data-dir={user_data_dir}")
        self.options.add_argument(f"--profile-directory=Default")
        self.options.add_argument("--disable-notifications")

    def extrair_bearer(self):
        
        with self.selenium_lock:

            self.driver = webdriver.Chrome(service=Service(), options=self.options)
            self.driver.get(self.url)
            self.action_chain = ActionChains(self.driver)
            while True:

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

                    cookies = self.driver.get_cookies()

                    self.driver.quit()
                    return f"Bearer {cookies[0]["value"]}"

                else:
                    cookies = self.driver.get_cookies()
                    self.driver.quit()
                    return f"Bearer {cookies[0]["value"]}"
