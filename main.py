# Cafe GUI for practise project
from tkinter import *
import pathlib

PATH = str(pathlib.Path(__file__).parent.resolve())+'/'

class App():
    def __init__(self, parent):
        self.parent = parent
        
        self.external_file = External_data_manager.text_file_manager
        self.external_images = External_data_manager.image_manager

class External_data_manager():
    def __init__(self):
        self.img_source = PATH+'imgs/'
        self.txt_soruce = PATH+'data/'
    
    def text_file_manager(self):
        data = []
        return data
    
    def image_manager(self):
        images = []
        for image in self.source:
            PhotoImage(image)
        return images

if __name__ == '__main__':
    root = Tk()
    root.title('Cafe Interferance')
    App(root)
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()