from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def add_timestamp(img):
    font = ImageFont.truetype("NotoSans-Regular.ttf", 20)
    draw = ImageDraw.Draw(img)
    # Get current time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((0,0), timestamp, (255,255,255), font=font)
    plt.subplot(1,2,1)
    plt.title("white text")
    # Add timestamp to the upper right corner of the image
    # Return the image
    return img

img = Image.open("Dice.png")
add_timestamp(img)
img.show()
ptl.imshow(img)