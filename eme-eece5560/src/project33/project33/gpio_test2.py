from gpiozero import OutputDevice
from time import sleep

led = OutputDevice(23)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
