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
        placeholder_normal_size = ImageTk.PhotoImage(placeholder.resize(
            (self.aspect_ratio(placeholdertk, 200, 200)), Image.ANTIALIAS))
        placeholder_small_size = ImageTk.PhotoImage(placeholder.resize(
            (self.aspect_ratio(placeholdertk)), Image.ANTIALIAS))

        for entry in self.json_data:
            try:
                image = (Image.open(PATH+'imgs/'+entry['img']))
                imagetk = ImageTk.PhotoImage(image)
                pic = ImageTk.PhotoImage(image.resize(
                    (self.aspect_ratio(imagetk, 200, 200)), Image.ANTIALIAS))
                small_pic = ImageTk.PhotoImage(image.resize(
                    (self.aspect_ratio(imagetk)), Image.ANTIALIAS))
            except:
                pic = placeholder_normal_size
                small_pic = placeholder_small_size

            self.image_data.append({'img_name': entry['img'], 'img_file': pic})
            self.small_image_data.append(
                {'img_name': entry['img'], 'img_file': small_pic})

    # keep images at their original aspect ratio
    def aspect_ratio(self, image, desired_width=120, desired_height=100):
        try:
            x = image.width()
            y = image.height()
        except:
            # most likely inputted non tkimage
            print('ERROR: could not determine aspect ratio - invalid image')
            return(desired_width, desired_height)

        # finds how much % the desired width/height is relative to actual image width/height
        x_percent = desired_width / x
        y_percent = desired_height / y

        if x_percent < y_percent:   # image is wide
            width = round(x_percent*x)
            height = round(x_percent*y)
            return(int(width), int(height))
        elif y_percent < x_percent:  # image is tall
            width = round(y_percent*x)
            height = round(y_percent*y)
            return(int(width), int(height))
        else:   # image is a square
            width = round(x_percent*x)
            height = round(y_percent*y)
            return(int(width), int(height))

    def write_orders(self, order_info):
        order_num = order_info[0]
        order_price = order_info[1]
        payment_method = order_info[2]
        order = order_info[3]
        change = order_info[4]
        filtered_order = []

        for dict in order:
            counter = 1
            if dict not in filtered_order:
                filtered_order.append(dict)
            else:
                for d in filtered_order:
                    if d['name'] == dict['name']:
                        counter += 1
                        d['name'] = f"{str(counter)} {d['name']}"

        with open(PATH+'data/orders.txt', 'a') as order_file:   # needs to be readable
            order_file.write(
                f'Order number: No.{order_num}\nOrder price: ${order_price}\nPayment method: {payment_method.capitalize()}\n')

            if change != 0:
                order_file.write(f'!!! Change: ${change} !!!\n')
            order_file.write('Items ordered:\n---\n')
            for dict in filtered_order:
                for item in dict:
                    if item != 'img':
                        if item == 'price':
                            order_file.write(
                                f'{item.capitalize()}: $'+str(dict[item]))
                            order_file.write('\n')
                        else:
                            order_file.write(
                                f'{item.capitalize()}: '+str(dict[item]))
                            order_file.write('\n')
                order_file.write('\n')
            order_file.write('---\n\n\n')
