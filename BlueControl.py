from machine import Pin
import time
import bluetooth
from BLE import BLEUART
import binascii

def on_rx():
    global dadosWifi
    msgRecebida = uart.read().decode()
    msgRecebida = msgRecebida.split("\x00") #Remove codigo de final da string
    print(msgRecebida[0])
    #msgRecebida = ExtASCII.myASCIIextToString( msgCodificada )  
    
    #print(msgRecebida)
    
    if(msgRecebida[0] == "Ping"):
        time.sleep(1)
        uart.write("22,33,50")
    else: print("Mensagem nao conhecida:", msgRecebida)

name = "ChurrasTech"  #"78:E3:6D:17:1A:4E"
ble = bluetooth.BLE() 
uart = BLEUART(ble, name)
uart.irq(handler = on_rx)
print("Iniciou Blue")

