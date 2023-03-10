import cv2
import numpy as np
from picamera import PiCamera
from time import sleep
from datetime import datetime
import mods.talking_heads as talking_heads

run = True
grayScale = False 
photo_id = 0

try:
    camera = PiCamera()
except:
    print("Camera error")
    run=False

# appends the filename to index.txt
def writeDB(imagename):
    with open("index.txt", "a") as db:
        db.write(f"{imagename}\n")
        
def TakePhoto():
    global run, photo_id
    if run==False: return
    try:
        global camera
        camera.start_preview()
        sleep(2)
        timestamp = str(datetime.now().timestamp()).replace('.', '_')
        imagename='./og-pics/'+str(photo_id)+'_'+timestamp+'.jpg'
        photo_id += 1
        camera.capture(imagename)
        camera.stop_preview()
        writeDB(imagename)
        print("Photo taken.  Filename: " + imagename)
    
    except Exception as e:
        print(f'Error taking photo: {e}')
        run=False

def SeriesOfPics():
    global run
    if run == False: return
    for i in range(3):
        TakePhoto(i)

def take_grayscale_picture():
    global camera
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
    # Overwrite the image to grayscale
    cv2.imwrite(image, cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))

    

def add_timestamp(img):
    # Get current time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

def rotate_existing_image(image_path, degree):
    # Load existing image
    img = cv2.imread(image_path)
    # Get image size
    rows,cols = img.shape[:2]
    # Define rotation matrix
    M = cv2.getRotationMatrix2D((cols/2,rows/2),degree,1)
    # Perform rotation
    img_rotated = cv2.warpAffine(img,M,(cols,rows))
    # Save rotated image
    cv2.imwrite(image_path, img_rotated)

def apply_filter(image_path, kernel):
    # Load existing image
    img = cv2.imread(image_path)
    # Apply filter using filter2D function
    filtered_img = cv2.filter2D(img, -1, kernel)
    # Save filtered image
    cv2.imwrite('filtered_image.jpg', filtered_img)

def apply_edgedet_filter(image_path):
    kernel = np.array([[-1,-1,-1],
                   [-1, 8,-1],
                   [-1,-1,-1]])
    apply_filter(image_path, kernel)



def operateCam (command):
    if command == "A1":
        #turns camera right 60 degrees
        talking_heads.talk(4, -60) #case 4 microstepper gives value to rotate
    elif command == "B2":
        #turns camera left 60 degrees
        talking_heads.talk(4, 60) #case 4 microstepper, pass rotation value
    elif command == "C3":
        TakePhoto()
        #take_picture()
    elif command == "D4":
        grayScale = True
        #set_camera_mode("G")
    elif command == "E5":
        grayScale = False
        #set_camera_mode("C")
    elif command == "F6":
        rotate_existing_image(photo_id, 180)
    elif command == "G7":
        print("")
        #apply_filter()
    elif command == "H8":
        print("")
        #remove_filters()
    else:
        print("Error: Invalid Input.")

if __name__=="__main__":
    behelit = TakePhoto(photo_id)
    apply_edgedet_filter(behelit)
    photo_id += 1
    grayScale=True
    TakePhoto("gray_" if grayScale else "regular_" + photo_id)
    photo_id += 1
    Xena = TakePhoto("gray_" if grayScale else "regular_" + photo_id)
    rotate_existing_image(Xena)
    photo_id += 1     