from PIL import Image, ImageTk
import requests


# Função que redimensiona o ícone corretamente
def carregar_icone(caminho, tamanho):
    return ImageTk.PhotoImage(Image.open(caminho).resize((tamanho, tamanho), Image.Resampling.LANCZOS))


# Função que busca pelo endereço e retorna latitude e longitude
def geocode_address(rua, numero, bairro, uf, municipio):
    api_key = 'AIzaSyABmCB47c_S2N3MY5aG0mugy2LvVR_L3L8'
    endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': f'{rua}, {numero}, {bairro}, {uf}, {municipio}',
        'key': api_key
    }

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()

        if response.status_code == 200 and data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            return latitude, longitude
        else:
            print(f"Erro na requisição: {data['status']}")
            return None, None
    except Exception as e:
        print(f"Erro ao acessar API do Google Maps: {e}")
        return None, None


# Função para limitar os caractéres
def limitar_caracteres(entry_text):
    return len(entry_text) <= 40
