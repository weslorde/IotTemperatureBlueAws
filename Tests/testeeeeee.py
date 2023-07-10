from machine import Pin, PWM
import time

pwmUp = PWM(Pin(23, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 23 responsavel por SUBIR o motor. É iniciado com duty de Zero para nao ativar o motor
pwmUp.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor

pwmDown = PWM(Pin(22, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 22 responsavel por DESCER o motor. É iniciado com duty de Zero para nao ativar o motor
pwmDown.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor

time.sleep(1)
print("comecou")
pwmDown = PWM(Pin(22, Pin.OUT), freq=5000, duty=500)
time.sleep(2)
pwmDown = PWM(Pin(22, Pin.OUT), freq=5000, duty=0)

while(True):
    time.sleep(1)
    print(".", end="")
