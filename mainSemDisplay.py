from machine import Pin, PWM
import time

import bluetooth
from BLE import BLEUART
from max6675 import MAX6675
from PID import PID

#------------ Rotina Blue ---------------------------

fimUp = Pin(02, Pin.IN) #Fim de curso SUPERIOR ligado ao pino 34
fimDown = Pin(15, Pin.IN) #Fim de curso INFERIOR ligado ao pino 35
BtnUp = Pin(19, Pin.IN) #Fim de curso SUPERIOR ligado ao pino 34
BtnDown = Pin(21, Pin.IN) #Fim de curso INFERIOR ligado ao pino 35

pwmUp = PWM(Pin(23, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 23 responsavel por SUBIR o motor. É iniciado com duty de Zero para nao ativar o motor
pwmDown = PWM(Pin(22, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 22 responsavel por DESCER o motor. É iniciado com duty de Zero para nao ativar o motor
pwmUp.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
pwmDown.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
#T3 = MAX6675(sck_pin=34, cs_pin=35, so_pin=32) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K
T1 = MAX6675(sck_pin=27, cs_pin=14, so_pin=12) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K
T2 = MAX6675(sck_pin=33, cs_pin=25, so_pin=26) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K

global TempAlvo
global Temp1
global Temp2
global Modo
global Entradas
global EntradasAnterior
global EntradasFiltradas
global EntradasContador
global TempoMotorFinal
global TempoMotor

TempAlvo = 0
Temp1 = 0
Temp2 = 0
Modo = "Manual"
Aciona = "Espera"
Entradas = [BtnUp, BtnDown, fimUp, fimDown]
EntradasFiltradas = [False, False, False, False, False, False]
EntradasContador = [0,0,0,0]
EntradasAnterior = [1,1,1,1]

TempoMotor = 0
TempoMotorFinal = 0

global TBlue
TBlue = 0

def on_rx():
    global TempAlvo
    global Temp1
    global Temp2
    global Modo
    global EntradasFiltradas
    global TBlue
    
    msgRecebida = uart.read().decode()
    msgRecebida = msgRecebida.split("\x00") #Remove codigo de final da string
    msgRecebida = msgRecebida[0].split(",")
    print(msgRecebida[0])
    #msgRecebida = ExtASCII.myASCIIextToString( msgCodificada )  
    
    #print(msgRecebida)
    
    if(msgRecebida[0] == "Ping"):
        time.sleep(1)
        uart.write("Temp," + str(int(Temp1)) + "," + str(int(Temp2)) + "," + str(int(TempAlvo)))
        
    elif(msgRecebida[0] == "Up"):
        EntradasFiltradas[4] = True
        
    elif(msgRecebida[0] == "Down"):
        EntradasFiltradas[5] = True
        
    elif(msgRecebida[0] == "End"):
        EntradasFiltradas[4] = False
        EntradasFiltradas[5] = False
        uart.write("End," + str(int(Temp1)) + "," + str(int(Temp2)) + "," + str(int(TempAlvo)))
        #uart.write("End,22,33,50")
        
    elif(msgRecebida[0] == "Num"):
        print(msgRecebida[1])
        TempAlvo = int(msgRecebida[1])
        #TBlue = int(msgRecebida[1])   #TesteCel
        uart.write("Temp," + str(int(Temp1)) + "," + str(int(Temp2)) + "," + str(int(TempAlvo)))
    
    elif(msgRecebida[0] == "Modo"):
        Modo = msgRecebida[1]
        print(Modo)
        
        
    else: print("Mensagem nao conhecida:", msgRecebida)
    
#------------ FIM Rotina Blue ---------------------------
    
#------------ Cria OBJ Blue -----------------------------

name = "ChurrasTech"  #"78:E3:6D:17:1A:4E"
ble = bluetooth.BLE() 
uart = BLEUART(ble, name)
uart.irq(handler = on_rx)
print("Iniciou Blue")

#------------ FIM Cria OBJ Blue ---------------------------

#------------ Fun Envia Temp ------------------------------

def EnviaTemp(Temp1,Temp2,TempAlvo):
    uart.write("Temp," + str(int(Temp1)) + "," + str(int(Temp2)) + "," + str(int(TempAlvo)))
     
#------------ FIM Fun Envia Temp ----------------------------
    
def FiltroEntradas():
    global Entradas
    global EntradasAnterior
    global EntradasFiltradas
    global EntradasContador
    ValorEntradas = [0,0,0,0]
    NumFiltro = 6
    
    for x in range(4):
        ValorEntradas[x] = Entradas[x].value()
        
        if ValorEntradas[x] == EntradasAnterior[x]:
            EntradasContador[x] += 1
        else:
            EntradasContador[x] = 0
            EntradasAnterior[x] = ValorEntradas[x]
        
        if EntradasContador[x] > NumFiltro and (EntradasFiltradas[x] == ValorEntradas[x]):
            EntradasFiltradas[x] = not(ValorEntradas[x])
            print(EntradasFiltradas)
            
    
def MovMotor(Dir="Stop", Vel=0, Temp=0):
    global EntradasFiltradas
    global TempoMotorFinal
    global TempoMotor
    FBtnUp, FBtnDown, FfimUp, FfimDown, BlueUp, BlueDown = EntradasFiltradas
    
    if Dir == "Up" and not(FfimUp):
        pwmDown.init(freq=5000, duty=0) #Zera Down
        pwmUp.init(freq=5000, duty=Vel) #Aciona Up
    elif Dir == "Down" and not(FfimDown):
        pwmUp.init(freq=5000, duty=0) #Zera Up
        pwmDown.init(freq=5000, duty=Vel) #Aciona Down
    elif Dir == "StopUp":
        pwmUp.init(freq=5000, duty=0) #Zera Up
    elif Dir == "StopDown":
        pwmDown.init(freq=5000, duty=0) #Zera Down
    elif Dir == "Stop":
        pwmDown.init(freq=5000, duty=0) #Zera Down
        pwmUp.init(freq=5000, duty=0) #Zera Up
        
    if Temp > 0:
        TempoMotorFinal = Temp*1000
        TempoMotor = time.ticks_ms()
    

timeTemp = time.ticks_ms() # Zera contador de tempo
timeAuto = time.ticks_ms() # Zera contador de tempo
AutoTemps = [1,[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
DifTemps1 = [0,0,0,0,0,0,0,0,0,0]
DifTemps2 = [0,0,0,0,0,0,0,0,0,0]
DeltaTemps = [0,0,0,0,0,0,0,0,0]

while(True):
    
    #--------Monitorar Temperatura-------------------------
    timeAtual = time.ticks_ms()

    if time.ticks_diff(timeAtual,timeTemp) > 4000: #Realiza medida e envia a cada 4seg
        Temp1 = T1.read()
        Temp2 = T2.read()
        print("T1: ", Temp1)
        print("T2: ", Temp2)
        print(TempAlvo)
        EnviaTemp(Temp1,Temp2,TempAlvo)
        timeTemp = time.ticks_ms() # Zera contador de tempo
    #--------Fim Monitorar Temperatura-------------------------
        
    #---------Filtro entradas ----------------------------
    FiltroEntradas()
    #---------Filtro entradas ----------------------------   
        
    #--------Checa entredas---------------------------
    FBtnUp, FBtnDown, FfimUp, FfimDown, BlueUp, BlueDown = EntradasFiltradas
    
    if pwmUp.duty() > 0 and FfimUp:
        MovMotor("StopUp")
    elif pwmDown.duty() > 0 and FfimDown:
        MovMotor("StopDown")
    elif FBtnUp or BlueUp:
        MovMotor("Up", 600)
        Modo = "Manual"
    elif FBtnDown or BlueDown:
        MovMotor("Down", 600)
        Modo = "Manual"
    elif TempoMotorFinal != 0: pass
    else: MovMotor("Stop")
    
    if time.ticks_diff(timeAtual,TempoMotor) > TempoMotorFinal and TempoMotorFinal != 0: #dsfgswdg
        MovMotor("Stop")
        TempoMotorFinal=0
    
    #--------FIM Checa entredas---------------------------
    
    #---------Rotina Modo Auto----------------------------
    if time.ticks_diff(timeAtual,timeAuto) > 1/20*60000: # A cada 1 minuto
        if AutoTemps[0] > 10: AutoTemps[0] = 1
        AutoTemps[AutoTemps[0]] = [T1.read(),T2.read()]
        #AutoTemps[AutoTemps[0]] = [TBlue,TBlue]  #Teste com o blue
        AutoTemps[0] += 1
        timeAuto = time.ticks_ms() # Zera contador de tempo
        print(AutoTemps)
        
        if AutoTemps[0] == 11:
            DifTemps1[0] = AutoTemps[1][0] - TempAlvo
            DifTemps2[0] = AutoTemps[1][1] - TempAlvo
            for x in range(9):
                DifTemps1[x+1] = AutoTemps[x+2][0] - TempAlvo
                DifTemps2[x+1] = AutoTemps[x+2][1] - TempAlvo
                DeltaTemps[x] =  AutoTemps[x+2][0] - AutoTemps[x+1][0]
            print(DifTemps1)
            print(DeltaTemps)
            somaDelta=0
            for x in range(9):
                somaDelta += DeltaTemps[x] 
            print(somaDelta)
            Aciona = "Espera"
            if somaDelta < 20 and somaDelta > -1 :
                Aciona = "Ok"
            elif somaDelta > -20 and somaDelta < 1 :
                Aciona = "Ok"
            else: Aciona = "Espera"
            
            Tempo = (DifTemps1[9] + DifTemps2[9])/2
            Tempo = Tempo/10
            
            if Aciona == "Ok" and (Tempo > 1 or Tempo < -1):
                if Tempo < 0:
                    Tempo = Tempo*(-1/2)
                    Aciona = "Down"
                elif Tempo > 0:
                    Tempo = Tempo/2
                    Aciona = "Up"
                print("Tempo:", Tempo, " Aciona:", Aciona)
                
                
    if Modo == "Auto":
        if Aciona == "Up":
            MovMotor("Up",600,Tempo)
        elif Aciona == "Down":
            MovMotor("Down",600,Tempo)
        Aciona = "Espera"
            
    
       
        
    
        



