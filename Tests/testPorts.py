from nextion import nextion
import time
from max6675 import MAX6675
from machine import Pin, deepsleep, TouchPad
import esp32
import machine


display = nextion(17, 16, 9600)

T1 = MAX6675(sck_pin=21, cs_pin=19, so_pin=18) 
T2 = MAX6675(sck_pin=26, cs_pin=27, so_pin=14)
T3 = MAX6675(sck_pin=32, cs_pin=33, so_pin=25)

FC1 = Pin(34, Pin.IN)    
FC2 = Pin(35, Pin.IN)  


x=1
time.sleep(2)

t = TouchPad(Pin(4))
t.config(200)               # configure the threshold at which the pin is considered touched
esp32.wake_on_touch(True)
x = 0
while(1):
#nextion test
#     x=x+10
#     print('dormiu')
#     display.sleep(1)
# 
#     time.sleep(30)
# 		
#     print('acordou')
#     display.sleep(0)
# 
#     time.sleep(30)

#Max6675 Test T3

    #print(T1.read())
    #print(FC1.value(), ',',FC2.value() , end='')
    print(T2.readCelsius())
    time.sleep(1)



    
    
