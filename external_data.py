from tkinter import *
import pathlib  # pip install pathlib
import json
from PIL import Image, ImageTk  # pip install pillow

PATH = str(pathlib.Path(__file__).parent.resolve())+'/'

class Data:
    def __init__(self):
        with open(PATH+'data/data.json') as json_file:
            self.json_data = json.load(json_file)
  
        self.image_data, self.small_image_data = [], []
        placeholder = (Image.open(PATH+'imgs/placeholder.png'))
        placeholdertk = ImageTk.PhotoImage(placeholder)
        placeholder_normal_size = ImageTk.PhotoImage(placeholder.resize((self.aspect_ratio(placeholdertk, 200, 200)), Image.ANTIALIAS))
        placeholder_small_size = ImageTk.PhotoImage(placeholder.resize((self.aspect_ratio(placeholdertk)), Image.ANTIALIAS))
        
        for entry in self.json_data:
            try:
                image = (Image.open(PATH+'imgs/'+entry['img']))
                imagetk = ImageTk.PhotoImage(image)
                pic = ImageTk.PhotoImage(image.resize((self.aspect_ratio(imagetk, 200, 200)), Image.ANTIALIAS))
                small_pic = ImageTk.PhotoImage(image.resize((self.aspect_ratio(imagetk)), Image.ANTIALIAS))
            except:
                pic = placeholder_normal_size
                small_pic = placeholder_small_size
                
            self.image_data.append({'img_name': entry['img'],'img_file': pic})
            self.small_image_data.append({'img_name': entry['img'],'img_file': small_pic})

    def aspect_ratio(self, image, desired_width=120, desired_height=100):   # keep images at their original aspect ratio
        try:
            x = image.width()
            y = image.height()
        except:
            print('ERROR: could not determine aspect ratio - invalid image')    # most likely inputted non tkimage
            return(desired_width, desired_height)
        
        x_percent = desired_width / x   # finds how much % the desired width/height is relative to actual image width/height
        y_percent = desired_height / y
        
        if x_percent < y_percent:   # image is wide
            width = round(x_percent*x)
            height = round(x_percent*y)
            return(int(width), int(height))
        elif y_percent < x_percent: # image is tall
            width = round(y_percent*x)
            height = round(y_percent*y)
            return(int(width), int(height))
        else:   # image is a square
            width = round(x_percent*x)
            height = round(y_percent*y)
            return(int(width), int(height))