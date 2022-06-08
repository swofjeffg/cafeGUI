# Cafe GUI for practise project
from tkinter import *
import pathlib  # pip install pathlib
import json

PATH = str(pathlib.Path(__file__).parent.resolve())+'/'
BACKGROUND_COLOUR = '#111111'
ORANGE_COLOUR = '#ffa500'

class App:
    def __init__(self, parent):
        self.parent = parent
        external_data = External_data_manager()
        
        self.menu = external_data.json_data
        self.image_data = external_data.image_data
        self.logo = PhotoImage(file=PATH+'imgs/placeholder.png')
        
        self.categories = []
        _ = []
        for entry in self.menu:
            if entry['category'] not in _:
                self.categories.append({'category': entry['category'], 'img': entry['img']})
                _.append(entry['category'])
        self.categories
        self.category = self.categories[0]['category']
        
        self.order = []
        
        self.widgets()
        self.state_picker()
    
    def widgets(self):
        master_frame = Frame(self.parent, background=BACKGROUND_COLOUR)
        master_frame.pack(fill='both', expand=True)
        
        self.nav_frame = Frame(master_frame, background=BACKGROUND_COLOUR, highlightbackground='#ffffff', highlightthickness=2)
        
        logo = Label(self.nav_frame, image=self.logo, background=BACKGROUND_COLOUR)
        logo.img = self.logo
        logo.pack(side=LEFT, padx=10, pady=10)
        
        Label(self.nav_frame, text='Ormiston Cafe', fg=ORANGE_COLOUR, font='Arial 50', background=BACKGROUND_COLOUR).pack(side=LEFT, padx=100)
        
        button_frame_1 = Frame(self.nav_frame, background=BACKGROUND_COLOUR, highlightbackground='#ffffff', highlightthickness=1)
        button_frame_2 = Frame(self.nav_frame, background=BACKGROUND_COLOUR, highlightbackground='#ffffff', highlightthickness=1)
        
        button_frame_2.pack(side=RIGHT, padx=10)
        button_frame_1.pack(side=RIGHT, padx=10)
        
        self.button1 = Button(button_frame_1, text='Food menu', fg=ORANGE_COLOUR, font='Arial 20', borderwidth=0, background=BACKGROUND_COLOUR, activebackground='#333333', activeforeground=ORANGE_COLOUR, command=lambda:self.state_picker(1))
        self.button2 = Button(button_frame_2, text='View order', fg=ORANGE_COLOUR, font='Arial 20', borderwidth=0, background=BACKGROUND_COLOUR, activebackground='#333333', activeforeground=ORANGE_COLOUR, command=lambda:self.state_picker(2))
        
        self.button1.pack()
        self.button2.pack()
        
        self.nav_frame.pack(side='top', fill='x')
        
        self.state_frame = Frame(master_frame, background=BACKGROUND_COLOUR)
    
    def initial_state(self):
        root = self.state_frame
        
        button_frame_1 = Frame(root, background=BACKGROUND_COLOUR, highlightbackground='#ffffff', highlightthickness=1)
        button_frame_2 = Frame(root, background=BACKGROUND_COLOUR, highlightbackground='#ffffff', highlightthickness=1)
        
        Button(button_frame_1, text='Click to start!', fg=ORANGE_COLOUR, font='Arial 100', borderwidth=0, background=BACKGROUND_COLOUR, activebackground='#333333', activeforeground=ORANGE_COLOUR, command=lambda:self.state_picker(1)).pack()
        Button(button_frame_2, text='Restart order', fg=ORANGE_COLOUR, font='Arial 100', borderwidth=0, background=BACKGROUND_COLOUR, activebackground='#333333', activeforeground=ORANGE_COLOUR, command=lambda:self.clear_order()).pack()
        
        button_frame_1.pack(pady=30)
        button_frame_2.pack(pady=30)
        
        root.place(anchor='n', relx=.5, rely=.128, relheight=0.872, relwidth=1)
    
    def menu_state(self):
        root = self.state_frame
        
        categories_frame = Frame(root, background=BACKGROUND_COLOUR, highlightbackground='#ffffff', highlightthickness=2)
        
        for category in self.categories:
            catergory_name = category['category'].capitalize()
            border = Frame(categories_frame, background=BACKGROUND_COLOUR, highlightbackground='#ffffff', highlightthickness=1)
            frame = Frame(border, background=BACKGROUND_COLOUR)
            for data in self.image_data:
                if data['img_name'] == category['img']:
                    image_data = data['img_file']
            image = Button(frame, image=image_data, borderwidth=0, background=BACKGROUND_COLOUR, activebackground=BACKGROUND_COLOUR, command=lambda i=category['category']:self.set_category(i))
            image.img = image_data
            image.pack()
            Button(frame, text=catergory_name, fg=ORANGE_COLOUR, borderwidth=0, background=BACKGROUND_COLOUR, activebackground=BACKGROUND_COLOUR, activeforeground=ORANGE_COLOUR, command=lambda i=category['category']:self.set_category(i)).pack()
            frame.pack(pady=5, padx=5)
            border.pack(pady=10, padx=10)
        
        categories_frame.pack(side='left', fill='y')
        
        options_frame = Frame(root, background=BACKGROUND_COLOUR, highlightbackground='#ffffff', highlightthickness=2)
        
        for entry in self.menu:
            if entry['category'] == self.category:
                t = entry['name']
                Label(options_frame, text=t).pack()
        
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
            self.button1.config(text = 'Food menu', command=lambda:self.state_picker(1))
            self.button2.config(text = 'View order', command=lambda:self.state_picker(2))
            self.initial_state()
        if target_state == 1:
            self.button1.config(text = 'Main menu', command=lambda:self.state_picker(0))
            self.button2.config(text = 'View order', command=lambda:self.state_picker(2))
            self.menu_state()
        if target_state == 2:
            self.button1.config(text = 'Main menu', command=lambda:self.state_picker(0))
            self.button2.config(text = 'Food menu', command=lambda:self.state_picker(1))
            self.final_state()
    
    def clear_order(self):
        self.order = []
    
    def set_category(self, category):
        self.category = category
        self.state_picker(1)

class External_data_manager:
    def __init__(self):
        with open(PATH+'data/data.json') as json_file:
            self.json_data = json.load(json_file)
  
        self.image_data = []
        for entry in self.json_data:
            try:
                pic = PhotoImage(file=PATH+'imgs/'+entry['img'])
            except:
                pic = PhotoImage(file=PATH+'imgs/placeholder.png')
            self.image_data.append({'img_name': entry['img'],'img_file': pic})

if __name__ == '__main__':
    root = Tk()
    root.title('Cafe Interferance')
    root.maxsize(1250, 1000)
    root.minsize(1250, 1000)
    root.configure(background=BACKGROUND_COLOUR)
    App(root)
    root.mainloop()