import requests

# Realizar um teste de conexão HTTP
def test_http_connection(url, id):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Verifica se a solicitação HTTP foi bem-sucedida

        if response.status_code == 200:
            print(f"Conexão HTTP para {url} bem-sucedida. Código de status: {response.status_code}")
        else:
            print(f"Conexão HTTP para {url} não retornou o código de status 200.")
    except requests.exceptions.RequestException as e:
        print(f"Erro na conexão HTTP para {url}: {e}")
    
# Exemplo de uso:
url1 = "http://10.8.0.26:90"
url2 = "http://191.222.56.124:8080"

test_http_connection(url1, 1)
test_http_connection(url2, 2)
