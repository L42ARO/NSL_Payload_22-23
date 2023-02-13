import mods.mr_blue_sky as mr_blue_sky
import mods.happy_landing as happy_landing
import mods.talking_heads as talking_heads
import mods.bullseye as bullseye
import mods.utils as utils
import mods.MoveServo as MoveServo

if __name__=="__main__":
    utils.exitListen()
    print("Starting ZERO-DEV")
    happy_landing.checkForLanding()
    mr_blue_sky.moveToHole()

    #define pins
    Servo1Pin = 18
    Servo2Pin = 19
    Servo3Pin = 12

    MoveServo.begin(Servo1Pin,True)
    MoveServo.begin(Servo2Pin,True)
    MoveServo.begin(Servo3Pin,True)
    
    mr_blue_sky.servoMover(90)
    bullseye.SeriesOfPics()