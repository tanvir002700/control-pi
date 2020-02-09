import os
from time import sleep
import RPi.GPIO as GPIO


fanPin = 17
maxTMP = 45


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(fanPin, GPIO.OUT)
    fanOFF()
    return

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    return temp

def fanON():
    GPIO.output(fanPin, True)
    return

def fanOFF():
    GPIO.output(fanPin, False)
    return

def handleFan():
    CPU_temp = float(getCPUtemperature())
    if CPU_temp > maxTMP:
        fanON()
        print("fan on")
        sleep(30)
    if CPU_temp <= maxTMP-10:
        fanOFF()
        print("fan off")
    return

try:
    setup()
    while True:
        print("running", getCPUtemperature())
        handleFan()
        sleep(5) # Read the temperature every 5 sec
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    fanOFF()
    GPIO.cleanup()
