#<!DOCTYPE PYTHON>
#Escrito por Thiago barros / Jimmy-neutron
#Script para verificaçao de status dos servidores locais de clientes se esta online ou offline.

#____IMPORTS____
import requests
import base64
import json
import time
import datetime

#____VARIAVEIS INICIAIS____
arraytoout = []
listajm = []

#____FUNCAO DE LOG____
def escrever_log(mensagem):
    data_atual = datetime.datetime.now()
    data_formatada = data_atual.strftime("%Y-%m-%d %H:%M:%S")
    log = f"[{data_formatada}] {mensagem}\n"

    try:
        with open("bkp.log", "a") as arquivo:
            arquivo.write(log)
    except IOError:
        print("erro!")
#____FIM DA FUNCAO____

#____GETAPI, FUNCAO PARA COLETAR DADOS DOS SERVIDORES ATIVOS____
def getapi():
    #VARIAVEIS DE ACESSO A API
    url = 'http://192.168.10.220/system/update_panel_sactus/api/get_list.php'
    dados = {'category': 'access'}
    dados_json = json.dumps(dados)
    headers = {'Content-Type': 'application/json'}
    #POST
    response = requests.post(url, data=dados_json, headers=headers)
    #TRATAMENTO E RETURN DOS DADOS OBTIDOS
    while True:
        try:
            response = requests.post(url, data=dados_json, headers=headers)
            response.raise_for_status()  # Isso gera uma exceção se o código de resposta não for 2xx
            resposta_json = response.json()
            if resposta_json.get("status") == True:
                print("get ok")
                message_value = resposta_json.get("message")
                return message_value
        except requests.exceptions.RequestException as e:
            print("Erro na requisição:", e)
            # Espera um tempo antes de tentar novamente (evitar sobrecarregar o servidor)
            time.sleep(5)
            continue 
#____FIM DA FUNCAO____

#____TESTEHTTPCONN, FUNCAO PARA TESTAR SE O CLIENTE ESTA OFFLINE____
def test_http_connection(url, id, cnpj):
    #TESTE DE CONEXAO
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        #SE 200(OK) NADA SERA FEITO
        if response.status_code == 200:
            print("conexao http ok")
        #OU SE OUTRO ERRO, INDICANDO QUE O HTTP ESTA RESPONDENDO
        else:
            print(f"Conexão HTTP para {url} não retornou o código de status 200.")
    #NA FALTA DE RESPOSTA GUARDA SE OS DADOS 
    except requests.exceptions.RequestException as e:
        valor = (id, cnpj)
        arraytoout.append(valor)
#____FIM DA FUNCAO____

#____BASE64DECODE, FUNCAO USADA PARA DECODIFICAR OS DADOS RECEBIDOS DE GETAPI____
def base64decode(stringcoded):
    decoded_bytes = base64.b64decode(stringcoded)
    decoded_string = decoded_bytes.decode('utf-8')
    #A RESPOSTA EM UTF8 E RETORNADA
    return decoded_string
#____FIM DA FUNCAO____

#____POSTAPIID, FUNCAO PARA ENVIAR OS DADOS OBTIDOS PARA O SERVIDOR INTERNO____
def postapiid(arraypost):
    #VARIAVEIS DE ACESSO A API
    url = 'http://192.168.10.220/system/update_panel_sactus/api/get_list.php'
    dados = {"type": "server_offline", "list": arraypost}
    dados_json = json.dumps(dados)
    headers = {'Content-Type': 'application/json'}
    #POST
    response = requests.post(url, data=dados_json, headers=headers)
    #TRATAMENTO E VERIFICAÇAO SE OBTEVE SUCESSO
    if response.status_code == 200:
        resposta_json = response.json()
        if resposta_json.get("status") == True:
            if resposta_json.get("message") =="OK":
                print("post id ok")
            else:
                print("A message post id nao e ok")
        else:
            print("O status post id nao e True")
    else:
        print("erro de post id ... " +str(response.status_code))
#____FIM DA FUNCAO____

#____POSTAPICNPJ, FUNCAO PARA ENVIO DE DADOS OBTIDOS PARA O SERVIDOR LOCAWEB
def postapicnpj(arraypost):
    #VARIAVEIS DE ACESSO A API
    url = 'https://jmsistemas.com.br/api/bi'
    dados = {"type": "server_offline", "list": arraypost}
    dados_json = json.dumps(dados)
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': '8cdf018ef4e26e3cc32f311eb84a987b', 'X-Authorization': '8cdf018ef4e26e3cc32f311eb84a987b'}
    #POST
    response = requests.post(url, data=dados_json, headers=headers)
    #TRATAMENTO E VERIFICAÇAO SE OBTEVE SUCESSO
    if response.status_code == 200:
        resposta_json = response.json()
        if resposta_json.get("status") == True:
            print("post cnpj ok")
        else:
            print("O status de post cnpj nao e True")
    else:
        print("erro de post cnpj... " +str(response.status_code))
#____FIM DA FUNCAO____



#___________________________________________
#_________LOOP DE EXECUCAO CONTINUO_________
while True:
    print("Executando a cada 5 minutos...")
    #____CHAMADA DE DADOS
    code = getapi()
    #____DECODE DE DAOS
    decoded_string = base64decode(code)
    #____CONVERSAO DE DADOS
    array = json.loads(decoded_string)
    #____LOOP PARA EXECUCAO UM A UM
    for elemento in array:
        id = elemento["id"]
        cnpj = elemento["cnpj"]
        ipex = elemento["ip_externo_servidor"]
        porta = elemento["porta_http"]
        #CERTIFICAÇAO QUE SEMPRE USA PELOMENOS O PADRAO
        if porta == "":
            porta = "80"
        #NAO EXECUTANDO O QUE NOS HOSPEDAMOS PELA CERTEZA DO UPTIME
        if ipex != "jmconsultorias.com.br":
            #MONTANDO A URL E CHAMANDO O TESTE
            url = ('http://' +str(ipex) +":" +str(porta))
            test_http_connection(url, id, cnpj)
        else:
            listajm.append(id)
    #SEPARANDO DADOS PARA ENVIAR
    id, cnpj = zip(*arraytoout)
    #ENVIANDO DADOS PARA SERVIDOR INTERNO
    postapiid(id)
    #ENVIANDO DADOS PARA SERVIDOR LOCAWEB
    postapicnpj(cnpj)
    time.sleep(300)    
#___________________________________________
#______________END-OF-CODING________________
#_ESCRITO-POR-THIAGO-BARROS/JIMMY-NEUTRON___
#___________________________________________
    



