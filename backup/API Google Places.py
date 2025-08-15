import requests

API_KEY = 'SUA_API_KEY_AQUI'
BUSCA = 'Padaria Pão Quente Belo Horizonte'

# 1. Buscar lugar pelo nome
search_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
params = {
    'input': BUSCA,
    'inputtype': 'textquery',
    'fields': 'place_id',
    'key': API_KEY
}
response = requests.get(search_url, params=params).json()
place_id = response['candidates'][0]['place_id']

# 2. Obter detalhes do lugar
details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
params = {
    'place_id': place_id,
    'fields': 'name,formatted_address,photos',
    'key': API_KEY
}
details = requests.get(details_url, params=params).json()
photos = details['result'].get('photos', [])

# 3. Montar URL da primeira imagem
if photos:
    photo_reference = photos[0]['photo_reference']
    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo_reference}&key={API_KEY}"
    print(f"URL da imagem: {photo_url}")
else:
    print("Nenhuma imagem encontrada.")
