
# source(6/2020): https://dev.to/abdurrahmaanj/building-an-oop-calculator-and-what-it-means-to-write-a-widget-library-4560

from tkinter import *

BUTTON_WIDTH = 4


def b_info(symbol, operation=None, width=1):
    if operation is None:
        operation = lambda s: s+symbol
    return (symbol, operation, width)


class Calculator:
    def __init__(self, parent, x, y):
        self.button_font = ('Verdana', 15)
        self.entry_font = ('Verdana', 20)
        self.parent = parent

        self.button_height = 1
        self.container = Frame(self.parent)
        self.container.grid(row=x, column=y)

        self.string = ''

        self.entry(0, 0)

        numbers = [
            [b_info(str(i)) for i in range(n, n+3)]
            for n in range(7, 0, -3)
        ]
        buttons = [
            [ b_info('+'), b_info('-') ],
            [ b_info('*'), b_info('/') ],
            [ b_info('('), b_info(')') ],
            [ 
                b_info('0'), 
                b_info('=', lambda s: str(eval(s)), 2),
                b_info('clear', lambda s: ''),
                b_info('<', lambda s: s[:-1])
            ], 
            []
        ]
        buttons = [i+j for i,j in zip(numbers+[[]], buttons)]

        for row, y in zip(buttons, range(1, len(buttons)+2)):
            x = 0 if y > 0 else 2
            for b in row:
                self.button(b[0], b[1], x, y, b[2])
                x += b[2]


    def entry(self, x, y):
        self.entry = Text(
            self.container, font=self.entry_font, state=DISABLED,
            height=self.button_height//2, width=BUTTON_WIDTH * 5)
        self.entry.grid(row=x, column=y, columnspan=5, sticky='we')

    def button(self, char, operation, x, y, w):
        print(x, y)
        def execute():
            self.string = operation(self.string)
            self.display(self.string)

        button = Button(
            self.container, text=char, width=BUTTON_WIDTH,
            height=self.button_height, font=self.entry_font,
            command=execute
        )
        button.grid(row=y, column=x, sticky='we', columnspan=w)

    def display(self, text_):
        self.entry.config(state=NORMAL)
        self.entry.delete('1.0', END)
        self.entry.insert('1.0', text_)
        self.entry.config(state=DISABLED)

class App:
    def __init__(self, master):
        self.master = master
        calc = Calculator(self.master, 0, 0)


root = Tk()
app = App(root)
root.title('dev.to calculator')
root.mainloop()
