import cv2
from picamera import PiCamera
from time import sleep
from datetime import datetime
import mods.talking_heads as talking_heads

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

def take_grayscale_picture(camera):
    # Set camera resolution and color mode to grayscale
    camera.resolution = (640, 480)
    camera.color_effects = (128, 128)
    camera.start_preview()
    sleep(2)  # Wait for camera to warm up

    # Capture grayscale image
    image = np.empty((camera.resolution[1], camera.resolution[0], 3), dtype=np.uint8)
    camera.capture(image, 'rgb')

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    return gray

def convert_to_grayscale(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    return gray

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

def operateCam (command):
    if command == "A1":
        talking_heads.talk(4, -60)
        #turn_camera_right60()
    elif command == "B2":
        talking_heads.talk(4, 60)
        #turn_camera_left60()
    elif command == "C3":
        print("")
        #take_picture()
    elif command == "D4":
        print("")
        #set_camera_mode("G")
    elif command == "E5":
        print("")
        #set_camera_mode("C")
    elif command == "F6":
        print("")
        #rotate_image180()
    elif command == "G7":
        print("")
        #apply_filter()
    elif command == "H8":
        print("")
        #remove_filters()
    else:
        print("Error: Invalid Input.")

if __name__=="__main__":
    for i in range(3):
        TakePhoto(i)