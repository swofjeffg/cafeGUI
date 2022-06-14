# Cafe GUI for practise project
from tkinter import *
import pathlib  # pip install pathlib
import json
import customtkinter    # pip install customtkinter
from PIL import Image, ImageTk  # pip install pillow

PATH = str(pathlib.Path(__file__).parent.resolve())+'/'

DARK_CREAM = '#F2DDC3'
CREAM = '#FFFFF0'
BROWN = '#A79280'

class App:
    def __init__(self, parent):
        self.parent = parent
        external_data = External_data_manager()
        
        self.menu = external_data.json_data
        self.image_data = external_data.image_data
        self.small_image_data = external_data.small_image_data
        self.logo = ImageTk.PhotoImage(Image.open(PATH+'imgs/placeholder.png').resize((120,100), Image.ANTIALIAS))
        
        self.categories = []
        filter_list = []
        for entry in self.menu:
            if entry['category'] not in filter_list:
                self.categories.append({'category': entry['category'], 'img': entry['img']})
                filter_list.append(entry['category'])
        self.categories
        self.category = self.categories[0]['category']
        
        self.order = []
        
        self.widgets()
        self.state_picker()
    
    def widgets(self):
        master_frame = Frame(self.parent, background=CREAM)
        master_frame.pack(fill='both', expand=True)
        
        self.nav_frame = customtkinter.CTkFrame(master_frame, fg_color=DARK_CREAM, corner_radius=0)
        
        logo = Label(self.nav_frame, image=self.logo, background=CREAM)
        logo.img = self.logo
        logo.pack(side=LEFT, padx=10, pady=10)
        
        customtkinter.CTkLabel(self.nav_frame, text='Ormiston Cafe', bg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 33)).pack(side=LEFT)
        
        self.button1 = customtkinter.CTkButton(self.nav_frame, fg_color=CREAM, text_color=BROWN, text_font=('Arial', 25), hover=False, corner_radius=30, command=lambda:self.state_picker(1))
        self.button2 = customtkinter.CTkButton(self.nav_frame, fg_color=CREAM, text_color=BROWN, text_font=('Arial', 25), hover=False, corner_radius=30, command=lambda:self.state_picker(2))
        
        self.button2.pack(side=RIGHT, padx=10)
        self.button1.pack(side=RIGHT, padx=10)
        
        self.nav_frame.pack(side='top', fill='x')
        
        self.state_frame = Frame(master_frame, background=CREAM)
    
    def initial_state(self):
        root = self.state_frame
        
        button1 = customtkinter.CTkButton(root, text='Start your\norder', fg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 80), hover=False, corner_radius=70, border_width=5, border_color=BROWN, width=700, command=lambda:self.state_picker(1))
        button2 = customtkinter.CTkButton(root, text='Restart your\norder', fg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 80), hover=False, corner_radius=70, border_width=5, border_color=BROWN, width=700, command=lambda:self.clear_order())
        
        button1.pack(ipady=50, pady=30, padx=50)
        button2.pack(ipady=50, pady=30, padx=50)
        root.place(anchor='n', relx=.5, rely=.128, relheight=0.872, relwidth=1)
    
    def menu_state(self):
        root = self.state_frame
        
        categories_frame = Frame(root, background=CREAM, highlightbackground=BROWN, highlightthickness=2)
        for category in self.categories:
            catergory_name = category['category'].capitalize()
            border = Frame(categories_frame, background=CREAM, highlightbackground=BROWN, highlightthickness=1)
            frame = Frame(border, background=CREAM)
            for data in self.small_image_data:
                if data['img_name'] == category['img']:
                    image_data = data['img_file']
            button = Button(frame, image=image_data, width=120, height=100, borderwidth=0, background=CREAM, activebackground=CREAM, command=lambda i=category['category']:self.set_category(i))
            button.pack()
            Button(frame, text=catergory_name, fg=ORANGE_COLOUR, borderwidth=0, background=CREAM, activebackground=CREAM, activeforeground=ORANGE_COLOUR, command=lambda i=category['category']:self.set_category(i)).pack()
            border.pack(pady=10, padx=10)
        
        categories_frame.pack(side='left', fill='y')
        
        options_frame = Frame(root, background=CREAM, highlightbackground=BROWN, highlightthickness=2)
        
        x = y = 1
        for entry in self.menu:
            if entry['category'] == self.category:
                x += 1
                name, price = entry['name'], entry['price']
                frame = Frame(options_frame, background=CREAM, highlightbackground=BROWN, highlightthickness=1)
                frame.grid(column = x, row = y, pady=10, padx=10)
                for data in self.image_data:
                    if data['img_name'] == entry['img']:
                        image_data = data['img_file']
                image = Label(frame, image=image_data, width=350, height=200, background=CREAM)
                image.pack()
                try:
                    size = entry['size']
                    Label(frame, text=f'{name.capitalize()}({size}) for ${price}', fg=ORANGE_COLOUR, background=CREAM).pack()
                except KeyError:
                    Label(frame, text=f'{name.capitalize()} for ${price}', fg=ORANGE_COLOUR, background=CREAM).pack()
                if x == 3:
                    x = 1
                    y += 1
        options_frame.grid_columnconfigure(0, weight=1) # centering the grid within 'options_frame' horizontally
        options_frame.grid_columnconfigure(4, weight=1)
        
        options_frame.pack(fill='both', expand=True)
        
        root.place(anchor='n', relx=.5, rely=.128, relheight=0.872, relwidth=1)
    
    def final_state(self):
        root = self.state_frame
        
        root.place(anchor='n', relx=.5, rely=.128, relheight=0.872, relwidth=1)

    def state_picker(self, target_state = 0):
        if self.state_frame.winfo_children():
            for child in self.state_frame.winfo_children():
                child.destroy()
        
        if target_state == 0:
            self.button1.config(text = 'Food\nMenu', command=lambda:self.state_picker(1))
            self.button2.config(text = 'View\nOrder', command=lambda:self.state_picker(2))
            self.initial_state()
        if target_state == 1:
            self.button1.config(text = 'Main\nMenu', command=lambda:self.state_picker(0))
            self.button2.config(text = 'View\nOrder', command=lambda:self.state_picker(2))
            self.menu_state()
        if target_state == 2:
            self.button1.config(text = 'Main\nMenu', command=lambda:self.state_picker(0))
            self.button2.config(text = 'Food\nMenu', command=lambda:self.state_picker(1))
            self.final_state()
    
    def clear_order(self):
        self.order = []
        print('order cleared')
    
    def set_category(self, category):
        self.category = category
        self.state_picker(1)

class External_data_manager:
    def __init__(self):
        with open(PATH+'data/data.json') as json_file:
            self.json_data = json.load(json_file)
  
        self.image_data, self.small_image_data = [], []
        
        for entry in self.json_data:
            try:
                image = (Image.open(PATH+'imgs/'+entry['img']))
                imagetk = ImageTk.PhotoImage(image)
                pic = ImageTk.PhotoImage(image.resize((self.aspect_ratio(imagetk, 350, 200)), Image.ANTIALIAS))
                small_pic = ImageTk.PhotoImage(image.resize((self.aspect_ratio(imagetk)), Image.ANTIALIAS))
            except:
                image = (Image.open(PATH+'imgs/placeholder.png'))
                imagetk = ImageTk.PhotoImage(image)
                pic = ImageTk.PhotoImage(image.resize((self.aspect_ratio(imagetk, 350, 200)), Image.ANTIALIAS))
                small_pic = ImageTk.PhotoImage(image.resize((self.aspect_ratio(imagetk)), Image.ANTIALIAS))
                
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

if __name__ == '__main__':
    root = Tk()
    root.title('Cafe Interferance')
    root.maxsize(700, 1000)
    root.minsize(700, 1000)
    root.configure(background=BROWN)
    App(root)
    root.mainloop()