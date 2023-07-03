#AWS MQTT client cert example for esp8266 or esp32 running MicroPython 1.9 
from umqtt.simple  import MQTTClient
import time
import wifi
#import esp



class AWS:
    def __init__(self):
        #try:
          #import usocket as socket
        #except:
          #import socket
          
        #import network

        #esp.osdebug(None)
        #import gc
        #gc.collect()

        wifi.WifiConectar()
        #This works for either ESP8266 ESP32 if you rename certs before moving into /flash 
        self.CERT_FILE = "/Cert/ChurrasTech.cert.der"
        self.KEY_FILE = "/Cert/ChurrasTechPrivate.key.der"

        #if you change the ClientId make sure update AWS policy
        self.MQTT_CLIENT_ID = "ChurrasTech2406"
        self.MQTT_PORT = 8883

        #if you change the topic make sure update AWS policy
        self.MQTT_TOPIC = "$aws/things/ChurrasTech2406/shadow/update"
        self.MQTT_TOPIC_Sub = "$aws/things/ChurrasTech2406/shadow/update/delta"

        #Change the following three settings to match your environment
        self.MQTT_HOST = "a35wgflbzj4nrh-ats.iot.sa-east-1.amazonaws.com"
        self.mqtt_client = None
        self.iniciaAWS()
        

    def sub_cb(topic, msg):
      print(topic, msg)
      if topic == b'notification' and msg == b'received':
        print('ESP received hello message')


    def restart_and_reconnect():
      print('Failed to connect to MQTT broker. Reconnecting...')
      time.sleep(5)
      #reset()
      
    def pub_msg(self, msg):
        try:    
            self.mqtt_client.publish(self.MQTT_TOPIC, msg)
            #print("Sent: " + msg)
            #print("Enviando Dados Atuais")
        except Exception as e:
            print("Exception publish: " + str(e))

    def connect_mqtt(self):    
        try:
            with open(self.KEY_FILE, "r") as f: 
                key = f.read()

            print("Got Key")
                
            with open(self.CERT_FILE, "r") as f: 
                cert = f.read()

            print("Got Cert")	

            self.mqtt_client = MQTTClient(client_id= self.MQTT_CLIENT_ID, server= self.MQTT_HOST, ssl=True, ssl_params={"cert":cert, "key":key, "server_side":False})
            #mqtt_client = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_HOST, port=MQTT_PORT, keepalive=60, ssl=True, ssl_params={"cert":cert, "key":key, "server_side":False})
            self.mqtt_client.set_callback(self.sub_cb)
            self.mqtt_client.connect()
            print('MQTT Connected')

            
        except Exception as e:
            print('Cannot connect MQTT: ' + str(e))
            self.restart_and_reconnect()
            raise


    def checaMsg(self):  
        print(self.mqtt_client.check_msg())
          
    def mandaMsg(self, n):
        self.pub_msg(b'''{
                  "state": {
                    "reported": {
                      "TAlvo": "''' + n + b'''"
                    }}}''' )
            
     
    def iniciaAWS(self):
        self.topic_sub = "$aws/things/ChurrasTech2406/shadow/update/delta"
        #start execution
        try:
            print("Connecting MQTT...")
            self.connect_mqtt()
            #print("Inscrevendo no topico")
            #mqtt_client.subscribe(topic_sub)
            
        except Exception as e:
            print(str(e))        

def AWSLoop():
    x = 0

    IotAWS = AWS()
    time.sleep(5)
    teste2 = _thread.start_new_thread(TestFlutterBlue.blueLoop, ())
    while(1):
        #for x in range (100000):
        #    pass
        x = x+10
        IotAWS.mandaMsg(str(x))
        time.sleep(1)
    

if __name__ == "__main__":
    AWSLoop()