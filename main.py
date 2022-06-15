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
    def __init__(self, parent, data):
        self.parent = parent
        external_data = data
        
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
        master_frame.pack(fill='both', expand=1)
        
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
        root.pack(anchor='n')
    
    def menu_state(self):
        root = self.state_frame
        
        categories_frame = Frame(root, background=BROWN, highlightbackground=BROWN, highlightthickness=2)
        for category in self.categories:
            catergory_name = category['category'].capitalize()
            for data in self.small_image_data:
                if data['img_name'] == category['img']:
                    image_data = data['img_file']
            customtkinter.CTkButton(categories_frame, text=catergory_name, fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, corner_radius=27, border_width=5, border_color=BROWN, height=50, width=(self.parent.winfo_width()/len(self.categories)), command=lambda i=category['category']:self.set_category(i)).pack(side='left')
        
        categories_frame.pack(side='top', fill='x')
        
        options_frame = Frame(root, background=CREAM)

        scrollable_frame = Frame(options_frame, background=CREAM)
        scrollable_frame.pack(fill='both', expand=1)

        scrollable_canvas = Canvas(scrollable_frame, background=CREAM, borderwidth=0, highlightbackground=CREAM)
        scrollable_canvas.pack(side='left', fill='both', expand=1)

        scrollbar = Scrollbar(scrollable_frame, orient=VERTICAL, command=scrollable_canvas.yview)
        scrollbar.pack(side='right', fill='y')

        scrollable_canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_canvas.bind('<Configure>', lambda e: scrollable_canvas.configure(scrollregion = scrollable_canvas.bbox('all')))

        second_frame = Frame(scrollable_canvas, background=CREAM)

        scrollable_canvas.create_window(((self.parent.winfo_width()/2),0), window=second_frame, anchor='n', width=self.parent.winfo_width())
        
        for entry in self.menu:
            if entry['category'] == self.category:
                name, price = entry['name'], entry['price']
                frame = customtkinter.CTkFrame(second_frame, fg_color=DARK_CREAM, corner_radius=27, border_width=3, border_color=BROWN)
                frame.pack(padx=(self.parent.winfo_width()*0.1), pady=20, ipady=20, fill='x', expand='true')    # width option is broken above
                frame.rowconfigure(0, weight=1) # vertically center contents of frame
                frame.rowconfigure(4, weight=1)
                frame.columnconfigure(2, weight=1)  # push contents to left
                for data in self.image_data:
                    if data['img_name'] == entry['img']:
                        image_data = data['img_file']
                image = Label(frame, image=image_data, width=200, height=200, background=DARK_CREAM)
                image.grid(row=1, column=1, rowspan=3, padx=5)
                try:
                    size = entry['size']
                    Label(frame, text=f'{name.capitalize()}({size})', fg=BROWN, background=DARK_CREAM, font=('Arial', 40)).grid(column=2, row=1)
                except KeyError:
                    Label(frame, text=f'{name.capitalize()}', fg=BROWN, background=DARK_CREAM, font=('Arial', 40)).grid(column=2, row=1)
                buttons_frame = Frame(frame, background=DARK_CREAM)
                buttons_frame.grid(column=2, columnspan=2, row=3)
                customtkinter.CTkButton(buttons_frame, text='Add', fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, corner_radius=27, height=50, width=(self.parent.winfo_width()/len(self.categories)), command=lambda i=name:self.update_order(i, True)).pack(side='left', padx=10)
                customtkinter.CTkButton(buttons_frame, text='Remove', fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, corner_radius=27, height=50, width=(self.parent.winfo_width()/len(self.categories)), command=lambda i=name:self.update_order(i, False)).pack(side='left', padx=10)
        options_frame.pack(fill='both', expand=1)
        
        root.pack(anchor='n', fill='both', expand='true')
    
    def final_state(self):
        root = self.state_frame
        
        root.pack(anchor='n', fill='both', expand='true')

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
    
    def update_order(self, item_name, being_added):
        if being_added:
            for entry in self.menu:
                if item_name == entry['name']:
                    self.order.append(entry)
        else:
            if len(self.order) == 0:
                pass
            else:
                for index, entry in enumerate(self.order):
                    if item_name == entry['name']:
                        self.order.pop(index)
                        break   # we don't wanna remove everything with the same name
        print(self.order)
    
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
    App(root, External_data_manager())
    root.mainloop()