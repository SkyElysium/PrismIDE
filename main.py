from tkinter import *
from tkinter import filedialog, font, messagebox
from tkinter.ttk import Separator

import sys
from menu import MainMenu, RightClickMenu
from line_number_bar import LineNumberBar
from binding import Binding

import clipboard
import chardet

class Main(Tk):
    def __init__(self):
        super().__init__()

        # window config
        self.geometry('800x500')
        self.title('Prism IDE')

        self.protocol('WM_DELETE_WINDOW', self.closing)

        self.iconbitmap('res/icon.ico')

        # variables
        self.path = None
        self.info = ''

        # call functions
        self.surface()

    def surface(self):
        # create the status bar
        self.status = StringVar()

        self.status_bar = Label(anchor = 'e', textvariable = self.status, bg = 'white')
        self.status_bar.pack(fill = 'x', side = 'bottom')

        Separator().pack(fill='x', side='bottom')

        # create the scrollbar
        self.scrollbar = Scrollbar()
        self.scrollbar.pack(fill = 'y', side = 'right')

        # text
        self.text = Text(undo = True, wrap = 'none', bd = False, font =  ('Consolas', 13))

        self.line_number_bar = LineNumberBar(self, self.text)

        self.text.pack(fill = 'both', expand = True)

        # config the scrollbar
        self.text['yscrollcommand'] = self.scrollbar.set

        # scroll the text and the line number bar
        self.scrollbar.config(command = self.line_number_bar.scroll)

        # create the main menu
        self.menu = MainMenu(self)

        # right-click menu
        self.right = RightClickMenu(self, self.text)

        # tab
        text_font = font.Font(font = self.text['font'])
        tab_size = text_font.measure(' ' * 4)

        self.text.config(tabs = tab_size)

        # binding
        Binding(self)

        self.text.bind('<Any-KeyPress>', lambda event : self.after(1, self.line_number_bar.update_line_number))
        self.text.bind('<<Selection>>', lambda event : self.after(1, self.line_number_bar.update_line_number))

        self.text.bind('<MouseWheel>', self.line_number_bar.wheel)

        self.line_number_bar.update_line_number()

    def new(self):
        # create a new file
        if self.closing_tip() is None:
            return

        self.title('Prism IDE - New')

        self.text.delete('0.1', 'end')
        self.path = None
        self.info = ''

        self.status.set('')
        self.text.edit_modified(False)

        self.line_number_bar.update_line_number()

    def open(self):
        # open the file
        if self.closing_tip() is None:
            return

        self.path = filedialog.askopenfilename()

        if not self.path:
            return None

        self.title(f'Prism IDE - {self.path}')

        with open(self.path, 'rb') as read:
            # get the right encoding
            context = read.read()
            self.info = chardet.detect(context)

            self.text.delete('1.0', 'end')
            self.text.insert('end', context.decode(self.info['encoding']))

            self.status.set(self.info['encoding'].upper() + ' ')

            self.info = ''
            self.text.edit_modified(False)

        self.line_number_bar.update_line_number()

    def save(self):
        # save the file
        if not self.path:
            return self.save_as()
        else:
            with open(self.path, 'w', encoding = 'utf-8' if self.info == '' else self.info['encoding']) as write:
                write.write(self.text.get('1.0', 'end'))
                self.text.edit_modified(False)

    def save_as(self):
        # save the file as...
        self.path = filedialog.asksaveasfilename()

        if self.path:
            with open(self.path, 'w', encoding = 'utf-8' if self.info == '' else self.info['encoding']) as write:
                write.write(self.text.get('1.0', 'end'))
                self.text.edit_modified(False)
        else:
            return 'EmptyPath'

    def undo(self, event = None):
        # undo
        try:
            self.text.edit_undo()
        except:
            pass

        self.line_number_bar.update_line_number()

    def redo(self, event = None):
        # redo
        try:
            self.text.edit_redo()
        except:
            pass

        self.line_number_bar.update_line_number()

    def copy(self, event = None):
        # copy select text
        try:
            self.context = self.text.get(SEL_FIRST, SEL_LAST)
            clipboard.copy(self.context)
        except:
            pass

    def cut(self, event = None):
        # cut select text
        self.copy()

        try:
            self.text.delete(SEL_FIRST, SEL_LAST)
        except:
            pass

        self.line_number_bar.update_line_number()

    def paste(self, event = None):
        # paste the text
        self.context = clipboard.paste()
        self.text.insert(INSERT, self.context)

        self.line_number_bar.update_line_number()

    def select_all(self, event = None):
        # select all the text
        self.text.tag_add('sel', '1.0', 'end')

    def closing_tip(self):
        # create a tip window
        msg = ''
        if self.text.edit_modified() == 1:
            msg = messagebox.askyesnocancel(title = 'Tip', message = 'Do you want to save the file?')
            if msg == 1:
                if self.save() == 'EmptyPath':
                    msg = None

        return msg

    def closing(self):
        # exit logic
        if self.closing_tip() is not None:
            sys.exit()

if __name__ == '__main__':
    run = Main()
    run.mainloop()
