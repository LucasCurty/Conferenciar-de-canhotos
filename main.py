from selenium import webdriver
from acessos import LOGIN,SENHA,URL,CAMINHO
from pastas import create_folders, rename_arquivos
import time
from datetime import date
import os

data = date.today().strftime("%d-%m-%Y")
#renomeando canhotos
lista_canhotos = rename_arquivos()
#----------iniciando aplicação
print("INICIANDO AUTOMAÇÃO !\n")
print("CONFERINDO PASTAS...\n")
create_folders() # verificando pastas
print(" [   Pastas Verificadas    ]\n")

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options)
driver.get(URL)

#Acessando a pagina
driver.maximize_window()
driver.find_element('xpath','//*[@id="Usuario"]').send_keys(LOGIN)
driver.find_element('xpath','//*[@id="Senha"]').send_keys(SENHA)
driver.find_element('xpath','//*[@id="login-form"]/div[2]/div[3]/button').click()
time.sleep(3)
driver.find_element('xpath','//*[@id="js-nav-menu"]/li[6]/a').click()
driver.find_element('xpath','//*[@id="js-nav-menu"]/li[6]/ul/li[1]/a').click()
driver.find_element('xpath','//*[@id="js-nav-menu"]/li[6]/ul/li[1]/ul/li[1]/a').click()
time.sleep(2)
driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[1]/div/div/div/div/div[1]/div[1]/div[4]/div/div/input').clear()
time.sleep(1.7)

#função inicial para gerenciar entre pastas
def gerenciando_canhoto(canhoto,status_canhoto):
    with open(f'log/log[{data}].txt','a') as log:
        log.write(f"\n{canhoto}: {status_canhoto}")
        
    if status_canhoto == 'Nenhum registro encontrado':
        print(f"## Canhoto [{canhoto}] com o status: {status_canhoto.upper()} ##")
        print("Movendo para pasta 'NÃO ENCONTRADOS'")
        arquivo_origem = os.path.join(f'{CAMINHO}CANHOTOS/',f'{canhoto}.png')
        arquivo_destino = os.path.join(f'{CAMINHO}CANHOTOS_NAO ENCONTRADOS/',f'{canhoto}.png')
        os.rename(arquivo_origem, arquivo_destino)
        print(f"~~ Canhoto movido para: {arquivo_destino} ~~")     
    else:
        print(f"## Canhoto [{canhoto}] com o status: {status_canhoto.upper()} ##")
        arquivo_origem = os.path.join(f'{CAMINHO}CANHOTOS/',f'{canhoto}.png')
        arquivo_destino = os.path.join(f'{CAMINHO}CANHOTOS_{status_canhoto.upper()}/',f'{canhoto}.png')
        os.rename(arquivo_origem, arquivo_destino)
        print(f"~~ Canhoto movido para: {arquivo_destino} ~~")     
#função para verificar caso nao apareca mensagem na tela principal            
def verificando_afundo(valor):
    print("! Só mais um momentos, verificando...")
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[1]/div/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/button').click()
    time.sleep(2)
    driver.find_element('xpath','/html/body/div[2]/div/div/main/div[21]/div/div/div[2]/form/div[2]/div/div/input').clear()
    driver.find_element('xpath','/html/body/div[2]/div/div/main/div[21]/div/div/div[2]/form/div[2]/div/div/input').send_keys(valor)
    driver.find_element('xpath','/html/body/div[2]/div/div/main/div[21]/div/div/div[2]/div[1]/div/button').click()
    time.sleep(2)
    try:
        resultado = driver.find_element('xpath','/html/body/div[2]/div/div/main/div[21]/div/div/div[2]/div[3]/div[1]/div/div/table/tbody/tr/td[6]/span').text    
    except Exception:
        resultado = driver.find_element('xpath','/html/body/div[2]/div/div/main/div[21]/div/div/div[2]/div[3]/div[1]/div/div/table/tbody/tr/td').text    
    
    driver.find_element('xpath','/html/body/div[2]/div/div/main/div[21]/div/div/div[1]/button').click()
    time.sleep(2)
    return resultado
        
def findCanhoto(canhoto):
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div/input').clear()
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[1]/div/div/div/div/div[1]/div[1]/div[2]/div/div/input').clear()
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div/input').send_keys(canhoto)
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[1]/div/div/div/div/div[3]/button[4]').click()
    time.sleep(3)

    try:
        status = driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div/table/tbody/tr/td[8]').text
    except Exception:
        status = driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div/table/tbody/tr').text 
    
    if status == 'Nenhum registro encontrado':
        result = verificando_afundo(canhoto)
        gerenciando_canhoto(canhoto,result)            
    elif status == 'Digitalizado' or 'Ag. Aprovação' or 'Pendente' or 'Recebido Físicamente' or 'Rejeitado':
        gerenciando_canhoto(canhoto, status)
            
inicio = time.time()
for item in lista_canhotos:
    try:
        print('\n==========================================')
        print(f'Pesquisando canhoto: [{item}]')
        findCanhoto(item)
        print('==========================================')
    except BaseException as error:
        print(error)             
final = time.time()
contagem = final-inicio
minutos = round(contagem / 60)
print("[] -- FIM DA EXECUÇÃO -- []\n")  
print(f"O programa levou {minutos} minutos para concluir toda a operação...\n")
