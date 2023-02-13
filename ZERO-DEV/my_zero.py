import mods.mr_blue_sky as mr_blue_sky
import mods.happy_landing as happy_landing
import mods.talking_heads as talking_heads
import mods.bullseye as bullseye
import mods.utils as utils

if __name__=="__main__":
    utils.exitListen()
    print("Starting ZERO-DEV")
    happy_landing.checkForLanding()
    mr_blue_sky.moveToHole()
    mr_blue_sky.servoMover(0)
    mr_blue_sky.servoMover(90)
    bullseye.SeriesOfPics()