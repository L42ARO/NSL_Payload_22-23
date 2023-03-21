import json
import numpy as np
from picamera import PiCamera
from time import sleep
from datetime import datetime
#from wand.image import Image 
import mods.talking_heads as talking_heads
from mods.utils import Database
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import mods.reset_arduino as reset_arduino

run = True
grayScale = False 
filterMode = False
rotateMode = False
photo_id = 0

#Declaring folder names
#comment out og images and final
og_images_folder = "og-images"
mission_folder = "mission"
final_folder = "final"

#Processing path depending on current directory being called from
folder_path = os.getcwd()
if not (os.path.basename(os.getcwd()) == 'mods'):
    folder_path = os.path.join(folder_path, 'mods')


#comment out og images and final
og_images_folder = os.path.join(folder_path, og_images_folder)
mission_folder = os.path.join(folder_path, mission_folder)
final_folder = os.path.join(folder_path, final_folder)

#Setting up the camera
global camera, og_images_db, mission_db, final_db
try:
    camera = PiCamera()
except:
    print("Camera error")
    run=False

def TakePhoto():
    global run, photo_id
    timestamp = str(datetime.now().timestamp())
    timestr = timestamp.replace('.', '_')
    imagename = str(photo_id)+'_'+timestr+'.jpg'
    imagepath = os.path.join(og_images_folder, imagename)
    db_entry = {"name": imagename, "path":imagepath, "timestamp": timestamp}
    #comment down below
    og_images_db.add_entry(db_entry)

    if run==False:
        print("Camera failed to initialize")
        return
    try:
        global camera
        camera.start_preview()
        sleep(2)
        photo_id += 1
        camera.capture(imagepath)
        camera.stop_preview()
        print("Photo taken.  Filename: " + imagepath)
    
    except Exception as e:
        print(f'Error taking photo: {e}')
        run=False

def SeriesOfPics(sequence):
    global og_images_db, mission_db, final_db
    try:
        og_images_db = Database(og_images_folder)
        mission_db = Database(mission_folder)
        final_db = Database(final_folder)
    except Exception as e:
        print(f'Unable to setup databases:{e}')
    for cmd in sequence:
        try:
            operateCam(cmd)
        except:
            print(f'Unable to run command {cmd}')
            reset_arduino.reset()

def convert_to_grayscale(i):
    # Overwrite the image to grayscale
    gray_image = i.convert("L")
    return gray_image

def post_process():
    try:
        image, imgObj = latestImage(og_images_db)
        if(grayScale):
            print("Applying grayscale filter")
            image=convert_to_grayscale(image)
        if(filterMode):
            print("Applying distortion filter")
            image = Easy_filter(image)
        if(rotateMode):
            image = image.rotate(180)
        savepath = os.path.join(mission_folder, imgObj["name"])
        image.save(savepath)
    except Exception as e:
        print(f'Failed to post process: {e}')
        
def add_timestamp(img):
    font = ImageFont.truetype("arial.ttf", 20)
    draw = ImageDraw.Draw(img)
    # Get current time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add timestamp to the upper left corner of the image
    draw.text((0,0), timestamp, (255,255,255), font=font)
    # Return the image
    return img

def latestImage(db:Database):
    #files = os.listdir(folder)
    #image_files = [f for f in files if f.endswith('.jpg') or f.endswith('.png')]
    #image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
    #latest_image_path = os.path.join(folder_path, image_files[0])
    #image_name = image_files[0]
    #return Image.open(latest_image_path), image_name
    data = db.data
    sorted_data = sorted(data, key=lambda x: x['timestamp'], reverse=True)
    latest_obj = sorted_data[0]
    latest_path = latest_obj["path"]
    return Image.open(latest_path), latest_obj

        
#def rotate_existing_image():
#    try:
#        image, jsonObj = latestImage(mission_db)
#        rotated=image.rotate(180)
#        #Will overwrite the image
#        #savepath= os.path.join(mission_folder, jsonObj["name"])
#        rotated.save(jsonObj["path"])
#
#    except Exception as e:
#        print(f'Failed to rotate image: {e}')

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

def operateCam (command:str):
    global grayScale, filterMode, rotateMode
    print(f'Executing {command}: ')
    if command == "A1":
        #turns camera right 60 degrees
        print("Turn camera right 60 deg")
        talking_heads.talk(4, -60) #case 4 microstepper gives value to rotate
        sleep(3)
    elif command == "B2":
        #turns camera left 60 degrees
        print("Turn camera left 60 deg")
        talking_heads.talk(4, 60) #case 4 microstepper, pass rotation value
        sleep(3)
    elif command == "C3":
        print("Taking photo")
        TakePhoto()
        post_process()
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
        print("Rotate FOLLOWING image by 180 degrees")
        if(rotateMode):
            rotateMode = False
        else:
            rotateMode = True
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