from machine import Pin, PWM
import time
from max6675 import MAX6675
from PID import PID
import bluetooth
from BLE import BLEUART


def on_rx():
    msgRecebida = uart.read().decode()
    msgRecebida = msgRecebida.split("\x00") #Remove codigo de final da string
    msgRecebida = msgRecebida[0].split(",")
    print(msgRecebida[0])
    #msgRecebida = ExtASCII.myASCIIextToString( msgCodificada )  
    
    #print(msgRecebida)
    
    if(msgRecebida[0] == "Ping"):
        time.sleep(1)
        uart.write("Temp,22,33,50")
    elif(msgRecebida[0] == "Up" and fimUp.value()):
        pwmUp.init(freq=5000, duty=600)
    elif(msgRecebida[0] == "Down" and fimDown.value()):
        pwmDown.init(freq=5000, duty=600)
    elif(msgRecebida[0] == "End"):
        pwmUp.init(freq=5000, duty=0)
        pwmDown.init(freq=5000, duty=0)
        uart.write("End,22,33,50")
        
    else: print("Mensagem nao conhecida:", msgRecebida)

name = "ChurrasTech"  #"78:E3:6D:17:1A:4E"
ble = bluetooth.BLE() 
uart = BLEUART(ble, name)
uart.irq(handler = on_rx)
print("Iniciou Blue")

#pwmUp = PWM(Pin(22), freq=5000)
#pwmDown = PWM(Pin(23), freq=5000)

fimUp = Pin(02, Pin.IN) #Fim de curso SUPERIOR ligado ao pino 34
fimDown = Pin(15, Pin.IN) #Fim de curso INFERIOR ligado ao pino 35
BtnUp = Pin(19, Pin.IN) #Fim de curso SUPERIOR ligado ao pino 34
BtnDown = Pin(21, Pin.IN) #Fim de curso INFERIOR ligado ao pino 35

pwmUp = PWM(Pin(22, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 23 responsavel por SUBIR o motor. É iniciado com duty de Zero para nao ativar o motor
pwmDown = PWM(Pin(23, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 22 responsavel por DESCER o motor. É iniciado com duty de Zero para nao ativar o motor
pwmUp.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
pwmDown.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor

#T = MAX6675(sck_pin=33, cs_pin=25, so_pin=26) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K
T2 = MAX6675(sck_pin=27, cs_pin=14, so_pin=12) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K
T1 = MAX6675(sck_pin=33, cs_pin=25, so_pin=26) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K

def MoveMotor(direcao, temp): #Funcao responsavel por mover o motor limitado pelo fim de curso
    t=temp*100 #Recebe tempo em segundos e calcula para entrar no for
    if direcao == "Up" and fimUp.value() == 0:	#Checa a direcao para iniciar o PWM
        pwmUp.init(freq=5000, duty=1000)
    elif direcao == "Down" and fimDown.value() == 0:
        pwmDown.init(freq=5000, duty=1000)
    
    for x in range(t): #Loop para manter o motor funcionando durante o tempo recebido enquanto chega o fim de curso
        time.sleep(0.01)
        if direcao == "Up" and fimUp.value() == 1:
            pwmDown.init(freq=5000, duty=0) # Se ativar fim de curso sai do "for" e para motor
            break
        if direcao == "Down" and fimDown.value() == 1:
            pwmUp.init(freq=5000, duty=0)
            break
    pwmUp.init(freq=5000, duty=0) #Para motor apos o tempo definido
    pwmDown.init(freq=5000, duty=0)


def BtnManual():
    print(BtnUp.value(), BtnDown.value(), fimUp.value(), fimDown.value())
    if BtnUp.value() == 0 or BtnDown.value() == 0:
        start = 0
        while (BtnUp.value() == 0 and fimUp.value() ): 
            time.sleep(0.001)
            if start == 0:
                pwmUp.init(freq=5000, duty=600)
                start = 1
        while (BtnDown.value() == 0 and fimDown.value() ): 
            time.sleep(0.001)
            if start == 0:
                pwmDown.init(freq=5000, duty=600)
                start = 1
            
        pwmUp.init(freq=5000, duty=0) #Para motor apos o tempo definido
        pwmDown.init(freq=5000, duty=0)
        time.sleep(0.1)
        pwmUp.init(freq=5000, duty=0) #Para motor apos o tempo definido
        pwmDown.init(freq=5000, duty=0)
        time.sleep(0.1)
        pwmUp.init(freq=5000, duty=0) #Para motor apos o tempo definido
        pwmDown.init(freq=5000, duty=0)

cc = 0
while(True):
    #MoveMotor("Up", 1)
    if (fimUp.value() == 0):
        pwmUp.init(freq=5000, duty=0)
        time.sleep(0.1)
        pwmUp.init(freq=5000, duty=0)
        time.sleep(0.1)
        pwmUp.init(freq=5000, duty=0)
    if (fimDown.value() == 0 ):
        pwmDown.init(freq=5000, duty=0)
        time.sleep(0.1)
        pwmDown.init(freq=5000, duty=0)
        time.sleep(0.1)
        pwmDown.init(freq=5000, duty=0)
        
        
    cc = cc+1
    time.sleep(0.01)
    print("T1: ", T1.read())
    print("T2: ", T2.read())
    
    if cc >= 100*300:
        cc = 0
        uart.write("Temp," + str(int(T1.read())) + "," + str(int(T2.read())) + ",0")
        print("Temp," + str(int(T1.read())) + "," + str(int(T2.read())) + ",0")
    BtnManual()
#MoveMotor("Down", 3)

#MoveMotor("Down", 0.5)
#time.sleep(0.001)
#MoveMotor("Down", 0.5)
#time.sleep(0.001)



#pid = PID(1, 0, 0, setpoint=30)
#pid.sample_time = 1  # Update every 0.01 seconds


while False:
    time.sleep(1)
    output = pid(35)
     


    
    
