import network
import time


sta_if = network.WLAN(network.STA_IF) #Cria objeto para WiFi
sta_if.active(True) #Liga Wifi

 
def WifiConectar(): #Realiza e testa conexao
    Pref = CarregarInfo()
    if not sta_if.isconnected():
        print('Conectando...')
        sta_if.connect(Pref["Login"], Pref["Senha"])
        count=0
        while not sta_if.isconnected():
            pass
    print('Config da rede:', sta_if.ifconfig())
    
    
def WifiStatus(): #Retorna Verdadeiro se estiver conectado 
    return sta_if.isconnected()
    
def WifiReinicia(Rede,Senha): #Reinicia conexao
    sta_if.disconnect()
    time.sleep(1)
    WifiConectar()
    
    
import os

def CarregarInfo(): #Carrega txt com informacoes salvas
    try:
        Arquivo = open('Pref.txt','r')   #Tenta abrir Pref.txt
        
    except:
        return({"Login":'Motta', "Senha":'wes56145233', "NumSerie":12131415})   #Se NAO existe retorna um dicionario vazio
    
    Pref = Arquivo.read()       #Passa as informacoes do txt para a variavel "Pref"
    Arquivo.close()             #Fecha o arquivo .txt 
    return eval (Pref)          #Retorna variavel

def Salvar(Pref):        #Salva conteudo da variavel Pref em um arquivo .txt
    print("Salvando")
    Info = open('Pref.txt','w')      
    Info.write(str(Pref))                          
    Info.close
    
    
    


