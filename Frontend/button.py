from machine import Pin
import time

button = Pin(18, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        print("Tu Pagal hai.")
    time.sleep(0.1)