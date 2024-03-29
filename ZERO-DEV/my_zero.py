import mods.mr_blue_sky as mr_blue_sky
import mods.buzzer as buzzer
import mods.happy_landing as happy_landing
import mods.talking_heads as talking_heads
import mods.bullseye as bullseye
import mods.utils as utils
from mods.MoveServo import ServoMotor
import mods.contact as contact
import time
import argparse
import mods.reset_arduino as reset_arduino
import mods.RadioGaGa as RadioGaGa

parser = argparse.ArgumentParser(description='ZERO-DEV')
parser.add_argument('--test', action='store_true', help='Run test. Will not run the await loop.')
args = parser.parse_args()

#Define Pins
buzzerPin = 21
coverPin = 26
extenderPin = 12
gimbalPin = 18
runAwait = True

if __name__=="__main__":
    reset_arduino.reset()
    if args.test:
        runAwait = False
    try:
        print("Starting ZERO-DEV")
        buzzer.runTest(buzzerPin)

        utils.exitListen()

        coverServo = ServoMotor(coverPin)
        extenderServo = ServoMotor(extenderPin)
        gimbalServo = ServoMotor(gimbalPin)

        coverServo.rotate(0)
        extenderServo.rotate(0)
        #gimbalServo.rotate(0)

        time.sleep(1)

        #Cover the holes
        coverServo.rotate(180)

        if runAwait:
            try:
                happy_landing.checkForLanding(120)
            except Exception as e:
                print(f'Failed to check for landing: {e}')
                print('Executing default landing sequence awaiting for 2 hours')
                time.sleep(180)
        else:
            time.sleep(1)
            
        buzzer.startBuzzer()
        
        #Remove the cover
        coverServo.rotate(0)
        time.sleep(1)

        #Move the extender to the desired hole
        mr_blue_sky.moveToHole(3)
        
        #Extend the extender
        #gimbalServo.rotate(90)
        time.sleep(1)
        extenderServo.rotate(160)
        time.sleep(1)
        #Move the gimbal to the true vertical
        #mr_blue_sky.MoveGimbal(gimbalServo, 0)

        #Get RAFCO sequence
        seq = RadioGaGa.get_commands()

        #Take pictures
        bullseye.TakePhoto()
        bullseye.SeriesOfPics(seq)
        reset_arduino.reset()

    except Exception as e:
        print(f'failed: {e}')

        