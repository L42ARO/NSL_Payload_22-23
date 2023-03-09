from gpiozero import Buzzer
import time

global starttime , buzzer
starttime= 0
buzzPin = 23
interval = 1    # in seconds
buzzerOn = False

def setBuzzerPin(pin):
    global buzzPin,buzzer
    buzzPin = pin
    buzzer = Buzzer(pin)

def toggleBuzzer():
    global buzzerOn, buzzer
    buzzerOn = not buzzerOn
    if(buzzerOn):
        buzzer.on()
    else:
        buzzer.off()


def startBuzzer():
    global starttime
    starttime = time.time()
    buzzer.on()

def turnoffBuzzer():
    buzzer.off()

def updateBuzzer():
    global starttime
    if (time.time() - starttime > interval):
        toggleBuzzer()
        starttime = time.time()
def runTest(pin):
    try:
        setBuzzerPin(pin)
    except Exception as e:
        print("Exception setting buzzer pin: ", e)
    startBuzzer()
    time.sleep(1)
    turnoffBuzzer()


if (__name__=="__main__"):
    i = 0
    startBuzzer()
    while (i < 100):
        updateBuzzer()
        i+=1
    turnoffBuzzer()