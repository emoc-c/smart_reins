from ap import *
from mode import *
import time
from machine import  Pin,PWM

buzzer=PWM(Pin(13))
l=[1000,2000,3000,4000]
for f in l:
    buzzer.freq(f)
    print(f)
    buzzer.duty_u16(1000)
    time.sleep(1)
buzzer.duty_u16(0)

    

