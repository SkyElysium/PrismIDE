from tkinter import Menu

class MainMenu:
    def __init__(self, master):
        self.master = master

        self.display()

        self.master.config(menu = self.menu)

    def display(self):
        self.menu = Menu(self.master)

        # file
        self.file = Menu(self.menu, tearoff = False)
        self.file.add_command(label = 'New', command = self.master.new)
        self.file.add_command(label = 'Open', command = self.master.open)
        self.file.add_command(label = 'Save', command = self.master.save)
        self.file.add_command(label = 'Save as...', command = self.master.save_as)

        self.menu.add_cascade(label =  'File', menu = self.file)

        # edit
        self.edit = Menu(self.menu, tearoff = False)
        self.edit.add_command(label = 'Undo', command = self.master.undo, accelerator = 'Ctrl+Z')
        self.edit.add_command(label = 'Redo', command = self.master.redo, accelerator = 'Ctrl+Shift+Z')
        self.edit.add_separator()
        self.edit.add_command(label = 'Copy', command = self.master.copy, accelerator = 'Ctrl+C')
        self.edit.add_command(label = 'Cut', command = self.master.cut, accelerator = 'Ctrl+X')
        self.edit.add_command(label = 'Paste', command = self.master.paste, accelerator = 'Ctrl+V')
        self.edit.add_command(label = 'Select all', command = self.master.select_all, accelerator = 'Ctrl+A')

        self.menu.add_cascade(label = 'Edit', menu = self.edit)

class RightClickMenu:
    def __init__(self, master, text_weight):
        self.master = master
        self.text_weight = text_weight

        self.display()

        self.text_weight.bind('<Button-3>', lambda event: self.right.post(event.x_root, event.y_root))

    def display(self):
        self.right = Menu(tearoff = False)

        self.right.add_command(label = 'Copy', command = self.master.copy)
        self.right.add_command(label = 'Cut', command = self.master.cut)
        self.right.add_command(label = 'Paste', command = self.master.paste)
