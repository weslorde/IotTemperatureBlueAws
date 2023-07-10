import time

import TestFlutterBlueTest
import AlexaAWS
import wifi
import BLEtest
import esp
esp.osdebug(None)

aws = AlexaAWS.AWS()

time.sleep(10)

#BlueEsp = TestFlutterBlueTest.FlutterBlue()
BlueEsp = BLEtest.demo()
#wifi.WifiConectar()

while(1):
    time.sleep(2)
    print(".", end="")