import os
from acessos import CAMINHO

#Conferindo pastas, se nao existe o sistema cria.
def create_folders():
    pastas = [
        f'{CAMINHO}CANHOTOS_DIGITALIZADO',
        f'{CAMINHO}CANHOTOS_AG. APROVAÇÃO',
        f'{CAMINHO}CANHOTOS_NAO ENCONTRADOS',
        f'{CAMINHO}CANHOTOS_PENDENTE',
        f'{CAMINHO}CANHOTOS_RECEBIDO FÍSICAMENTE',
        f'{CAMINHO}CANHOTOS_REJEITADO',
    ]

    for i in pastas:
        if os.path.exists(i) == False:
            os.mkdir(i)
            print("====Pasta criada com sucesso! ", i)

def rename_arquivos():
    try:
        folder = os.listdir(f'{CAMINHO}CANHOTOS')
        folder_canhotos = []
        for i in folder:
            canhoto = i.split('.')
            canhoto.pop()
            novo_canhoto = canhoto[0]
            os.rename(f'{CAMINHO}CANHOTOS/{i}',f'{CAMINHO}CANHOTOS/{novo_canhoto}.png')
            folder_canhotos.append(novo_canhoto)      
    except Exception as error:
        print(error)        
    return folder_canhotos
    
def gerar_pendentes():
    try:
        pasta = os.listdir(f'{CAMINHO}CANHOTOS_PENDENTE')
        apenas_numero = []
        for i in pasta:
            canhoto = i.split('.')
            canhoto.pop()
            novo_canhoto = canhoto[0]
            os.rename(f'{CAMINHO}CANHOTOS_PENDENTE/{i}',f'{CAMINHO}CANHOTOS_PENDENTE/{novo_canhoto}.png')
            apenas_numero.append(novo_canhoto)      
    except Exception as error:
        print(error)        
    return apenas_numero
