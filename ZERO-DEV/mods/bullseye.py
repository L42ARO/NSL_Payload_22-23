import cv2
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

def add_timestamp(img):
    # Get current time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add timestamp to the upper right corner of the image
    cv2.putText(img, timestamp, (img.shape[1]-150,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
    # Return the image
    return img

def rotate_image(img, degree):
    # Get image size
    rows,cols = img.shape[:2]
    # Define rotation matrix
    M = cv2.getRotationMatrix2D((cols/2,rows/2),degree,1)
    # Perform rotation
    img_rotated = cv2.warpAffine(img,M,(cols,rows))
    # Return rotated image
    return img_rotated


if __name__=="__main__":
    for i in range(3):
        TakePhoto(i)