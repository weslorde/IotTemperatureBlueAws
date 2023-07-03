import time

import bluetooth
from BLE import BLEUART

import Perifericos
import DisplayController as Disp

class FlutterBlue:
    global TBlue
    TBlue = 0

    def on_rx(self):
        global Modo
        global EntradasFiltradas
        global TBlue
                
        msgRecebida = self.uart.read().decode()
        msgRecebida = msgRecebida.split("\x00") #Remove codigo de final da string
        msgRecebida = msgRecebida[0].split(",")
        #print(msgRecebida[0])
        #msgRecebida = ExtASCII.myASCIIextToString( msgCodificada )  
        
        print(msgRecebida)
        
        if(msgRecebida[0] == "Ping"):
            TGrelha, TSensor1, TSensor2, TempAlvo = Perifericos.GetTemps()
            self.uart.write("Temp," + str(int(TGrelha)) + "," + str(int(TSensor1)) + "," + str(int(TSensor2)) + "," + str(int(TempAlvo))) 
            
        elif(msgRecebida[0] == "Alarme"):
            
            TimerAlarme, GrausAlarme = Perifericos.getAlarm()
            print(TimerAlarme)
                
            for x in range(len(TimerAlarme)):
                self.uart.write(f"AlarmT,{x},{TimerAlarme[x][0]},{TimerAlarme[x][1]}")

            for x in range(len(GrausAlarme)):
                self.uart.write(f"AlarmG,{x},{GrausAlarme[x][0]},{GrausAlarme[x][1]}")
                
                
        elif(msgRecebida[0] == "DelAlarme"):
            Perifericos.delAlarm(0, msgRecebida[1], msgRecebida[2])
            Disp.MonitoraDisplay("^Go AlarmeAtivos^")
            
            
        elif(msgRecebida[0] == "Target"):
            Perifericos.DefineAlvo(int(msgRecebida[1]))
            
        
        elif(msgRecebida[0] == "Motor"):
            Perifericos.DefineAlvo(0)
            if msgRecebida[2] == "Press":
                Perifericos.DispDefUpDown(msgRecebida[1], 1)
            elif msgRecebida[2] == "Release":
                Perifericos.DispDefUpDown(msgRecebida[1], 0)
                
    
            
            
        else: print("Mensagem nao conhecida:", msgRecebida)
        
    #------------ FIM Rotina Blue ---------------------------
        
    #------------ Cria OBJ Blue -----------------------------
    def __init__(self):
        name = "ChurrasTech"  #"78:E3:6D:17:1A:4E"
        ble = bluetooth.BLE() 
        self.uart = BLEUART(ble, name)
        self.uart.irq(handler = self.on_rx)
        print("Iniciou Blue")

#------------ FIM Cria OBJ Blue ---------------------------


def blueLoop():
    x = 0
    teste = FlutterBlue()

    while(1):
        x = x+10
        time.sleep(1)
        print(x)

if __name__ == "__main__":
    blueLoop()
    