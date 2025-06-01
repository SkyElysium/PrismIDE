from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter.ttk import Separator
from tkinter import messagebox

import clipboard
import chardet

class Main(Tk):
    def __init__(self):
        super().__init__()

        # window config
        self.geometry('800x500')
        self.title('Prism IDE')

        self.protocol('WM_DELETE_WINDOW', self.closing)

        self.iconbitmap('resources/icon.ico')

        # variables
        self.path = None
        self.info = ''

        # call functions
        self.surface()

        # display the menus
        self.config(menu = self.menu)

    def surface(self):
        # create the main menu
        self.menu = Menu()

        self.file = Menu(self.menu, tearoff = False)
        self.file.add_command(label = 'New', command = self.new)
        self.file.add_command(label = 'Open', command = self.open)
        self.file.add_command(label = 'Save', command = self.save)
        self.file.add_command(label = 'Save as...', command = self.save_as)

        self.menu.add_cascade(label = 'File', menu = self.file)

        self.edit = Menu(self.menu, tearoff = False)
        self.edit.add_command(label = 'Undo', command = self.undo, accelerator = 'Ctrl+Z')
        self.edit.add_command(label = 'Redo', command = self.redo, accelerator = 'Ctrl+Shift+Z')
        self.edit.add_separator()
        self.edit.add_command(label = 'Copy', command = self.copy, accelerator = 'Ctrl+C')
        self.edit.add_command(label = 'Cut', command = self.cut, accelerator = 'Ctrl+X')
        self.edit.add_command(label = 'Paste', command = self.paste, accelerator = 'Ctrl+V')
        self.edit.add_command(label = 'Select all', command = self.select_all, accelerator = 'Ctrl+A')

        self.menu.add_cascade(label = 'Edit', menu = self.edit)

        # right-click menu
        self.right = Menu(tearoff = False)
        self.right.add_command(label = 'Copy', command = self.copy)
        self.right.add_command(label = 'Cut', command = self.cut)
        self.right.add_command(label = 'Paste', command = self.paste)

        # create the status bar
        self.status = StringVar()

        self.status_bar = Label(anchor = 'e', textvariable = self.status, bg = 'white')
        self.status_bar.pack(fill = 'x', side = 'bottom')

        Separator().pack(fill='x', side='bottom')

        # create the scrollbar
        self.scrollbar = Scrollbar()
        self.scrollbar.pack(fill = 'y', side = 'right')

        # create the line number bar
        self.line_number_bar = Text(width = 5, bd = False, bg = '#e8e8e8', font = ('Consolas', 13), state = 'disabled', cursor = 'arrow')
        self.line_number_bar.pack(fill = 'y', side = 'left')

        # create the text
        self.text = Text(undo = True, wrap = 'none', bd = False, font = ('Consolas', 13))
        self.text.pack(fill='both', expand=True)

        # tab
        text_font = font.Font(font = self.text['font'])
        tab_size = text_font.measure(' ' * 4)

        self.text.config(tabs = tab_size)

        # config the scrollbar
        self.text['yscrollcommand'] = self.scrollbar.set

        # scroll the text and the line number bar
        self.scrollbar.config(command = self.scroll)

        # delete event
        self.event = {'<Control-z>' : '<<Undo>>',
                     '<Control-Shift-z>'  : '<<Redo>>',
                     '<Control-c>'  : '<<Copy>>',
                     '<Control-x>'  : '<<Cut>>',
                     '<Control-v>'  : '<<Paste>>'
                     }

        for key, event_name in self.event.items():
            self.event_delete(event_name, key)
            self.event_delete(event_name, key.title())

        # bind
        self.fast = {'<Control-z>' : self.undo,
                     '<Control-Shift-z>' : self.redo,
                     '<Control-c>' : self.copy,
                     '<Control-x>' : self.cut,
                     '<Control-v>' : self.paste,
                     '<Control-a>' : self.select_all
                     }

        for key, func in self.fast.items():
            self.bind(key, func)
            self.bind(key.title(), func)

        self.text.bind('<Button-3>', lambda event : self.right.post(event.x_root, event.y_root))

        self.text.bind('<Any-KeyPress>', lambda event : self.after(1, self.update_line_number))
        self.text.bind('<<Selection>>', lambda event : self.after(1, self.update_line_number))

        self.text.bind('<MouseWheel>', self.wheel)
        self.line_number_bar.bind('<MouseWheel>', self.wheel)

        self.line_number_bar.bind('<Button-1>', lambda event : 'break')

        self.update_line_number()

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

        self.update_line_number()

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

        self.update_line_number()

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
            exit()

    def undo(self, event = None):
        # undo
        try:
            self.text.edit_undo()
        except:
            pass

        self.update_line_number()

    def redo(self, event = None):
        # redo
        try:
            self.text.edit_redo()
        except:
            pass

        self.update_line_number()

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

        self.update_line_number()

    def paste(self, event = None):
        # paste the text
        self.context = clipboard.paste()
        self.text.insert(INSERT, self.context)

        self.update_line_number()

    def select_all(self, event = None):
        # select all the text
        self.text.tag_add('sel', '1.0', 'end')

    def update_line_number(self):
        # update the line number
        self.lines = self.text.index('end').split('.')[0]
        self.line_context = '\n'.join([' ' + str(num) for num in range(1, int(self.lines))])

        self.line_number_bar.config(state = 'normal')

        self.line_number_bar.delete('1.0', 'end')
        self.line_number_bar.insert('1.0', self.line_context)

        self.line_number_bar.config(state = 'disabled')

        self.line_number_bar.yview_moveto(self.text.yview()[0])

    def scroll(self, *xy):
        # config scroll
        self.text.yview(*xy)
        self.line_number_bar.yview(*xy)

    def wheel(self, event):
        # scroll the text and the line number bar
        self.text.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        self.line_number_bar.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        return 'break'

if __name__ == '__main__':
    run = Main()
    run.mainloop()