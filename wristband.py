import machine
import utime
import random

from ssd1306 import SSD1306_I2C
from ssd1306 import SSD1306

WIDTH = 128
HEIGHT = 64
scl=machine.Pin(11)
sda=machine.Pin(10)
i2c=machine.I2C(1,sda=sda, scl=scl, freq=400000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)
button_temp = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_coin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
flashlight = machine.Pin(8, machine.Pin.OUT)
onboardLed = machine.Pin(25, machine.Pin.OUT)
switch = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_DOWN)
wirtual3v3_temp = machine.Pin(7, machine.Pin.OUT)
wirtual3v3_temp.value(1)

# after long break temperature sensor sometimes shows wrong value
# in first measurment, this funcion help to "warm up" the sensor
def warm_up():
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    format_temp = "{:.2f}".format(temperature)
    
#converts temperature to celcius degres and show result on the screen
def convert_show_temp():
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    format_temp = "{:.2f}".format(temperature)
    oled.fill(0)
    oled.text('temperatura:' + str(format_temp), 0, 25)
    oled.show()
    utime.sleep(0.25)
    print(temperature)

# makes flip and shows result on the screen
def flip_show():
    coin_flip = bool(random.randint(0,1))
    if coin_flip == True:
        oled.fill(0)
        oled.text('heads', 43, 25)
        oled.show()
    else:
        oled.fill(0)
        oled.text('tails', 40, 25)
        oled.show()

while True:
    onboardLed.value(1)    
    if button_temp.value() == 1:
        warm_up()
        oled.poweron()
        convert_show_temp()
        utime.sleep(3.5)
    else:
        oled.poweroff()
        utime.sleep(0.2)
    if button_coin.value() == 0:
        oled.poweron()
        flip_show()
        utime.sleep(2)
    else:
        oled.poweroff()
        utime.sleep(0.2)
    if switch.value() == 0:
        flashlight.value(0)
        oled.poweroff()
        utime.sleep(0.2)
    while switch.value() == 1:
        flashlight.value(1)
        oled.poweron()
        oled.fill(0)
        oled.text('flashlight mode', 5, 25)
        oled.show()
