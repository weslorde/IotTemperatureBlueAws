import time

from machine import WDT
import bluetooth
from BLE import BLEUART

import _thread

import DisplayController as Disp
import TestFlutterBlue
import Perifericos
import AlexaAWS

import wifi
from PID import PID

timeTemp = time.ticks_ms() # Zera contador de tempo
timeAuto = time.ticks_ms() # Zera contador de tempo
AutoTemps = [1,[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
DifTemps1 = [0,0,0,0,0,0,0,0,0,0]
DifTemps2 = [0,0,0,0,0,0,0,0,0,0]
DeltaTemps = [0,0,0,0,0,0,0,0,0]

wdt = WDT(timeout=15000)  # enable it with a timeout of 10s
wdt.feed()

Pref = wifi.CarregarInfo()
wifi.Salvar(Pref)
tipoConect = Pref["Modo"]
if tipoConect == "Bluetooth":
    BlueEsp = TestFlutterBlue.FlutterBlue()
    Perifericos.passFunBlue(BlueEsp.enviaBlue)
elif tipoConect == "AWS":
    IotAWS = AlexaAWS.AWS()
    
#teste = _thread.start_new_thread(AlexaAWS.AWSLoop, ())

#time.sleep(15)

#teste2 = _thread.start_new_thread(TestFlutterBlue.blueLoop, ())

def criaPID(Talvo):
    global controleCount
    global pid
    
    controleCount = 0
    pid = PID(0, 0.002, -0.0001, setpoint=Talvo)
    pid.output_limits = (-2, 2) 
    
def controleTemp():
    global controleCount
    global pid
    Temps = Perifericos.GetTemps()
    TGrelha = Temps[0]
    TAlvo = Temps[3]
    
    if TAlvo > 30:    
        respPID = pid(TGrelha)
        print("Temp:", TGrelha, "PID:",respPID)
        controleCount += 1
        if controleCount == 10:
            controleCount = 0
            print("test")
            
            if respPID > 0.3:
                print("move motor Down ", str(respPID), " segundos")
                Perifericos.MovMotor(Dir="Down", Vel=600, Temp=int(respPID))
                criaPID(TAlvo)
         
            elif pid(TGrelha) < -0.3:
                print("move motor UP", str(respPID), " segundos")
                Perifericos.MovMotor(Dir="Up", Vel=600, Temp=int(respPID)*-1)
                criaPID(TAlvo)
                
    #Caso nao atender o 0.3 em 1 ciclo de teste so mover um valor minimo fixo (fazer!)
    


#timeAtual = time.ticks_ms()
global controleCount
controleCount = 0
criaPID(0)
Perifericos.funCriaPID(criaPID)
errAws=0
while(True):
      
    #--------Monitorar Temperatura-------------------------
    timeAtual = time.ticks_ms()
    
    if time.ticks_diff(timeAtual,timeTemp) > 5010: #ZeraTimer apos 10 seg
        #print(Perifericos.GetTemps()) 
        timeTemp = time.ticks_ms()-2 # Zera contador de tempo e retira um tempo para nao zerar as comparacoes
        
    #--------Fim Monitorar Temperatura-------------------------
    if time.ticks_diff(timeAtual,timeTemp)%1000 == 0: wdt.feed()
    if time.ticks_diff(timeAtual,timeTemp)%200 == 0: Disp.MonitoraDisplay()
    if time.ticks_diff(timeAtual,timeTemp)%1000 == 0:  Disp.QualPag()
    
    if time.ticks_diff(timeAtual,timeTemp)%50 == 0: Perifericos.MotorLogic()
    if time.ticks_diff(timeAtual,timeTemp)%10 == 0: Perifericos.FiltraEntradas()
    
    if time.ticks_diff(timeAtual,timeTemp)%500 == 0: controleTemp() #Como 1500 so acontece uma vez ate chegar no 2000 e zerar vai funcionar a cada 2000
    
    if time.ticks_diff(timeAtual,timeTemp)%1000 == 0: Perifericos.checaAlarmes()
    
    if tipoConect == "Bluetooth":
        pass
    elif tipoConect == "AWS":
        try:
            if time.ticks_diff(timeAtual,timeTemp)%500 == 0: IotAWS.checaMsg()
            errAws=0
        except:
            errAws+=1
            print("EEEEEERRRRRRRRRRRRRPOOOOOOOOOOo")
            if errAws >= 10:
                while(1):
                    time.sleep(1)
        #if time.ticks_diff(timeAtual,timeTemp)%5000 == 0: IotAWS.attAwsShadow() #Receber pedido pelo aws
    

    
    
    #if time.ticks_diff(timeAtual,timeTemp)%200 == 0: IotAWS.checaMsg()
    #---------Rotina Modo Auto----------------------------
#     
#     if time.ticks_diff(timeAtual,timeAuto) > 1/20*60000: # A cada 1 minuto
#         if AutoTemps[0] > 10: AutoTemps[0] = 1
#         AutoTemps[AutoTemps[0]] = [T1.read(),T2.read()]
#         #AutoTemps[AutoTemps[0]] = [TBlue,TBlue]  #Teste com o blue
#         AutoTemps[0] += 1
#         timeAuto = time.ticks_ms() # Zera contador de tempo
#         print(AutoTemps)
#         
#         if AutoTemps[0] == 11:
#             DifTemps1[0] = AutoTemps[1][0] - TempAlvo
#             DifTemps2[0] = AutoTemps[1][1] - TempAlvo
#             for x in range(9):
#                 DifTemps1[x+1] = AutoTemps[x+2][0] - TempAlvo
#                 DifTemps2[x+1] = AutoTemps[x+2][1] - TempAlvo
#                 DeltaTemps[x] =  AutoTemps[x+2][0] - AutoTemps[x+1][0]
#             print(DifTemps1)
#             print(DeltaTemps)
#             somaDelta=0
#             for x in range(9):
#                 somaDelta += DeltaTemps[x] 
#             print(somaDelta)
#             Aciona = "Espera"
#             if somaDelta < 20 and somaDelta > -1 :
#                 Aciona = "Ok"
#             elif somaDelta > -20 and somaDelta < 1 :
#                 Aciona = "Ok"
#             else: Aciona = "Espera"
#             
#             Tempo = (DifTemps1[9] + DifTemps2[9])/2
#             Tempo = Tempo/10
#             
#             if Aciona == "Ok" and (Tempo > 1 or Tempo < -1):
#                 if Tempo < 0:
#                     Tempo = Tempo*(-1/2)
#                     Aciona = "Down"
#                 elif Tempo > 0:
#                     Tempo = Tempo/2
#                     Aciona = "Up"
#                 print("Tempo:", Tempo, " Aciona:", Aciona)
#                 
#                 
#     if Modo == "Auto":
#         if Aciona == "Up":
#             MovMotor("Up",600,Tempo)
#         elif Aciona == "Down":
#             MovMotor("Down",600,Tempo)
#         Aciona = "Espera"
            
    
       






























    


    
        




