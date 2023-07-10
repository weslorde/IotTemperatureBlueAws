from machine import Pin, PWM
import time

FimUp = Pin(15, Pin.IN, Pin.PULL_UP)
FimDown = Pin(2, Pin.IN, Pin.PULL_UP)

pwmUp = PWM(Pin(23, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 23 responsavel por SUBIR o motor. É iniciado com duty de Zero para nao ativar o motor
pwmUp.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor

pwmDown = PWM(Pin(22, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 22 responsavel por DESCER o motor. É iniciado com duty de Zero para nao ativar o motor
pwmDown.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor

global sentido
sentido = 0

def InterruptFimUp(pin):
    global sentido
    print("UUPPP!!", FimUp.value())
    pwmUp.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
    pwmDown.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
    sentido = 1

def InterruptFimDown(pin):
    global sentido
    print("Downnnn!!", FimDown.value())
    pwmDown.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
    pwmUp.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
    sentido = 0
    
#FimUp.irq(trigger=Pin.IRQ_FALLING, handler=InterruptFimUp)
#FimDown.irq(trigger=Pin.IRQ_FALLING, handler=InterruptFimDown)

pwmUp.init(freq=5000, duty=500)
time.sleep(1)
pwmUp.init(freq=5000, duty=0)

while(True):
    global sentido
    time.sleep(2)
    print("comecou", sentido)
    if sentido == 0 and FimUp.value() == 1 and 0:
        print("subindo")
        pwmUp.init(freq=5000, duty=600)
    elif sentido == 1 and FimDown.value() == 1 and 0:
        print("descendo")
        pwmDown.init(freq=5000, duty=600)
        
    
     