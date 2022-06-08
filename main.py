# Cafe GUI for practise project
from tkinter import *
import pathlib  # pip install pathlib
import json

PATH = str(pathlib.Path(__file__).parent.resolve())+'/'

class App:
    def __init__(self, parent):
        self.parent = parent
        external_data = External_data_manager()
        
        self.menu = external_data.json_data
        self.image_data = external_data.image_data
        
        self.widgets()
    
    def widgets(self):
        master_frame = Frame(self.parent)
        master_frame.place(relx=.5, rely=.5, anchor=CENTER)
        
        test = Label(master_frame, image = self.image_data[0])
        test.image = self.image_data[0]
        test.pack()
        
        self.nav_frame = Frame(master_frame)
        self.nav_frame.pack()
        
        self.state_frame = Frame(master_frame)
        self.state_frame.pack()
    
    def initial_state(self):
        pass
    
    def menu(self):
        pass
    
    def final_state(self):
        pass

    def state_picker(self, target_state = 0):
        if self.state_frame.winfo_children():
            for child in self.state_frame.winfo_children():
                child.destroy()
        
        if target_state == 0:
            self.initial_state()
        if target_state == 1:
            self.menu()
        if target_state == 2:
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
    App(root)
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()