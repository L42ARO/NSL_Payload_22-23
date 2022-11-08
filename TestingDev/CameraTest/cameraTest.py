from picamera import PiCamera
from time import sleep

def TakePhoto(a, camera):
    camera.start_preview()
    sleep(2)
    imagename='./image'+str(a)+'.jpg'
    camera.capture(imagename)
    camera.stop_preview()
    print(imagename)

if __name__=="__main__":
    camera = PiCamera()
    for i in range(3):
        TakePhoto(i, camera)