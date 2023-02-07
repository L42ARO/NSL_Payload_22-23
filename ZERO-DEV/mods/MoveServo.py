import piServoCtl

#has to run sudo pigpiod before running
class MainServo:
    def rotate(self, startAngle, endAngle):
        i = -1 if startAngle > endAngle else 1

        for pos in range(startAngle, endAngle, i):
            piServoCtl.write(pos)
            piServoCtl.delay(15)
        piServoCtl.write(endAngle)
    
    def begin(self):
        piServoCtl.pinMode(pin, piServoCtl.OUTPUT)
        piServoCtl.attach(pin)
