import external_data
import states
from tkinter import *

class App:
    def __init__(self, root):
        self.root = root
        data = external_data.Data()
        self.menu = data.json_data
        self.images = data.image_data
        self.small_images = data.small_image_data
        self.order = []
        self.total_price = 0

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

        # initial state
        self.state_manager()
        self.state_picker(0)
    
    def state_manager(self):
        self.start_state = states.Start_State(self.state_frame, [self.state_picker, self.clear_order])
        self.menu_state = states.Menu_State(self.state_frame, self.unique_categories, self.menu, self.images, self.small_images, self.order, [self.state_picker, self.update_order])
        self.checkout_state = states.Checkout_State(self.state_frame, self.order, self.small_images, [self.checkout_payment, self.update_order, self.reliable_round])
        self.popup = states.PopUp(self.restart, self.reliable_round)

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
            self.checkout_state.widgets(self.total_price)
            self.navigation_buttons[0].config(text = 'Main\nMenu', command=lambda:self.state_picker(0))
            self.navigation_buttons[1].config(text = 'Food\nMenu', command=lambda:self.state_picker(1))
    
    def clear_order(self):
        self.order = []
    
    def update_order(self, item, added, target_state):
        if added:
            for entry in self.menu:
                if item == entry['name']:
                    self.order.append(entry)
                    self.total_price += entry['price']
        else:
            if len(self.order) == 0:
                self.total_price = 0.00
                pass
            else:
                for index, entry in enumerate(self.order):
                    if item == entry['name']:
                        self.order.pop(index)
                        self.total_price -= entry['price']
                        break   # we don't wanna remove everything with the same name
        self.state_picker(target_state)
    
    def reliable_round(self, value):
        try:
            values = str(value).split('.')
            try:
                if int(values[1]) > 2:
                    values[1] = values[1][:2]
            except:
                values[1] = values[1][:2]
            return(float('.'.join(values)))
        except:
            return(value)   # value doesn't have a decimal
    
    def checkout_payment(self, order_num):
        self.popup.popup(self.order, order_num, self.total_price, self.root)
    
    def restart(self):
        self.clear_order()
        self.state_picker(0)
        self.state_manager()

if __name__ == '__main__':
    root = Tk()
    root.title('Cafe Interferance')
    App(root)
    root.maxsize(700, 1000)
    root.minsize(700, 1000)
    root.mainloop()