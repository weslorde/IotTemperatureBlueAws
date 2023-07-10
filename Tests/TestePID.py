from PID import PID
import time

pid = PID(1/10, 0.01, 0, setpoint=50)
pid.sample_time = 2  # Update every 0.01 seconds

x=60
n=0
while True:
    time.sleep(1)
    #x = x + 0.1
    n = n+1
    output = pid(x)
    print(n, ":  ", x, "--",output)
    if n == 10: n = 0