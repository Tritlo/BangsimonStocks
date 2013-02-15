import Tkinter
from Tkinter import *
import tkMessageBox
import ttk

top = Tkinter.Tk()
top.wm_title("New")

#Frame
frame = Frame(top,height=180,width=300)
frame.pack()

#Text
var = StringVar()
label = Label(top, textvariable=var,)

var.set("           Days in moving average:\n \n \n \n Date to plot from:\n \n \n Date to plot to:")
label.pack()
label.place(y=10)


#Frame
frame = Frame(top)
frame.pack()

#Entry
L2 = Label(top)
L2.pack( side = LEFT)
E2 = Entry(top,width=5,justify=RIGHT)

E2.pack()

#Buttons
#def OpenNewWindow():
   #tkMessageBox.showinfo( "Hello Python", "Hello World")

def close_window(): 
  top.destroy()
  
D = Tkinter.Button(top, text ="Plot", command = close_window, width=6)

F = Tkinter.Button(top, text ="Cancel", command = close_window,)

D.pack()
F.pack()

#Comboboxes
countryvar = StringVar()
box1 = ttk.Combobox(top, textvariable=countryvar,width=15)
box1.pack()

box2 = ttk.Combobox(top, textvariable=countryvar,width=15)
box2.pack()

#Til ad binda vid
#country.bind('<<ComboboxSelected>>', function)

#Placement of buttons and entry
D.place(x=85, y=160)
F.place(x=155, y=160)
E2.place(x=175, y=12)
box1.place(x=135, y=70)
box2.place(x=135, y=115)

top.mainloop()

