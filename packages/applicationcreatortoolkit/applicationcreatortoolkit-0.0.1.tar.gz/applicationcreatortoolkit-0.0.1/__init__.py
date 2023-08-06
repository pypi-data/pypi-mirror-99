from tkinter import *
from tkinter import messagebox

class MainWin:

    def __init__(self):
        global root
        root = Tk()

    def title(self, title):
        root.title(title)

    def size(self, size):
        if size == "fullscreen":
            root.attributes("-fullscreen", True)
        else:
            root.geometry(size)

    def text_label(self, info):
        text = Label(root, text=info)
        text.pack()

    def button(self, button_text, onclick):
        button = Button(root, text=button_text, command=onclick)
        button.pack()

def popup(popup_title, popup_message):
        messagebox.showinfo(popup_title, popup_message)
