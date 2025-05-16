from tkinter import Text

class LineNumberBar:
    def __init__(self, master, text_weight):
        self.master = master
        self.text_weight = text_weight

        self.display()

        # binding
        self.line_number_bar.bind('<MouseWheel>', self.wheel)

        self.line_number_bar.bind('<Button-1>', lambda event: 'break')

    def display(self):
        self.line_number_bar = Text(self.master, width = 5, bd = False, bg = '#e8e8e8', font = ('Consolas', 13), state = 'disabled', cursor = 'arrow')
        self.line_number_bar.pack(fill = 'y', side = 'left')

    def update_line_number(self):
        # update the line number
        self.lines = self.text_weight.index('end').split('.')[0]
        self.line_context = '\n'.join([' ' + str(num) for num in range(1, int(self.lines))])

        self.line_number_bar.config(state = 'normal')

        self.line_number_bar.delete('1.0', 'end')
        self.line_number_bar.insert('1.0', self.line_context)

        self.line_number_bar.config(state = 'disabled')

        self.line_number_bar.yview_moveto(self.text_weight.yview()[0])

    def scroll(self, *xy):
        # config scroll
        self.text_weight.yview(*xy)
        self.line_number_bar.yview(*xy)

    def wheel(self, event):
        # scroll the text and the line number bar
        self.text_weight.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        self.line_number_bar.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        return 'break'
