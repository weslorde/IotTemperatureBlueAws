#AWS MQTT client cert example for esp8266 or esp32 running MicroPython 1.9 
from umqtt.simple import MQTTClient
import time
import wifi
import json
import Perifericos
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
        self.MQTT_CLIENT_ID = "Esp32Board"
        self.MQTT_PORT = 8883

        #if you change the topic make sure update AWS policy
        self.MQTT_TOPIC = "$aws/things/ChurrasTech2406/shadow/name/TemperaturesShadow/update"
        #self.MQTT_TOPIC_Sub = "$aws/things/ChurrasTech2406/shadow/update/delta"
        #self.MQTT_TOPIC_Sub = "$aws/things/ChurrasTech2406/test/tamanho"

        #Change the following three settings to match your environment
        self.MQTT_HOST = "a35wgflbzj4nrh-ats.iot.sa-east-1.amazonaws.com"
        self.mqtt_client = None
        self.iniciaAWS()
            
    def sub_cb(self,topic,msg):
      #print(msg)
      #print(topic)
      jmsg = json.loads(msg)
      #print(topic)
      if topic == b'$aws/things/ChurrasTech2406/shadow/name/TemperaturesShadow/update/delta':
          if jmsg['state']['Enviar'] == "1":
              self.attAwsShadow()
          elif jmsg['state']['TAlvoFlutter'] != "0":
              newTAlvo = jmsg['state']['TAlvoFlutter']
              print("NovoTalvo: ",newTAlvo)
              Perifericos.DefineAlvo(int(newTAlvo))
              self.pub_msg(b'''{"state": {"desired": {"TAlvoFlutter": "0","TAlvoEsp": "%s"}}}''' % newTAlvo)
              
    
      elif topic == b'$aws/things/ChurrasTech2406/shadow/name/AlarmShadow/update/delta':
          if jmsg['state']['Enviar'] == "1":
              TimerAlarme, GrausAlarme = Perifericos.getAlarm()
              print(TimerAlarme, GrausAlarme)
              TimerAlarmeFlutter = []
              for x in TimerAlarme:
                  TimerAlarmeFlutter.append(x[0:2])
              self.pub_msg(b'''{"state": {"desired": {"Enviar": "0","TimerAlarm": "%s","GrausAlarm": "%s"}}}''' %(TimerAlarmeFlutter, GrausAlarme), topic='$aws/things/ChurrasTech2406/shadow/name/AlarmShadow/update')
     
      elif topic == b'$aws/things/ChurrasTech2406/shadow/name/MotorShadow/update/delta':         
          Perifericos.DefineAlvo(0)
          print(jmsg['state']['Nivel'],jmsg['state']['Sentido'])
          if jmsg['state']['Nivel'] == "Press":
              Perifericos.DispDefUpDown(jmsg['state']['Sentido'], 1)
          elif jmsg['state']['Nivel'] == "Release": 
              Perifericos.DispDefUpDown(jmsg['state']['Sentido'], 0)
            
              
      #with open("arquivo.py", "w") as file:
      #    file.write(msg)
      
      #time.sleep(5)
      #execfile('arquivo.py')

    def attAwsShadow(self):
        TGrelha, TSensor1, TSensor2, TempAlvo = Perifericos.GetTemps()
        msg = b'''{
                  "state": {
                    "desired": {
                      "Grelha": "%s",
                      "Temp1": "%s",
                      "Temp2": "%s",
                      "TAlvoEsp": "%s",
                      "Enviar": "0"
                    }
                  }
                }''' %(TGrelha, TSensor1, TSensor2, TempAlvo)
        #print(msg)
        self.pub_msg(msg)

    def restart_and_reconnect():
      print('Failed to connect to MQTT broker. Reconnecting...')
      time.sleep(5)
      #reset()
      
    def pub_msg(self, msg, topic=""):
        try:  
            if topic == "":
                self.mqtt_client.publish(self.MQTT_TOPIC, msg)
                #print("Sent: " + msg)
                #print("Enviando Dados Atuais")
            else:
                self.mqtt_client.publish(topic, msg)
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
            print('indo para o sub')
            self.mqtt_client.set_callback(self.sub_cb)
            print('indo para o conect')
            self.mqtt_client.connect()
            print('MQTT Connected')
            self.mqtt_client.subscribe("$aws/things/ChurrasTech2406/shadow/name/TemperaturesShadow/update/delta")
            self.mqtt_client.subscribe("$aws/things/ChurrasTech2406/shadow/name/AlarmShadow/update/delta")
            self.mqtt_client.subscribe("$aws/things/ChurrasTech2406/shadow/name/MotorShadow/update/delta")
            
            
        except Exception as e:
            print('Cannot connect MQTT: ' + str(e))
            self.restart_and_reconnect()
            machine.reset()
            raise


    def checaMsg(self):
        awsMsg = self.mqtt_client.check_msg()
        #if awsMsg != None:
            #print(awsMsg)
          
    def mandaMsg(self, n):
        self.pub_msg(b'''{
                  "state": {
                    "reported": {
                      "TAlvo": "''' + n + b'''"
                    }}}''' )
            
     
    def iniciaAWS(self):
        #self.topic_sub = "$aws/things/ChurrasTech2406/shadow/update/delta"
        self.topic_sub = "$aws/things/ChurrasTech2406/test/tamanho"
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
    while(1):
        #for x in range (100000):
        #    pass
        x = x+10
        time.sleep(1)
        print(x)
    

if __name__ == "__main__":
    AWSLoop()