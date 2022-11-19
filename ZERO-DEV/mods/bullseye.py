from picamera import PiCamera
from time import sleep

camera = PiCamera()

def TakePhoto(a):
    global camera
    camera.start_preview()
    sleep(2)
    imagename='./image'+str(a)+'.jpg'
    camera.capture(imagename)
    camera.stop_preview()
    print(imagename)

if __name__=="__main__":
    for i in range(3):
        TakePhoto(i)