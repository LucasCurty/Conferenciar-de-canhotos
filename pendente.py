from selenium import webdriver
from acessos import LOGIN,SENHA,URL,CAMINHO, CAMINHO_ENV
from pastas import create_folders, gerar_pendentes
import time
import pyautogui
from datetime import date
import os

#renomeando canhotos
lista_canhotos = gerar_pendentes()

#----------iniciando aplicação
print("INICIANDO AUTOMAÇÃO !\n")
print("CONFERINDO PASTAS...\n")
create_folders() # verificando pastas
print("[   Pastas Verificadas    ]")

#Configuração do Selenium
driver = webdriver.Chrome()
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

#função para enviar o canhoto pendente
def se_pendente(valor): 
    driver.execute_script("window.scrollBy(0,300);")
    time.sleep(2)
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div/table/tbody/tr/td[14]/div/button').click()
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div/table/tbody/tr/td[14]/div/div/a[4]').click()
    time.sleep(3)
    pyautogui.typewrite(f'{CAMINHO_ENV}\{valor}.png')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(3)
            
#função inicial para gerenciar entre pastas
data = date.today().strftime("%d-%m-%Y")
def gerenciando_canhoto(canhoto,status_canhoto):
    with open(f'log/log[{data}].txt','a') as log:
        log.write(f"\n{canhoto}: {status_canhoto}")
    arquivo_origem = os.path.join(f'{CAMINHO}CANHOTOS_PENDENTE/',f'{canhoto}.png')  
     
    if status_canhoto == 'Pendente':
        print(f"Enviando o canhoto: {canhoto}...")
        se_pendente(canhoto)
        arquivo_destino = os.path.join(f'{CAMINHO}CANHOTOS_AG. APROVAÇÃO/',f'{canhoto}.png')
        os.rename(arquivo_origem, arquivo_destino)
        print(f"==== Canhoto movido para: {arquivo_destino}")
        
    elif status_canhoto == 'Nenhum registro encontrado':
        print("CAIIU NO NAO ENCONTRADO")
        arquivo_destino = os.path.join(f'{CAMINHO}CANHOTOS_NAO ENCONTRADOS/',f'{canhoto}.png')
        os.rename(arquivo_origem, arquivo_destino)
        print(f"==== Canhoto movido para: {arquivo_destino}")
    else:
        print(f"==== O canhoto {canhoto} está com o status: {status_canhoto.upper()}")
        arquivo_origem = os.path.join(f'{CAMINHO}CANHOTOS_PENDENTE/',f'{canhoto}.png')
        arquivo_destino = os.path.join(f'{CAMINHO}CANHOTOS_{status_canhoto.upper()}/',f'{canhoto}.png')
        os.rename(arquivo_origem, arquivo_destino)
        print(f"==== Canhoto movido para: {arquivo_destino}")
             
def findCanhoto(canhoto):
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div/input').clear()
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[1]/div/div/div/div/div[1]/div[1]/div[2]/div/div/input').clear()
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div/input').send_keys(canhoto)
    driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[1]/div/div/div/div/div[3]/button[4]').click()
    time.sleep(2)
    try:
        status = driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div/table/tbody/tr/td[8]').text
    except Exception:
        status = driver.find_element('xpath','/html/body/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div/table/tbody/tr').text 
    
    if status == 'Nenhum registro encontrado':
        gerenciando_canhoto(canhoto, status_canhoto="Nenhum registro encontrado")
    elif status == 'Digitalizado' or 'Ag. Aprovação' or 'Pendente' or 'Recebido Físicamente' or 'Rejeitado':
        gerenciando_canhoto(canhoto,status)
    
        

inicio = time.time()           
for item in lista_canhotos:
    try:
        print('==========================================\n')
        print(f'Pesquisando canhoto: [{item}]')
        findCanhoto(item)
        print('\n==========================================\n')
    except BaseException as error:
        print(error)
fim = time.time()
contagem = fim-inicio             
print(f" FIM DA EXECUÇÃO Tempo Estimado foi de: {print(f"{round(contagem)}")}") 