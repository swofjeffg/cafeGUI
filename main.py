# Cafe GUI for practise project
from tkinter import *
import pathlib
import csv

PATH = str(pathlib.Path(__file__).parent.resolve())+'/'

class App():
    def __init__(self, parent):
        self.parent = parent
        
        self.external_file = External_data_manager.text_file_manager()
        self.external_images = External_data_manager.image_manager()


class External_data_manager():
    def text_file_manager():
        data = []
        with open(PATH+'data/data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    
    def image_manager():
        images = []
        for image in PATH+'imgs/':
            PhotoImage(image)
        return images

if __name__ == '__main__':
    root = Tk()
    root.title('Cafe Interferance')
    App(root)
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()