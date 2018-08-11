import tkinter

top = tkinter.Tk()
frame = tkinter.Frame(top)
frame.pack()

button_frame = tkinter.Frame(top)
button_frame.pack(side=tkinter.BOTTOM)

red_button = tkinter.Button(frame, text='Red', fg='red')
red_button.pack(side=tkinter.LEFT)

green_button = tkinter.Button(frame, text='Green top middle', fg='green')
green_button.pack(side=tkinter.LEFT)

blue_button = tkinter.Button(frame, text='Blue', fg='blue')
blue_button.pack(side=tkinter.LEFT)

black_button = tkinter.Button(button_frame, text='Black', fg='black')
black_button.pack(side=tkinter.LEFT)

top.mainloop()
