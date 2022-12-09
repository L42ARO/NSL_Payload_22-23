from picamera import PiCamera
from time import sleep
from datetime import datetime
run = True
try:
    camera = PiCamera()
except:
    print("Camera error")
    run=False

def TakePhoto(a):
    global run
    if run==False: return
    try:
        global camera
        camera.start_preview()
        sleep(2)
        imagename='./image'+str(a)+'.jpg'
        camera.capture(imagename)
        camera.stop_preview()
        print(imagename)
    except Exception as e:
        print(f'Error taking photo: {e}')
        run=False
def SeriesOfPics():
    global run
    if run == False: return
    for i in range(3):
        TakePhoto(i)

if __name__=="__main__":
    for i in range(3):
        TakePhoto(i)