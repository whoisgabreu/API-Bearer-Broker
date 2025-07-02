from playwright.sync_api import sync_playwright
from time import sleep

import requests
from bs4 import BeautifulSoup
import random
from rapidfuzz import fuzz

class GoogleTransparency:

    def __init__(self):
        self.url = 'https://adstransparency.google.com/?hl=pt-BR&region=anywhere'
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

    def analyse(self, business_info) -> dict:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--ignore-certificate-errors",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--window-position=0,0",
                    "--window-size=800,600"
                ]
            )

            context = browser.new_context(
                viewport={"width": 800, "height": 600},
                user_agent=self.user_agent,
                ignore_https_errors=True
            )

            page = context.new_page()
            page.goto(self.url, timeout=60000)

            # Preenche o campo de busca
            input_area = page.query_selector(".input-area")
            if input_area:
                input_area.fill(business_info["empresa"]["razao_social"])
            else:
                print("Input area não encontrado.")

            sleep(1)  # Se quiser, depois pode trocar por wait_for_selector

            # Verificar presença do seletor de quantidade de anúncios
            pres_online = page.evaluate("""
                () => {
                    return document.querySelector(".ads-count-legacy") ? true : false;
                }
            """)

            quant_ads = page.evaluate("""
                () => {
                    const el = document.querySelector(".ads-count-legacy");
                    return el ? el.textContent.replace("~", "").split(" ")[0] : "0";
                }
            """)

            browser.close()

            business_info.setdefault("ads", {}).setdefault("google_transparency", {})
            business_info["ads"]["google_transparency"]["presenca_online"] = pres_online
            business_info["ads"]["google_transparency"]["qtd_anuncio"] = int(quant_ads)

            return business_info

class GoogleBusiness: # NÃO FUNCIONA NA VPS POR QUESTÕES DE CAPTCHA

    def __init__(self):
        self.userData = None
        self.authToken = None

    def analyse(self, business_info) -> dict:

        if business_info["empresa"]["nome_fantasia"] != None:
            print("entrou aqui")
            url = "https://www.google.com/search?q=" + business_info["empresa"]["nome_fantasia"]

            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--ignore-certificate-errors",
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--window-position=0,0",
                        "--window-size=800,600",
                    ]
                )

                # ✅ User-Agent Fake de Desktop (Chrome realístico)
                context = browser.new_context(
                    viewport={"width": 800, "height": 600},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    ignore_https_errors=True
                )

                page = context.new_page()

                page.goto(url, timeout=60000)
                sleep(2)

                botoes = page.query_selector_all(".bkaPDb")
                print(botoes)
                print("html",page.content())
                for botao in botoes:
                    span = botao.query_selector("span")
                    print(span.inner_text())
                    if span.inner_text() == "Avaliar":
                        print(span.inner_text())
                        href = botao.query_selector("a").get_attribute("href")
                        new_url = f"https://google.com{href}"
                        page.goto(new_url, timeout=60000)

                        presenca = page.evaluate("""
                            () => {
                                return document.querySelector(".Aq14fc") ? true : false;
                            }
                        """)

                        nota = page.evaluate("""
                            () => {
                                const el = document.querySelector(".Aq14fc");
                                return el ? parseFloat(el.innerText.replace(",", ".")) : 0;
                            }
                        """)

                        qtd_avaliacoes = page.evaluate("""
                            () => {
                                const el = document.querySelector(".rjxHPb.PZPZlf span a span");
                                return el ? el.innerText : "0";
                            }
                        """)

                        business_info.setdefault("ads", {}).setdefault("google_business", {})
                        business_info["ads"]["google_business"]["presenca_online"] = presenca
                        business_info["ads"]["google_business"]["nota"] = nota
                        business_info["ads"]["google_business"]["qtd_avaliacao"] = int(qtd_avaliacoes.split(" ")[0])

                browser.close()

        else:
            business_info.setdefault("ads", {}).setdefault("google_business", {})
            business_info["ads"]["google_business"]["presenca_online"] = False
            business_info["ads"]["google_business"]["nota"] = 0
            business_info["ads"]["google_business"]["qtd_avaliacao"] = 0

        return business_info

class DuckDuckGo:


    def buscar(self, razao_social, tipo_busca):
        """
        Tipo_busca = [.br, instagram.com, facebook.com]
        """

        def checar_similaridade(arg1, arg2):
            
            # remover = [" ","www.",".com",".br"]
            # for item in remover:
            #     arg1 = arg1.replace(item, "")
            #     arg2 = arg2.replace(item, "")

            # print(arg1, arg2)

            # arg1 = arg1.lower().replace(" ", "")
            # arg2 = arg2.lower()
            similaridade = fuzz.ratio(arg1, arg2)
            # print(similaridade)

            if similaridade > 60:
                return True
            else:
                return False
            
        timer = random.randrange(5,10)
        sleep(timer)

        query = f"{razao_social} site:{tipo_busca}"
        url = f"https://duckduckgo.com/html/?q={query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.select('.result__url')
        for link in links:
            # print(link.get_text().strip())
            link_text = link.get_text().strip()
            if tipo_busca == ".br":
                partes = link_text.split(".")
                if len(partes) > 1:
                    link_check = partes[1]
                else:
                    continue
            else:
                partes = link_text.split("/")
                if len(partes) > 1:
                    link_check = partes[1]
                else:
                    continue
            result = checar_similaridade(razao_social, link_check)
            print(result)
            if result:
                return link.get_text().strip()
            else:
                return None


# dic = {"paginas_online":[]}

# dic["paginas_online"].append(DuckDuckGo().buscar("Direção Concursos", ".br"))
# dic["paginas_online"].append(DuckDuckGo().buscar("Direção Concursos", "instagram.com"))
# dic["paginas_online"].append(DuckDuckGo().buscar("Direção Concursos", "facebook.com"))

# print(dic)