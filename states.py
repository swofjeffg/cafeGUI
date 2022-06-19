from multiprocessing.sharedctypes import Value
from posixpath import split
from random import randint
from tkinter import *
from unicodedata import decimal
import customtkinter
from numpy import diff, var    # pip install customtkinter

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
    def __init__(self, root, categories, menu, images, small_images, order, functions):
        self.root = root
        self.categories = categories
        self.menu = menu
        self.images = images
        self.small_images = small_images
        self.order = order
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

        internal_frame = Frame(scrollable_canvas, background=CREAM)

        scrollable_canvas.create_window(((self.root.winfo_width()/2),0), window=internal_frame, anchor='n', width=self.root.winfo_width())
        
        for entry in self.menu:
            if entry['category'] == self.category:
                count = 0
                name, price = entry['name'], entry['price']
                
                frame = customtkinter.CTkFrame(internal_frame, fg_color=DARK_CREAM, corner_radius=27, border_width=3, border_color=BROWN)
                frame.pack(padx=(self.root.winfo_width()*0.1), pady=20, ipady=20, fill='x', expand='true')    # width option is broken above

                for data in self.images:
                    if data['img_name'] == entry['img']:
                        image_data = data['img_file']

                image = Label(frame, image=image_data, width=200, height=200, background=DARK_CREAM)
                image.pack(padx=5, pady=5, side='left')

                if entry in self.order:
                    for item in self.order:
                        if item['name'] == entry['name']:
                            count += 1
                
                label_frame = Frame(frame, background=DARK_CREAM)

                try:
                    size = entry['size']
                    Label(label_frame, text=f'{name.capitalize()}', fg=BROWN, background=DARK_CREAM, font=('Arial', 40), anchor='w').pack(fill='x')
                    Label(label_frame, text=f'({size})', fg=BROWN, background=DARK_CREAM, font=('Arial', 15), anchor='w').pack(fill='x')
                    Label(label_frame, text=f'${price}', fg=BROWN, background=DARK_CREAM, font=('Arial', 15), anchor='w').pack(fill='x')
                except KeyError:
                    Label(label_frame, text=f'{name.capitalize()}', fg=BROWN, background=DARK_CREAM, font=('Arial', 40), anchor='w').pack(fill='x')
                    Label(label_frame, text=f'${price}', fg=BROWN, background=DARK_CREAM, font=('Arial', 15), anchor='w').pack(fill='x')
                
                buttons_frame = Frame(label_frame, background=DARK_CREAM)

                if count != 0:
                    Label(label_frame, text=f'({count} added)', fg=BROWN, background=DARK_CREAM, font=('Arial', 15), anchor='e').pack(fill='x')
                    customtkinter.CTkButton(buttons_frame, text='Remove', fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, corner_radius=27, height=50, width=(self.root.winfo_width()/len(self.categories)), command=lambda i=name:self.update_order(i, False, 1)).pack(side='right', padx=10)
                    customtkinter.CTkButton(buttons_frame, text='Add', fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, corner_radius=27, height=50, width=(self.root.winfo_width()/len(self.categories)), command=lambda i=name:self.update_order(i, True, 1)).pack(side='right', padx=10)
                else:
                    customtkinter.CTkButton(buttons_frame, text='Add', fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, corner_radius=27, height=50, width=(self.root.winfo_width()/len(self.categories)), command=lambda i=name:self.update_order(i, True, 1)).pack(side='right', padx=10)
                
                label_frame.pack(pady=10, padx=10, fill='both', expand=1)

                buttons_frame.pack(side='bottom', fill='x', padx=10, pady=10)
                
        options_frame.pack(fill='both', expand=1)
        
        self.root.pack(anchor='n', fill='both', expand='true')
    
    def set_category(self, category):
        self.category = category
        self.change_state(1)




class Checkout_State:
    def __init__(self, root, order, images, functions):
        self.root = root
        self.order = order
        self.images = images
        self.checkout = functions[0]
        self.update_order = functions[1]
        self.round = functions[2]
    
    def widgets(self, total_price):  # so many magic numbers :(
        checkout_frame = customtkinter.CTkFrame(self.root, fg_color=DARK_CREAM, border_color=BROWN, border_width=5, corner_radius=100, width=self.root.winfo_width()*.8, height=self.root.winfo_height()*.8)

        customtkinter.CTkFrame(checkout_frame, fg_color=BROWN, height=6, corner_radius=0).place(relx=.5, rely=.17, anchor=CENTER, relwidth=1)
        customtkinter.CTkFrame(checkout_frame, fg_color=BROWN, height=6, corner_radius=0).place(relx=.5, rely=.83, anchor=CENTER, relwidth=1)
        Label(checkout_frame, text='Selected Items', font=('Arial', 62), background=DARK_CREAM, foreground=BROWN).place(relx=.5, rely=.085, anchor=CENTER)

        checkout_canvas = Canvas(checkout_frame, background=DARK_CREAM, highlightthickness=0)
        checkout_canvas.place(anchor='n', rely=.175, relx=.493, relheight=(1-(.175*2)), relwidth=.97)

        checkout_scroll = Scrollbar(checkout_frame, orient=VERTICAL, command=checkout_canvas.yview)
        checkout_scroll.place(anchor='n', rely=.175, relx=.977, relheight=(1-(.175*2)))

        checkout_canvas.configure(yscrollcommand=checkout_scroll.set)
        checkout_canvas.bind('<Configure>', lambda e: checkout_canvas.configure(scrollregion = checkout_canvas.bbox('all')))

        internal_frame = Frame(checkout_canvas, background=DARK_CREAM)

        checkout_canvas.create_window(((self.root.winfo_width()/2),0), window=internal_frame, anchor='n', width=self.root.winfo_width()*.8)

        for entry in self.order:
                name, price = entry['name'], entry['price']
                
                frame = customtkinter.CTkFrame(internal_frame, fg_color=CREAM, corner_radius=27, border_width=3, border_color=BROWN)
                frame.pack(padx=(self.root.winfo_width()*0.05), pady=20, ipady=20, fill='x', expand='true')    # width option is broken above'

                label_frame = Frame(frame, background=CREAM)

                for data in self.images:
                    if data['img_name'] == entry['img']:
                        image_data = data['img_file']

                image = Label(frame, image=image_data, width=150, height=150, background=CREAM)
                image.pack(padx=5, pady=5, side='left')

                try:
                    size = entry['size']
                    Label(label_frame, text=f'{name.capitalize()}', fg=BROWN, background=CREAM, font=('Arial', 30), anchor='w').pack(fill='x')
                    Label(label_frame, text=f'({size})', fg=BROWN, background=CREAM, font=('Arial', 15), anchor='w').pack(fill='x')
                    Label(label_frame, text=f'${price}', fg=BROWN, background=CREAM, font=('Arial', 15), anchor='w').pack(fill='x')
                except KeyError:
                    Label(label_frame, text=f'{name.capitalize()}', fg=BROWN, background=CREAM, font=('Arial', 30), anchor='w').pack(fill='x')
                    Label(label_frame, text=f'${price}', fg=BROWN, background=CREAM, font=('Arial', 15), anchor='w').pack(fill='x')
                
                buttons_frame = Frame(label_frame, background=CREAM)
                customtkinter.CTkButton(buttons_frame, text='Remove', fg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, corner_radius=27, height=50, width=50, command=lambda i=name:self.update_order(i, False, 2)).pack(side='right', padx=10)
                
                label_frame.pack(pady=10, padx=10, fill='both', expand=1)
                buttons_frame.pack(side='bottom', fill='x', padx=10, pady=10)
        
        customtkinter.CTkLabel(checkout_frame, text=f'Total price:\n${self.round(total_price)}', fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), corner_radius=20).place(relheight=.12, relx=.22, rely=.9, anchor=CENTER)
        if self.order:
            customtkinter.CTkButton(checkout_frame, text=f'Confirm\norder', fg_color=CREAM, text_color=BROWN, text_font=('Arial', 20), corner_radius=20, hover=False, command=lambda:self.checkout(randint(000,999))).place(relheight=.12, relx=.78, rely=.9, anchor=CENTER)

        checkout_frame.place(relx=.5, rely=.5, anchor=CENTER)




class PopUp:
    def __init__(self, restart_function, reliable_round):
        self.restart_function = restart_function
        self.cash = StringVar()
        self.card_num = StringVar()
        self.card_csv = StringVar()
        self.paddings = {'padx': 5, 'pady': 5}
        self.round = reliable_round

        self.old = []

    def popup(self, order, order_num, order_price, root):
        self.popup_root = Toplevel(root)
        self.order = order
        self.order_num = order_num
        self.order_price = order_price

        self.cancel_button = customtkinter.CTkButton(self.popup_root, fg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False)
        self.cancel_button.pack(side='bottom', pady=20)

        self.popup_root.title('Confirm order')
        self.popup_root.geometry("350x350")
        self.popup_root.config(background=CREAM)

        self.master_frame = Frame(self.popup_root, background=CREAM)

        self.pay_with()
    
    def pay_with(self):
        if self.master_frame.winfo_children():
            for child in self.master_frame.winfo_children():
                child.destroy()

        self.cancel_button.config(text='Cancel', command=lambda:self.popup_root.destroy())
        
        customtkinter.CTkButton(self.master_frame, text='Pay with\ncash', fg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 25), hover=False, command=lambda:self.pay_with_cash()).pack(side='left', fill='y', expand=1, padx=20)
        customtkinter.CTkButton(self.master_frame, text='Pay with\ncard', fg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 25), hover=False, command=lambda:self.pay_with_card()).pack(side='right', fill='y', expand=1, padx=20)

        self.master_frame.pack(side='top', pady=20, fill='both', expand=1)
    
    def pay_with_cash(self):
        for child in self.master_frame.winfo_children():
            child.destroy()
        self.confirm_button = customtkinter.CTkButton(self.master_frame, text=f'Place order\n#{self.order_num}', fg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, command=lambda:self.display_success())
        self.cancel_button.config(text='Go back', command=lambda:self.pay_with())
        root = self.master_frame

        Label(root, text='Enter total value of cash:', background=CREAM, foreground=BROWN, font=('Arial', 20), anchor='w').pack(fill='x', **self.paddings)
        self.cash_entry = customtkinter.CTkEntry(root, textvariable=self.cash, fg_color=DARK_CREAM, border_color=BROWN, text_color=BROWN, text_font=('Arial', 20))
        self.cash_entry.pack(fill='x', **self.paddings)

        Label(root, text='Change:', background=CREAM, foreground=BROWN, font=('Arial', 20), anchor='w').pack(fill='x', **self.paddings)
        change_label = Label(root, text='Enter cash value...', background=CREAM, foreground=BROWN, font=('Arial', 20), anchor='w')
        change_label.pack(fill='x', **self.paddings)

        self.cash.trace('w', lambda x, y, z, label=change_label:self.change_output(label))

    def pay_with_card(self):
        for child in self.master_frame.winfo_children():
            child.destroy()
        self.confirm_button = customtkinter.CTkButton(self.master_frame, text=f'Place order\n#{self.order_num}', fg_color=DARK_CREAM, text_color=BROWN, text_font=('Arial', 20), hover=False, command=lambda:self.display_success())
        self.cancel_button.config(text='Go back', command=lambda:self.pay_with())
        root = self.master_frame

        Label(root, text='Card number:', background=CREAM, foreground=BROWN, font=('Arial', 20), anchor='w').pack(fill='x', **self.paddings)
        self.card_number_entry = customtkinter.CTkEntry(root, textvariable=self.card_num, fg_color=DARK_CREAM, border_color=BROWN, text_color=BROWN, text_font=('Arial', 20))
        self.card_number_entry.pack(fill='x', **self.paddings)

        Label(root, text='Three digits on the back:', background=CREAM, foreground=BROWN, font=('Arial', 20), anchor='w').pack(fill='x', **self.paddings)
        self.card_csv_entry = customtkinter.CTkEntry(root, textvariable=self.card_csv, fg_color=DARK_CREAM, border_color=BROWN, text_color=BROWN, text_font=('Arial', 20))
        self.card_csv_entry.pack(fill='x', **self.paddings)

        self.card_num.trace('w', lambda x, y, z, type='card':self.is_allowed(type))
        self.card_csv.trace('w', lambda x, y, z, type='card':self.is_allowed(type))
    
    def change_output(self, label):
        self.is_allowed('cash')
        if self.round(self.cash.get()) == self.round(self.order_price):
            label.config(text='Exact change')
            self.confirm_button.pack()
            return
        if self.cash.get() != '':
            difference = self.round(float(self.cash.get()))-self.order_price
            rounded = self.round(difference)    # round() function is unreliable with float
        try:
            if float(self.cash.get()) >= self.order_price:
                label.config(text=f'${abs(rounded)} change')
                self.confirm_button.pack()
            else:
                label.config(text=f'${abs(rounded)} more')
                self.confirm_button.forget()
        except ValueError:
            label.config(text='Enter cash value...')
    
    def is_allowed(self, type):
        if type == 'cash':
            cash_input = self.cash.get()

            if cash_input == '.':
                self.cash_entry.delete((len(self.cash.get())-1), END)

            if cash_input != '':
                decimal = False
                for c in cash_input:

                    if decimal == True:
                        if c == '.':
                            self.cash_entry.delete((len(cash_input)-1), END)
                        if len(split_string[1]) >= 3:
                            self.cash_entry.delete((len(cash_input)-1), END)
                            break
                    
                    if decimal == False and c == '.':
                        decimal = True
                        split_string = self.cash.get().split('.')
                    elif c.isdigit() == False and c != '.':
                        self.cash_entry.delete((len(cash_input)-1), END)
                    
        elif type == 'card':
            card_num_input = self.card_num.get()
            raw_card_num_input = []

            for c in card_num_input:
                if c != ' ':
                    raw_card_num_input.append(c)
            
            if card_num_input != '':
                if card_num_input[len(card_num_input)-1].isdigit() == False:
                    self.card_number_entry.delete((len(card_num_input)-1), END)
                    return
                
                if (len(raw_card_num_input) % 4) == 0 and len(self.old) == 0:
                    if len(raw_card_num_input) != 16:
                        self.card_number_entry.insert(END, ' ')
                
                if (len(self.card_num.get()) % 5) == 0:   # if a space has been inserted
                    if self.card_num.get()[len(self.card_num.get())-1] == ' ':
                        self.old.append(self.card_num.get())
                    else:
                        self.card_number_entry.insert([len(self.card_num.get())-1], ' ')
                else:
                    for child in self.old:
                        self.old.remove(child)
                
                if len(raw_card_num_input) >= 17:
                    self.card_number_entry.delete((len(card_num_input)-1), END)
                    return

            if len(self.card_csv.get()) >= 4:
                self.card_csv_entry.delete(3, END)
            
            if self.card_csv.get().isdigit() == False:
                self.card_csv_entry.delete(len(self.card_csv.get())-1, END)
    
    def display_success(self):
        self.restart_function()
        self.popup_root.destroy()