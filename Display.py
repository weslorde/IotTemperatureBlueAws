# Funções baixadas
import time
import esp32
from machine import Pin, lightsleep, TouchPad
from nextion import nextion # Responsavel pela comunicação com a tela

display = nextion(17, 16, 9600)

global Estado
global AlarmTimer
global AlarmGraus
global TempAlvo
global GrausAlarme
global TimerAlarme
global atualPag
TempAlvo = 0
GrausAlarme = []
TimerAlarme = []
atualPag = 0

t = TouchPad(Pin(4))
t.config(300)             # configure the threshold at which the pin is considered touched
esp32.wake_on_touch(True)
display.sleep(0)
display.cmd("page 0")
#display.cmd("sendme")
#display.cmd("bkcmd=3") #bkcmd = 3 is Always, returns 0x00 to 0x23 result of serial command.

def DisplayController(): #Solicita resposta do nextion e retorna resposta ja filtrada
    
    global TempAlvo
    global GrausAlarme
    global TimerAlarme
    global atualPag

    Resp = str(display.read()) #Le resposta do nextion
    if Resp.find("^") != -1:
        MensagemList = Resp.split("^")[1].split(" ")
        print(MensagemList)
        
        Comando = MensagemList[0]
        if Comando == "Go":
            display.cmd("page "+MensagemList[1])
        elif Comando == "Desligar":
            display.sleep(1)
            lightsleep()
            display.sleep(0)
            time.sleep(0.6) #Timer para aguardar o display religar
            display.cmd("page 0")
        elif Comando == "TempAlvo":
            TempAlvo = int(MensagemList[1])
        elif Comando == "GrausAlarme":
            GrausAlarme.append([MensagemList[2],int(MensagemList[1])])
            print(GrausAlarme)
        elif Comando == "TimerAlarme":
            TimerAlarme.append([MensagemList[1],MensagemList[2],time.ticks_ms()])
            print(TimerAlarme)
            
        elif Comando == "ListaPass":
            if MensagemList[1] == "nextPag":
                atualPag += 1
            elif MensagemList[1] == "backPag":
                atualPag -= 1
            display.cmd("page AlarmeAtivos")
            
                    
        elif Comando == "ListaAlarme":
            numPags = 0          
            m = atualPag*3
            
            pagTA = (len(TimerAlarme)-1) // 3
            pagGA = (len(GrausAlarme)-1) // 3
            print('pagTA: ',pagTA)
            if pagTA > 0 or pagGA > 0:
                if pagTA > pagGA: numPags = pagTA
                else: numPags = pagGA
                display.cmd(f'nPag.val={atualPag+1}',0)
                if atualPag > 0:
                    display.cmd("left.pic=26",0)
                    display.cmd("left.pic2=26",0)
                else:
                    display.cmd("left.pic=25",0)
                    display.cmd("left.pic2=25",0)

                if atualPag < numPags:
                    display.cmd("rigth.pic=28",0)
                    display.cmd("rigth.pic2=28",0)
                else:
                    display.cmd("rigth.pic=27",0)
                    display.cmd("rigth.pic2=27",0)
                
                
                display.cmd("vis left,1",0)
                display.cmd("vis nPag,1",0)
                display.cmd("vis rigth,1",0)
                 
                 

            for item in [["x",TimerAlarme],["y",GrausAlarme]]:
                for n in range(3):
                    print(item[0],n)
                    if n+m < len(item[1]):
                        if item[0]=="x":
                            display.cmd(f'{item[0]}{n}Valor.txt="{item[1][n+m][0]}h{item[1][n+m][1]}m"',0)
                        else:
                            display.cmd(f'{item[0]}{n}Tipo.txt="{item[1][n+m][0]}:"',0)
                            display.cmd(f'{item[0]}{n}Valor.txt="{item[1][n+m][1]}"',0)
                            display.cmd(f'{item[0]}{n}Valor.txt+=Graus.txt') #Simbolo de Graus está chegando errado, logo usando variavel com o simbolo já escrita no display 
                        display.cmd(f'vis {item[0]}{n},1',0)
                        display.cmd(f'vis {item[0]}{n}Tipo,1',0)
                        display.cmd(f'vis {item[0]}{n}Valor,1',0)
                        display.cmd(f'vis {item[0]}{n}Del,1',0)
        
        if Comando == "DeleteAlarme":
            m = atualPag*3
            if MensagemList[1] == 'y':
                GrausAlarme.pop(int(MensagemList[2])+m)
            elif MensagemList[1] == 'x':
                TimerAlarme.pop(int(MensagemList[2])+m)
            display.cmd("page AlarmeAtivos")    
            
        
                    
def QualPag():
    print(str(display.cmd("sendme")))


        
            
