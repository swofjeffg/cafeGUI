import external_data
import states
from tkinter import *

class App:
    def __init__(self, root):
        data = external_data.Data()
        self.menu = data.json_data
        self.images = data.image_data
        self.small_images = data.small_image_data
        self.order = []

        self.unique_categories = []
        filter_list = []
        for entry in self.menu:
            if entry['category'] not in filter_list:
                self.unique_categories.append(entry['category'])
                filter_list.append(entry['category'])

        # setting up all master state to be ready for other states
        master_state = states.Master(root, self.small_images[len(self.small_images)-1]['img_file'])
        self.navigation_buttons = master_state.get_buttons()
        self.state_frame = master_state.get_frame()

        # each state is an object
        self.start_state = states.Start_State(self.state_frame, [self.state_picker, self.clear_order])
        self.menu_state = states.Menu_State(self.state_frame, self.unique_categories, self.menu, self.images, self.small_images, self.order, [self.state_picker, self.update_order])
        self.checkout_state = states.Checkout_State(self.state_frame, self.order, self.small_images, [self.checkout_payment, self.update_order])

        # initial state
        self.state_picker(0)

    def state_picker(self, target):
        if self.state_frame.winfo_children():   # get rid of anything side the state view when chaning states
            for child in self.state_frame.winfo_children():
                child.destroy()
        
        if target == 0:
            self.start_state.widgets()
            self.navigation_buttons[0].config(text = 'Food\nMenu', command=lambda:self.state_picker(1))
            self.navigation_buttons[1].config(text = 'View\nOrder', command=lambda:self.state_picker(2))
        if target == 1:
            self.menu_state.widgets()
            self.navigation_buttons[0].config(text = 'Main\nMenu', command=lambda:self.state_picker(0))
            self.navigation_buttons[1].config(text = 'View\nOrder', command=lambda:self.state_picker(2))
        if target == 2:
            self.checkout_state.widgets()
            self.navigation_buttons[0].config(text = 'Main\nMenu', command=lambda:self.state_picker(0))
            self.navigation_buttons[1].config(text = 'Food\nMenu', command=lambda:self.state_picker(1))
    
    def clear_order(self):
        self.order = []
    
    def update_order(self, item, added, target_state):
        if added:
            for entry in self.menu:
                if item == entry['name']:
                    self.order.append(entry)
        else:
            if len(self.order) == 0:
                pass
            else:
                for index, entry in enumerate(self.order):
                    if item == entry['name']:
                        self.order.pop(index)
                        break   # we don't wanna remove everything with the same name
        self.state_picker(target_state)
    
    def checkout_payment(self):
        print(self.order)

if __name__ == '__main__':
    root = Tk()
    root.title('Cafe Interferance')
    App(root)
    root.maxsize(700, 1000)
    root.minsize(700, 1000)
    root.mainloop()