from cgitb import small
from tkinter import *
import customtkinter    # pip install customtkinter

DARK_CREAM = '#F2DDC3'
CREAM = '#FFFFF0'
BROWN = '#A79280'

class Master:
    def __init__(self, root, logo):
        self.root = root
        self.logo = logo
        self.widgets()
    
    def widgets(self):
        master_frame = Frame(self.root, background=CREAM)
        master_frame.pack(fill='both', expand=1)

        nav_frame = Frame(master_frame, background=DARK_CREAM)

        logo = Label(nav_frame, image=self.logo, background=CREAM)
        logo.img = self.logo
        logo.pack(side=LEFT, padx=10, pady=10)

        customtkinter.CTkLabel(nav_frame, text='Ormiston Cafe', bg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 33)).pack(side=LEFT)

        self.button1 = customtkinter.CTkButton(nav_frame, fg_color=CREAM, text_color=BROWN, text_font=('Arial', 25), hover=False, corner_radius=30)
        self.button2 = customtkinter.CTkButton(nav_frame, fg_color=CREAM, text_color=BROWN, text_font=('Arial', 25), hover=False, corner_radius=30)

        self.button2.pack(side=RIGHT, padx=10)
        self.button1.pack(side=RIGHT, padx=10)

        nav_frame.pack(side='top', fill='x')

        self.state_frame = Frame(master_frame, background=CREAM)

    def get_frame(self):
        return(self.state_frame)
    
    def get_buttons(self):
        return([self.button1, self.button2])

class Start_State:
    def __init__(self, root, functions):
        self.root = root
        self.change_state = functions[0]
        self.clear_order = functions[1]
    
    def widgets(self):
        button1 = customtkinter.CTkButton(self.root, text='Start your\norder', fg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 80), hover=False, corner_radius=70, border_width=5, border_color=BROWN, width=700, command=lambda i=1:self.change_state(i))
        button2 = customtkinter.CTkButton(self.root, text='Restart your\norder', fg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 80), hover=False, corner_radius=70, border_width=5, border_color=BROWN, width=700, command=lambda:self.clear_order())
        
        button1.pack(ipady=50, pady=30, padx=50)
        button2.pack(ipady=50, pady=30, padx=50)
        self.root.pack(anchor='n')




class Menu_State:
    def __init__(self, root, categories, menu, images, small_images, functions):
        self.root = root
        self.categories = categories
        self.menu = menu
        self.images = images
        self.small_images = small_images
        self.change_state = functions[0]
        self.update_order = functions[1]
        self.category = categories[0]

    def widgets(self):
        categories_frame = Frame(self.root, background=BROWN, highlightbackground=BROWN, highlightthickness=2)
        for category in self.categories:
            catergory_name = category.capitalize()
            customtkinter.CTkButton(categories_frame, text=catergory_name, fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, corner_radius=27, border_width=5, border_color=BROWN, height=50, width=(self.root.winfo_width()/len(self.categories)), command=lambda i=category:self.set_category(i)).pack(side='left')
        
        categories_frame.pack(side='top', fill='x')
        
        options_frame = Frame(self.root, background=CREAM)

        scrollable_frame = Frame(options_frame, background=CREAM)
        scrollable_frame.pack(fill='both', expand=1)

        scrollable_canvas = Canvas(scrollable_frame, background=CREAM, borderwidth=0, highlightbackground=CREAM)
        scrollable_canvas.pack(side='left', fill='both', expand=1)

        scrollbar = Scrollbar(scrollable_frame, orient=VERTICAL, command=scrollable_canvas.yview)
        scrollbar.pack(side='right', fill='y')

        scrollable_canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_canvas.bind('<Configure>', lambda e: scrollable_canvas.configure(scrollregion = scrollable_canvas.bbox('all')))

        second_frame = Frame(scrollable_canvas, background=CREAM)

        scrollable_canvas.create_window(((self.root.winfo_width()/2),0), window=second_frame, anchor='n', width=self.root.winfo_width())
        
        for entry in self.menu:
            if entry['category'] == self.category:
                name, price = entry['name'], entry['price']
                frame = customtkinter.CTkFrame(second_frame, fg_color=DARK_CREAM, corner_radius=27, border_width=3, border_color=BROWN)
                frame.pack(padx=(self.root.winfo_width()*0.1), pady=20, ipady=20, fill='x', expand='true')    # width option is broken above
                for data in self.images:
                    if data['img_name'] == entry['img']:
                        image_data = data['img_file']
                image = Label(frame, image=image_data, width=200, height=200, background=DARK_CREAM)
                image.pack(padx=5, pady=5, side='left')
                try:
                    size = entry['size']
                    Label(frame, text=f'{name.capitalize()}', fg=BROWN, background=DARK_CREAM, font=('Arial', 40), anchor='w').pack(fill='x', padx=10, pady=10)
                    Label(frame, text=f'{size}', fg=BROWN, background=DARK_CREAM, font=('Arial', 15), anchor='w').pack(fill='x', padx=10)
                    Label(frame, text=f'${price}', fg=BROWN, background=DARK_CREAM, font=('Arial', 20), anchor='w').pack(fill='x', padx=10)
                except KeyError:
                    Label(frame, text=f'{name.capitalize()}', fg=BROWN, background=DARK_CREAM, font=('Arial', 40), anchor='w').pack(fill='x', padx=10, pady=10)
                    Label(frame, text=f'${price}', fg=BROWN, background=DARK_CREAM, font=('Arial', 20), anchor='w').pack(fill='x', padx=10)
                buttons_frame = Frame(frame, background=DARK_CREAM)
                buttons_frame.pack(side='bottom', pady=7)
                customtkinter.CTkButton(buttons_frame, text='Add', fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, corner_radius=27, height=50, width=(self.root.winfo_width()/len(self.categories)), command=lambda i=name:self.update_order(i, True)).pack(side='left', padx=10)
                customtkinter.CTkButton(buttons_frame, text='Remove', fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, corner_radius=27, height=50, width=(self.root.winfo_width()/len(self.categories)), command=lambda i=name:self.update_order(i, False)).pack(side='left', padx=10)
        options_frame.pack(fill='both', expand=1)
        
        self.root.pack(anchor='n', fill='both', expand='true')
    
    def set_category(self, category):
        self.category = category
        self.change_state(1)




class Checkout_State:
    def __init__(self, root, order):
        pass