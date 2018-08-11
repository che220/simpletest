from tkinter import Tk, Frame, LEFT, BOTH, RIGHT

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Article Reader')

root = Tk()
root.geometry('400x500+200+200')
app = Window(root)
root.mainloop()