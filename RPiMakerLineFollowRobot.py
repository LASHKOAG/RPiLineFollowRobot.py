#IdrisCytron/RPiMakerLineFollowRobot.py
#https://gist.github.com/IdrisCytron/3e64af6e81f6d75138ce9d0f89004230#file-rpimakerlinefollowrobot-py

from gpiozero import Button, Buzzer, LineSensor
from time import sleep
import pigpio
from os import system

pi = pigpio.pi()

sw1 = Button(21)
sw2 = Button(16)
sw3 = Button(20)

buzzer = Buzzer(26)

sensorD1 = LineSensor(27)
sensorD2 = LineSensor(22)
sensorD3 = LineSensor(25)
sensorD4 = LineSensor(12)
sensorD5 = LineSensor(13)

M1A = 18
M1B = 17
M2A = 3
M2B = 2

pi.set_mode(M1A, pigpio.OUTPUT)
pi.set_mode(M1B, pigpio.OUTPUT)
pi.set_mode(M2A, pigpio.OUTPUT)
pi.set_mode(M2B, pigpio.OUTPUT)

def readMakerLine():
    global sensorReading
    sensorString = ""
    sensorReading = 1*(sensorD5.value) + \
                    2*(sensorD4.value) + \
                    4*(sensorD3.value) + \
                    8*(sensorD2.value) + \
                    16*(sensorD1.value)
    
    if sensorReading < 16:
        sensorString = "0"
    if sensorReading < 8:
        sensorString = sensorString + "0"
    if sensorReading < 4:
        sensorString = sensorString + "0"
    if sensorReading < 2:
        sensorString = sensorString + "0"
    
    sensorString = sensorString + "{0:b}".format(sensorReading)
    print("Maker Line: " + sensorString)

def robotMove(speedLeft, speedRight):
    if speedLeft > 0:
        pi.set_PWM_dutycycle(M1A, 0)
        pi.set_PWM_dutycycle(M1B, speedLeft)
    else:
        pi.set_PWM_dutycycle(M1A, abs(speedLeft))
        pi.set_PWM_dutycycle(M1B, 0)

    if speedRight > 0:
        pi.set_PWM_dutycycle(M2A, 0)
        pi.set_PWM_dutycycle(M2B, speedRight)
    else:
        pi.set_PWM_dutycycle(M2A, abs(speedRight))
        pi.set_PWM_dutycycle(M2B, 0)

def sw1Pressed():
    global robotGo
    robotGo = True
    buzzer.beep(0.1, 0.1, 1)

def sw2Pressed():
    global robotGo
    robotGo = False
    buzzer.beep(0.1, 0.1, 1)

sw1.when_pressed = sw1Pressed
sw2.when_pressed = sw2Pressed

sensorReading = 0

robotGo = False

buzzer.beep(0.1, 0.1, 2)

try:
    while True:
        if robotGo == False:
            robotMove(0, 0)
        else:
            readMakerLine()
            # You can adjust motor speed based on your hardware
            if sensorReading == 0b00100 or sensorReading == 0b01110:
                robotMove(40, 40)
            elif sensorReading == 0b01100:
                robotMove(30, 40)
            elif sensorReading == 0b00110:
                robotMove(40, 30)
            elif sensorReading == 0b11100:
                robotMove(20, 40)
            elif sensorReading == 0b00111:
                robotMove(40, 20)
            elif sensorReading == 0b11000:
                robotMove(10, 40)
            elif sensorReading == 0b00011:
                robotMove(40, 10)
            elif sensorReading == 0b10000:
                robotMove(0, 40)
            elif sensorReading == 0b00001:
                robotMove(40, 0)
            elif sensorReading == 0b11111:
                robotMove(30, 30)

        if sw3.is_pressed:
            robotMove(0, 0)
            sleep(1)
            buzzer.beep(0.2, 0.2, 3)
            sleep(1)
            system('sudo shutdown -h now')

except KeyboardInterrupt:
    buzzer.off()
    robotMove(0, 0)
