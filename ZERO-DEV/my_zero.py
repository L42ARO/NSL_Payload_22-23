import mods.mr_blue_sky as mr_blue_sky
import mods.happy_landing as happy_landing
import mods.talking_heads as talking_heads
import mods.bullseye as bullseye
import mods.utils as utils
import mods.MoveServo as MoveServo
import RPI.GPIO as GPIO
gpio_buzz=False


if __name__=="__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.OUT)
        GPIO.output(23, GPIO.HIGH)
        utils.exitListen()
        print("Starting ZERO-DEV")

        Servo1Pin = 19
        coverServo = MoveServo.begin(Servo1Pin,True)

        MoveServo.rotate(coverServo, 0, 180)
        happy_landing.checkForLanding()

        MoveServo.rotate(coverServo, 180, 0)
        mr_blue_sky.moveToHole(1)

        #define pins
        Servo2Pin = 12
        Servo3Pin = 18

        extenderServo = MoveServo.begin(Servo2Pin,True)
        gimbalServo = MoveServo.begin(Servo3Pin,True)

        MoveServo.rotate(extenderServo, 0, 45)
        mr_blue_sky.MoveGimbal(gimbalServo)

        bullseye.SeriesOfPics()
    except Exception as e:
        print('failed')