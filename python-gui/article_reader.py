from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

root = Tk()

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('Zero Hedge Reader')
        self.pack(fill=BOTH)

        canvas = Canvas(self, highlightthickness=0)
        canvas.pack(expand=1, padx=10, pady=10)
        Label(canvas, text='Zero Hedge articles:').pack(side=LEFT, padx=10)
        self.article_combo = Combobox(canvas, state='readonly', value=['article 1', 'article 2', 'article 3', 'article 4'])
        self.article_combo.current(0)
        self.article_combo.pack(side=LEFT, padx=10)

        canvas = Canvas(self, highlightthickness=0)
        canvas.pack(expand=True, pady=10, fill=BOTH)
        scroll_bar = Scrollbar(canvas)
        scroll_bar.pack(side=RIGHT, fill=Y)

        self.article_box = Text(canvas, background='yellow')
        self.article_box.pack(side=LEFT, fill=BOTH, expand=True)
        scroll_bar.config(command=self.article_box.yview)
        self.article_box.config(yscrollcommand=scroll_bar.set)

        Button(self, text='Exit', command=self._client_exit).pack(fill=BOTH, padx=10, pady=10)

    def _client_exit(self):
        exit(0)
#        if messagebox.askyesno("Please Verify", "Do you really want to exit?"):
#            exit(0)

if __name__ == '__main__':
    root.geometry('400x600+0+0')
    app = Window(root)
    root.mainloop()
