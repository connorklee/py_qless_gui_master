import sys

from tkinter import *
from tkinter.messagebox import askyesno

from lib.gui.entry_page import EntryPage

class Root(Tk):
    def __init__(self, dic='./dics/sowpods.txt'):
        Tk.__init__(self)
        self.title('PyQLess')
        self.config(bg='azure')
        # self.protocol('WM_DELETE_WINDOW', self.quit_game)

        self.dict = dic

        # center game window
        ws = self.winfo_screenwidth()
        x = int((ws/2) - (704/2))  

        self.geometry('704x420+{}+{}'.format(x, 0))
        self.minsize(704, 420)

        self.draw_menu()
        self.draw_container()

        EntryPage(self.container, self.dict)

    def draw_menu(self):
        top = Menu(self)
        self.config(menu=top)

        game_m = Menu(top)
        game_m.add_command(label='Quit', underline=0, command=self.quit_game)

        about_m = Menu(top)
        about_m.add_command(label='Game Info', underline=0, command=self.render_info_page)

        top.add_cascade(label='Game', menu=game_m, underline=0)
        top.add_cascade(label='About', menu=about_m, underline=0)

    def draw_container(self):
        self.container = Frame(self, bg='azure')
        self.container.pack(side=TOP, fill=BOTH, expand=YES)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def render_info_page(self):
        info_page = Toplevel(self)
        info_page.minsize(700, 420)
        info_page.maxsize(700, 420)

        info = Text(info_page, height=40, width=90)
        scroll = Scrollbar(info_page, command=info.yview)

        info.configure(yscrollcommand=scroll.set)

        info.tag_configure('bold', font=('Arial', 15, 'bold'))
        info.tag_configure('title', font=('Arial', 21, 'bold', 'italic'), justify='center')
        info.tag_configure('italic', font=('Arial', 13, 'italic'))
        info.tag_configure('underline', font=('Arial', 12, 'italic', 'underline'))

        info.insert(END, 'BASIC INFO\n\n', 'title')
        info.insert(END, 'THE GAME\n\n', 'bold')
        info.insert(END, 'Roll the dice and use ALL 12 letters to make words that connect. Words must have at least 3 letters. No proper nouns. No time limit. Most rolls are solvable but not all.\n\n\n')
        info.insert(END, 'Caution\n\n', 'bold')
        info.insert(END, 'Q-Less can be addictive.\n\n\n')
        info.pack(side=LEFT, padx=20)
        scroll.pack(side=RIGHT, fill=Y)

    def quit_game(self):
        if askyesno('Quit Game', 'Are you sure to quit the game?'):
            if self.child:
                self.child.destroy()

            self.quit()

    def set_geometry(self):
        if sys.platform == 'darwin':
            self.geometry('750x790')
            self.minsize(750, 790)
        elif sys.platform == 'win32':
            self.geometry('620x600')
            self.minsize(620, 600)
        else:
            self.geometry('700x650')
            self.minsize(700, 650)
