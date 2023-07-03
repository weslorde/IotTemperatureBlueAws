from machine import Pin, PWM
import time
from max6675 import MAX6675


#T2 = MAX6675(sck_pin=27, cs_pin=14, so_pin=12) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K
#T1 = MAX6675(sck_pin=33, cs_pin=25, so_pin=26) #Inicia comunicacao com o modulo max6675 responsavel por comunicar com o termopar tipo K

#pwmUp = PWM(Pin(23, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 23 responsavel por SUBIR o motor. É iniciado com duty de Zero para nao ativar o motor
#pwmDown = PWM(Pin(22, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 22 responsavel por DESCER o motor. É iniciado com duty de Zero para nao ativar o motor

#pwmUp.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
#pwmDown.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor


#while(True):
  
time.sleep(3)

if(False):
    Up = Pin(23, Pin.OUT)
    Down = Pin(22, Pin.OUT)

    print("up")
    Up.on()
    time.sleep(1)
    Up.off()

    time.sleep(3)

    print("Down")
    Down.on()
    time.sleep(1)
    Down.off()

if(True):
    
    pwmUp = PWM(Pin(22, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 23 responsavel por SUBIR o motor. É iniciado com duty de Zero para nao ativar o motor
    pwmDown = PWM(Pin(23, Pin.OUT), freq=5000, duty=0) #Cria sinal PWM no pino 22 responsavel por DESCER o motor. É iniciado com duty de Zero para nao ativar o motor

    pwmUp.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
    pwmDown.init(freq=5000, duty=0) #Inicia sinal PWM de zero para garantir que não vai ativar o motor
    
    #print("Temp1:", T1.read())

    #print("Temp2:", T2.read())
    
    print("comecou")
    pwmDown.init(freq=5000, duty=600)
    time.sleep(3)
    pwmDown.init(freq=5000, duty=0)
        
    while(True):
        time.sleep(2)
        
        print("comecou")
        pwmUp.init(freq=5000, duty=600)
        time.sleep(3.2)
        pwmUp.init(freq=5000, duty=0)

        print("foi down")
        time.sleep(2)

        pwmDown.init(freq=5000, duty=600)
        time.sleep(2)
        pwmDown.init(freq=5000, duty=0)




print("fim")
