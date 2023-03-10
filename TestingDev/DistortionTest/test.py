from wand.image import Image

def distortion():
    with open('./og-pics/index.txt') as file:
        #Grabs the last character from the index.txt file
        imgNum = file.readlines()[-1]
    #Saves the image for distortion from its original location
    image = './og-pics/' + str(imgNum) + '.jpg'
    args = (0.2, 0.0, 0.0, 1.5)
    #Distorts image using a barrel distortion
    with Image(filename = image) as img:
        img.distort('barrel', args)
        img.save(filename = './Mission/' + str(imgNum) + '.jpg')