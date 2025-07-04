# import asyncio
# import aiohttp
# from aiolimiter import AsyncLimiter


# class CnpjaCustomAPI:
#     def __init__(self):
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
#         }
#         # 5 requests por minuto = 5 req/60s
#         self.limiter = AsyncLimiter(max_rate=3, time_period=60)

#     async def fetch(self, session, url):
#         async with self.limiter:  # respeita limite
#             async with session.get(url, headers=self.headers) as response:
#                 if response.status != 200:
#                     print(f"Erro em {url}")
#                 return await response.json()

#     async def search(self, nome) -> list:
#         async with aiohttp.ClientSession() as session:
#             url = f"https://bff.cnpja.com/search?query={nome}"
#             data = await self.fetch(session, url)
#             return [
#                 {"uuid": x["person"]["id"], "name": x["person"]["name"]}
#                 for x in data["records"] if x["index"] == "person"
#             ]

#     async def person_search(self, uuids: list) -> list:
#         tasks = []
#         async with aiohttp.ClientSession() as session:
#             for uuid in uuids:
#                 url = f"https://bff.cnpja.com/person/{uuid['uuid']}"
#                 tasks.append(self.fetch(session, url))
#             responses = await asyncio.gather(*tasks)
#             all_companies = []
#             for resp in responses:
#                 companies = [
#                     {"id": x["company"]["id"], "name": x["company"]["name"]}
#                     for x in resp["membership"]
#                 ]
#                 all_companies.extend(companies)
#             return all_companies

#     async def company_search(self, company_id_list: list) -> list:

#         tasks = []
#         async with aiohttp.ClientSession() as session:
#             for company_id in company_id_list:
#                 url = f"https://bff.cnpja.com/company/{company_id['id']}"
#                 tasks.append(self.fetch(session, url))
#             responses = await asyncio.gather(*tasks)
#             offices = []
#             for resp in responses:
#                 offices.append({
#                     "name": resp["name"],
#                     "alias": resp["offices"][0]["alias"],
#                     "cnpj": resp["offices"][0]["taxId"]
#                 })
#             return offices
        
#     async def office_search(self, office_cnpj:str) -> list:
#         tasks = []
#         async with aiohttp.ClientSession() as session:
#             url = f"https://bff.cnpja.com/office/{office_cnpj}"
#             tasks.append(self.fetch(session, url))
#             responses = await asyncio.gather(*tasks)
#             # Faça o que quiser com os responses
#             return responses
        

# def coletar_cnpj(s1, s2):
#     import asyncio
#     from rapidfuzz import fuzz

#     api = CnpjaCustomAPI()

#     def checar_similaridade(arg1, arg2):
#         return fuzz.ratio(arg1, arg2)

#     async def main(nome_socio: str, nome_fantasia: str):
#         pessoas = await api.search(nome_socio)
#         # print("Pessoas:", pessoas)

#         companies = await api.person_search(pessoas)
#         # print("Empresas:", companies)

#         offices = await api.company_search(companies)
#         # print("Offices:", offices)

#         for office in offices:
#             similaridade = checar_similaridade(
#                 nome_fantasia.lower(), office["alias"].lower()
#             )
#             if similaridade > 80:
#                 office_data = await api.office_search(office["cnpj"])
#                 return office_data
#         return None  # caso não ache nada

#     try:
#         # Envolve tudo com timeout de 180 segundos (3 minutos)
#         resultado = asyncio.run(
#             asyncio.wait_for(main(s1, s2), timeout=180)
#         )
#     except asyncio.TimeoutError:
#         # print("Tempo limite excedido! A coleta foi cancelada.")
#         return {"timeout":"Não foi possivel localizar as informações desejadas dentro do tempo limite (3min)."}

#     return resultado


import asyncio
from aiolimiter import AsyncLimiter
import aiohttp
from rapidfuzz import fuzz


# ------------------------------------------
# Configuração do limiter global
# ------------------------------------------

global_limiter = AsyncLimiter(max_rate=3, time_period=60)


# ------------------------------------------
# Client API
# ------------------------------------------

class CnpjaCustomAPI:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            )
        }
        self.limiter = global_limiter

    async def fetch(self, session, url):
        async with self.limiter:
            async with session.get(url, headers=self.headers) as response:
                if response.status != 200:
                    print(f"Erro em {url}: {response.status}")
                return await response.json()

    async def search(self, session, nome: str) -> list:
        url = f"https://bff.cnpja.com/search?query={nome}"
        data = await self.fetch(session, url)
        return [
            {"uuid": x["person"]["id"], "name": x["person"]["name"]}
            for x in data["records"]
            if x["index"] == "person"
        ]

    async def person_search(self, session, uuids: list) -> list:
        tasks = []
        for uuid in uuids:
            url = f"https://bff.cnpja.com/person/{uuid['uuid']}"
            tasks.append(self.fetch(session, url))
        responses = await asyncio.gather(*tasks)
        all_companies = []
        for resp in responses:
            companies = [
                {"id": x["company"]["id"], "name": x["company"]["name"]}
                for x in resp["membership"]
            ]
            all_companies.extend(companies)
        return all_companies

    async def company_search(self, session, company_id_list: list) -> list:
        tasks = []
        for company_id in company_id_list:
            url = f"https://bff.cnpja.com/company/{company_id['id']}"
            tasks.append(self.fetch(session, url))
        responses = await asyncio.gather(*tasks)
        offices = []
        for resp in responses:
            offices.append({
                "name": resp["name"],
                "alias": resp["offices"][0]["alias"],
                "cnpj": resp["offices"][0]["taxId"],
            })
        return offices

    async def office_search(self, session, office_cnpj: str):
        url = f"https://bff.cnpja.com/office/{office_cnpj}"
        return await self.fetch(session, url)


# ------------------------------------------
# Função principal
# ------------------------------------------

async def coletar_cnpj(socio: str, alias: str):
    api = CnpjaCustomAPI()

    def checar_similaridade(a, b):
        return fuzz.ratio(a, b)

    async with aiohttp.ClientSession() as session:
        pessoas = await api.search(session, socio)
        print(f"[DEBUG] Pessoas encontradas: {pessoas}")

        companies = await api.person_search(session, pessoas)
        print(f"[DEBUG] Empresas encontradas: {companies}")

        offices = await api.company_search(session, companies)
        print(f"[DEBUG] Offices encontrados: {offices}")

        for office in offices:
            office_alias = office.get("alias", "")
            if office_alias:
                similaridade = checar_similaridade(alias.lower(), office_alias.lower())
                print(f"[DEBUG] Similaridade: {similaridade} - {office['alias']}")
                if similaridade > 80:
                    office_data = await api.office_search(session, office["cnpj"])
                    return office_data

        return {"message": "Nenhuma correspondência encontrada"}

async def criar_lista_fria(socio: str, alias: str):
    api = CnpjaCustomAPI()

    def checar_similaridade(a, b):
        return fuzz.ratio(a, b)

    async with aiohttp.ClientSession() as session:
        try:
            pessoas = await api.search(session, socio)
            print(f"[DEBUG] Pessoas encontradas: {pessoas}")

            companies = await api.person_search(session, pessoas)
            print(f"[DEBUG] Empresas encontradas: {companies}")

            offices = await api.company_search(session, companies)
            print(f"[DEBUG] Offices encontrados: {offices}")

            office_list = []

            for office in offices:
                office_alias = office.get("alias", "")
                if office_alias:
                    similaridade = checar_similaridade(alias.lower(), office_alias.lower())
                    print(f"[DEBUG] Similaridade: {similaridade} - {office_alias}")

                    if similaridade < 70:
                        office_data = await api.office_search(session, office["cnpj"])
                        office_list.append(office_data)

            if office_list:
                return office_list

            return {"message": "Nenhuma correspondência encontrada"}

        except Exception as e:
            print(f"[ERRO] Falha na criação da lista fria: {e}")
            return {"error": str(e)}