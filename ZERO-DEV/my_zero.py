import mods.mr_blue_sky as mr_blue_sky
import mods.buzzer as buzzer
import mods.happy_landing as happy_landing
import mods.talking_heads as talking_heads
#import mods.bullseye as bullseye
import mods.utils as utils
from mods.MoveServo import ServoMotor
import mods.contact as contact
import time
import argparse

parser = argparse.ArgumentParser(description='ZERO-DEV')
parser.add_argument('--test', action='store_true', help='Run test. Will not run the await loop.')
args = parser.parse_args()

buzzerPin = 10
Servo1Pin = 19
Servo2Pin = 12
Servo3Pin = 18
runAwait = True

if __name__=="__main__":
    if args.test:
        runAwait = False
    try:
        print("Starting ZERO-DEV")
        buzzer.runTest(buzzerPin)

        utils.exitListen()

        coverServo = ServoMotor(Servo1Pin)
        extenderServo = ServoMotor(Servo2Pin)
        gimbalServo = ServoMotor(Servo3Pin)

        coverServo.rotate(0)
        extenderServo.rotate(0)
        gimbalServo.rotate(0)

        time.sleep(1)

        #Cover the holes
        coverServo.rotate(180)

        if runAwait:
            try:
                happy_landing.checkForLanding()
            except Exception as e:
                print(f'Failed to check for landing: {e}')
                print('Executing default landing sequence awaiting for 2 hours')
                time.sleep(7200)
        else:
            time.sleep(1)

        #Remove the cover
        coverServo.rotate(0)
        time.sleep(1)

        #Move the extender to the desired hole
        mr_blue_sky.moveToHole(1)
        
        #Extend the extender
        extenderServo.rotate(180)
        time.sleep(1)
        #Move the gimbal to the true vertical
        mr_blue_sky.MoveGimbal(gimbalServo, 0)

        #Get RAFCO sequence
        seq = contact.GetRAFCOSequence()

        #Take pictures
        #bullseye.SeriesOfPics(seq)
    except Exception as e:
        print('failed')