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
        
        self.widgets()
        self.state_picker()
    
    def widgets(self):
        master_frame = Frame(self.parent, background=BACKGROUND_COLOUR)
        master_frame.pack(fill='both')
        
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
        
        self.nav_frame.pack(side=TOP, expand=True, fill='x')
        
        self.state_frame = Frame(master_frame, background=BACKGROUND_COLOUR)
        self.state_frame.pack()
    
    def initial_state(self):
        root = self.state_frame
    
    def menu_state(self):
        root = self.state_frame
    
    def final_state(self):
        root = self.state_frame

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
            self.image_data.append(pic)

if __name__ == '__main__':
    root = Tk()
    root.title('Cafe Interferance')
    root.maxsize(1250, 800)
    root.minsize(1250, 800)
    root.configure(background=BACKGROUND_COLOUR)
    App(root)
    root.mainloop()