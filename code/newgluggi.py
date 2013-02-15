import Tkinter
from Tkinter import *
import tkMessageBox

top = Tkinter.Tk()
top.wm_title("New")
#Text
var = StringVar()
label = Label( top, textvariable=var,)

var.set("Enter ticker of company/indice you wish to examin:")
label.pack()
#Frame
frame = Frame(top,height=80,width=150)
frame.pack()

#Entry
L1 = Label(top)
L1.pack( side = LEFT)
E1 = Entry(top, bd =5)

E1.pack()

#Buttons
#def OpenNewWindow():
   #tkMessageBox.showinfo( "Hello Python", "Hello World")

def close_window(): 
  top.destroy()
  
B = Tkinter.Button(top, text ="Open", command = close_window)

C = Tkinter.Button(top, text ="Cancel", command = close_window)


B.pack()
C.pack()

#Placement of buttons and entry
B.place(x=68, y=80)
C.place(x=158, y=80)
E1.place(x=70, y=35)
top.mainloop()
