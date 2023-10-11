
import requests
import base64
import json

arraytoout = []
listajm = []
def getapi():
    url = 'http://192.168.10.220/system/update_panel_sactus/api/get_list.php'
    dados = {'category': 'access'}
    dados_json = json.dumps(dados)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=dados_json, headers=headers)

    if response.status_code == 200:
        resposta_json = response.json()
        if resposta_json.get("status") == True:
            print("get ok")
            
            message_value = resposta_json.get("message")
    

    else:
        # A solicitação falhou
        print(f'Erro na solicitação. Código de status: {response.status_code}')
    return message_value

def test_http_connection(url, id):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        
        if response.status_code == 200:
            #print(f"Conexão HTTP para {url} bem-sucedida. Código de status: {response.status_code}")
            valor = (str(id) +":1")
            arraytoout.append(valor)
        else:
            print(f"Conexão HTTP para {url} não retornou o código de status 200.")

    except requests.exceptions.RequestException as e:
        #print(f"Erro na conexão HTTP para {url}: {e}")
        valor = (str(id) +":0")
        arraytoout.append(valor)


def base64decode(stringcoded):
    decoded_bytes = base64.b64decode(stringcoded)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

code = getapi()
decoded_string = base64decode(code)
array = json.loads(decoded_string)


for elemento in array:
    id = elemento["id"]
    cnpj = elemento["cnpj"]
    ipex = elemento["ip_externo_servidor"]
    porta = elemento["porta_http"]

    if porta == "":
        porta = "80"

    if ipex != "jmconsultorias.com.br":
        url = ('http://' +str(ipex) +":" +str(porta))
        test_http_connection(url, id)
    else:
        listajm.append(id)



print(arraytoout)



json_string = json.dumps(arraytoout)
nome_arquivo = "saida.json"
with open(nome_arquivo, "w") as arquivo:
    arquivo.write(json_string)

print(f'Saída JSON foi salva em "{nome_arquivo}"')

    



