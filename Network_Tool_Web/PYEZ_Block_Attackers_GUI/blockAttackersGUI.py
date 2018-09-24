from Tkinter import *
from jnpr.junos.utils.config import Config
import json
import mysql.connector

form = Tk()

topFrame = Frame(form)
topFrame.pack()

bottomFrame = Frame(form)
bottomFrame.pack(side=BOTTOM)

label1 = Label(topFrame, text="Block Attackers Tool")
label1.pack(fill=X)

button1 = Button(bottomFrame, text="Block IP")
button2 = Button(bottomFrame, text='Delete IP')
button3 = Button(bottomFrame, text='Exit')

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=RIGHT)


form.mainloop()

