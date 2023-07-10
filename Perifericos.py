from machine import Pin, PWM
from max6675 import MAX6675
import time

#--------------------Temperatura-----------------------------------

T1 = MAX6675(sck_pin=18, cs_pin=19, so_pin=21) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K
T2 = MAX6675(sck_pin=14, cs_pin=27, so_pin=26) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K
T3 = MAX6675(sck_pin=25, cs_pin=33, so_pin=32) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K

global TGrelha
global TSensor1
global TSensor2
global TempAlvo
TGrelha = 0
TSensor1 = 0
TSensor2 = 0
TempAlvo = 0

global funCriaPID

def funCriaPID(fun):
    global funCriaPID
    funCriaPID = fun

def DefineAlvo(TA):
    global TempAlvo
    TempAlvo = TA
    funCriaPID(TempAlvo)
    
    
def MediaTemps():
    global TGrelha
    global TSensor1
    global TSensor2
    
    SumT1 = T1.read()
    SumT2 = T2.read()
    SumT3 = T3.read()
    
    for x in range(9):
        SumT1 += T1.read()
        SumT2 += T2.read()
        SumT3 += T3.read()
    
    TGrelha = int(SumT1/10)
    TSensor1 = int(SumT2/10)
    TSensor2 = int(SumT3/10)
    
    
def GetTemps():
    MediaTemps()
    return(TGrelha, TSensor1, TSensor2, TempAlvo)




#----------------------Entradas e Comandos -----------------------

fimUp = Pin(34, Pin.IN) #Fim de curso SUPERIOR ligado ao pino 34
fimDown = Pin(35, Pin.IN) #Fim de curso INFERIOR ligado ao pino 35


global Entradas
global EntradasAnterior
global EntradasFiltradas
global EntradasContador

Entradas = [fimUp, fimDown]
EntradasFiltradas = [False, False, False, False]
EntradasContador = [0,0]
EntradasAnterior = [1,1]


def FiltraEntradas():
    global Entradas
    global EntradasAnterior
    global EntradasFiltradas
    global EntradasContador
    ValorEntradas = [0,0,0,0]
    NumFiltro = 6
    
    for x in range(2):
        ValorEntradas[x] = Entradas[x].value()
        
        if ValorEntradas[x] == EntradasAnterior[x]:
            EntradasContador[x] += 1
        else:
            EntradasContador[x] = 0
            EntradasAnterior[x] = ValorEntradas[x]
        
        if EntradasContador[x] > NumFiltro and (EntradasFiltradas[x] == ValorEntradas[x]):
            EntradasFiltradas[x] = not(ValorEntradas[x])
            print(EntradasFiltradas)
            
def DispDefUpDown(direcao, valor):
    global EntradasFiltradas
    if direcao == "Up": EntradasFiltradas[2] = valor
    elif direcao == "Down": EntradasFiltradas[3] = valor
    
def getEntradasFiltradas():
    global EntradasFiltradas
    return EntradasFiltradas
#--------------------------Controle Motor-----------------------------------------
            
pwmUp = PWM(Pin(23, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 23 responsavel por SUBIR o motor. É iniciado com duty de Zero para nao ativar o motor
pwmDown = PWM(Pin(22, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 22 responsavel por DESCER o motor. É iniciado com duty de Zero para nao ativar o motor
pwmUp.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
pwmDown.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
global TempoMotorFinal
global TempoMotor
TempoMotorFinal = 0
TempoMotor = 0
             
def MovMotor(Dir="Stop", Vel=0, Temp=0):
    global EntradasFiltradas
    global TempoMotorFinal
    global TempoMotor
    FfimUp, FfimDown, BlueUp, BlueDown = EntradasFiltradas
    
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
            

    
def MotorLogic():
    global TempoMotorFinal
    global TempoMotor
    global EntradasFiltradas
    
    FfimUp, FfimDown, BlueUp, BlueDown = EntradasFiltradas
    
    if pwmUp.duty() > 0 and FfimUp:
        MovMotor("StopUp")
    elif pwmDown.duty() > 0 and FfimDown:
        MovMotor("StopDown")
    elif BlueUp:
        MovMotor("Up", 1000)
        Modo = "Manual"
    elif BlueDown:
        MovMotor("Down", 1000)
        Modo = "Manual"
    elif TempoMotorFinal != 0: pass
    else: MovMotor("Stop")
    
   #print(TempoMotorFinal)
    if time.ticks_diff(time.ticks_ms(),TempoMotor) > TempoMotorFinal and TempoMotorFinal != 0: #dsfgswdg
        MovMotor("Stop")
        TempoMotorFinal=0
        
        

#----------------------------------------------Alarme ---------------------------------------------------------------------
        
global GrausAlarme
global TimerAlarme
GrausAlarme = []
TimerAlarme = []

def appendAlarm(Comando, Info):
    global GrausAlarme
    global TimerAlarme
    if Comando == "GrausAlarme":
        GrausAlarme.append(Info) # [['Grelha', 5], ['Sensor1', 15], ['Sensor2', 115]]['Sensor1', 15]
    elif Comando == "TimerAlarme":
        TimerAlarme.append(Info) # [['01', '11', 1757430], ['02', '22', 1763257]]
    
def getAlarm():
    global GrausAlarme
    global TimerAlarme
    return (TimerAlarme, GrausAlarme)

def delAlarm(pag, item, indice):
    global GrausAlarme
    global TimerAlarme
    m = pag*3
    if item == 'y' or item == "graus":
        GrausAlarme.pop(int(indice)+m)
    elif item == 'x' or item == "timer":
        TimerAlarme.pop(int(indice)+m)

global enviaBlue
def passFunBlue(fun):
    global enviaBlue
    enviaBlue = fun

def checaAlarmes():
    global GrausAlarme
    global TimerAlarme
    global TGrelha
    global TSensor1
    global TSensor2
    global TempAlvo
    global enviaBlue
    x = 0
    
    for item in TimerAlarme:
        #print(item)
        diffTime = time.ticks_diff(time.ticks_ms(),item[2])
        
        minutos = str( (diffTime // 1000 // 60) % 60 )
        horas = str( (diffTime // 1000 // 3600) % 24 )
        
        #print(minutos)
        #print(horas)
        #print(f"test 1: {horas == item[0]}, test 2: {minutos >= item[1]}")
        
        if (horas == item[0] and minutos >= item[1]):
            enviaBlue(f"NotT,{horas},{minutos}")
            delAlarm(0, "timer", x)
        x += 1
    
    listTemps = {"Grelha": TGrelha, "Sensor1": TSensor1, "Sensor2": TSensor2}
    x=0 
    for item in GrausAlarme:
        sensor = item[0]
        tempAviso = item[1]
        if ( (listTemps[sensor] <= tempAviso + 5) and (listTemps[sensor] >= tempAviso - 5) ):
            enviaBlue(f"NotG,{sensor},{tempAviso}")
            delAlarm(0, "graus", x)   
    x += 1
        
        
        
        
        
        
    
    
    
    
    
    
    
    