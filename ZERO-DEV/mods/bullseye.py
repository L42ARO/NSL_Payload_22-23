#import cv2
import numpy as np
from picamera import PiCamera
from time import sleep
from datetime import datetime
#from wand.image import Image 
import mods.talking_heads as talking_heads
import os
from PIL import Image

run = True
grayScale = False 
filterMode = False
photo_id = 0

#Declaring folder names
og_images_folder = "og-images"
mission_folder = "mission"
final_folder = "final"

#Processing path depending on current directory being called from
folder_path = os.path.basename(os.getcwd())
if not (os.path.basename(os.getcwd()) == 'mods'):
    folder_path = os.path.join(folder_path, 'mods')

og_images_folder = os.path.join(folder_path, og_images_folder)
mission_folder = os.path.join(folder_path, mission_folder)
final_folder = os.path.join(folder_path, final_folder)

#Setting up the camera
global camera
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
    if run==False:
        print("Camera failed to initialize")
        return
    try:
        global camera
        camera.start_preview()
        sleep(2)
        path = os.path.realpath(__file__)   # __file__ = absolute path of myzero.py
        dir = os.path.dirname(path)
        timestamp = str(datetime.now().timestamp()).replace('.', '_')
        imagename = os.path.join(dir, "og-pics", str(photo_id)+'_'+timestamp+'.jpg')
        photo_id += 1
        camera.capture(imagename)
        camera.stop_preview()
        writeDB(imagename)
        print("Photo taken.  Filename: " + imagename)
    
    except Exception as e:
        print(f'Error taking photo: {e}')
        run=False

def SeriesOfPics(sequence):
    #sequence: array<strings>
    for cmd in sequence:
        operateCam(cmd)

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

def convert_to_grayscale(i):
    # Overwrite the image to grayscale
    #cv2.imwrite(image, cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))
    gray_image = i.convert("L")
    return gray_image

def post_process():
    try:
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        with open(dir+'/og-pics/index.txt', 'r') as f:
            last_image = f.readlines()[-1]
        image = Image.open(last_image)
        if(grayScale):
            print("Applying grayscale filter")
            image=convert_to_grayscale(image)
        if(distortion):
            print("Applying distortion filter")
        image.save('./mission/processed_image.jpg')
    except Exception as e:
        print(f'Failed to post process: {e}')
        
def add_timestamp(img):
    # Get current time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add timestamp to the upper right corner of the image
    cv2.putText(img, timestamp, (img.shape[1]-150,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
    # Return the image
    return img
def latestImage(folder):
    files = os.listdir(folder_path)
    image_files = [f for f in files if f.endswith('.jpg') or f.endswith('.png')]
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    latest_image_path = os.path.join(folder_path, image_files[0])

    return Image.open(latest_image_path)
        
def rotate_existing_image():
    try:
        image = latestImage('mission')
    except Exception as e:
        print(f'Failed to rotate image: {e}')

#Requires the Wand package from python
#May need to edit the file location for function to work as intended
#def distortion():
#    with open('./og-pics/index.txt') as file:
#        #Grabs the last character from the index.txt file
#        imgNum = file.readlines()[-1]
#    #Saves the image for distortion from its original location
#    image = './og-pics/' + str(imgNum) + '.jpg'
#    #Arguments for the distortion to occur
#    args = (0.2, 0.0, 0.0, 1.5)
#    #Distorts image using a barrel distortion
#    with Image(filename = image) as img:
#        img.distort('barrel', args)
#        img.save(filename = './Mission/' + str(imgNum) + '.jpg')
#    print("Barrel distortion has been applied to the image.")

#dubious type of gaming out here
def Easy_filter(image):

    from PIL.ImageFilter import(CONTOUR)
    filtered_image = image.filter(CONTOUR)
    return filtered_image




def apply_edgedet_filter(image_path):
    kernel = np.array([[-1,-1,-1],
                   [-1, 8,-1],
                   [-1,-1,-1]])
    apply_filter(image_path, kernel)

def operateCam (command:str):
    global grayScale
    print(f'Executing {command}: ')
    if command == "A1":
        #turns camera right 60 degrees
        print("Turn camera right 60 deg")
        talking_heads.talk(4, -60) #case 4 microstepper gives value to rotate
    elif command == "B2":
        #turns camera left 60 degrees
        print("Turn camera left 60 deg")
        talking_heads.talk(4, 60) #case 4 microstepper, pass rotation value
    elif command == "C3":
        print("Taking photo")
        TakePhoto()
        #take_picture()
    elif command == "D4":
        print("Changing to grayscale mode")
        grayScale = True
        #set_camera_mode("G")
    elif command == "E5":
        print("Exiting grayscale mode")
        grayScale = False
        #set_camera_mode("C")
    elif command == "F6":
        print("Rotate last image by 180 degrees")
        rotate_existing_image(photo_id, 180)
    elif command == "G7":
        print("Changing to filter mode")
        filterMode = True
        #apply_filter()
    elif command == "H8":
        print("Exiting filter mode")
        filterMode = False
        #remove_filters()
    else:
        print("Invalid Input.")

if __name__=="__main__":
    import contact
    seq = contact.GetRAFCOSequence()
    SeriesOfPics(seq)