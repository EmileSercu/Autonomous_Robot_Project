import time
import lgpio
import sys

LED = 24

# open the gpio chip and set the LED pin as output
h = lgpio.gpiochip_open(0)
ret=lgpio.gpio_claim_output(h, LED)

try:
    while True:
        # Turn the GPIO pin on
        lgpio.gpio_write(h, LED, 1)
        print('gpio high')
        time.sleep(1)

        # Turn the GPIO pin off
        lgpio.gpio_write(h, LED, 0)
        print('gpio low')
        time.sleep(1)
except KeyboardInterrupt:
    lgpio.gpio_write(h, LED, 0)
    lgpio.gpiochip_close(h)
