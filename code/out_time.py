from tkinter import *
from tkinter import messagebox
import tkinter as tk 
import time
app = Tk()
app.title("出場")
app_scale = Canvas(height=150, width=600)
lbl1 = Label(app, text="車牌號碼",font=('Arial', 30))
lbl1.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.N+tk.E)
#\抓取系統時間\
localtime = time.localtime()
result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
#\\\\\\\\\\\\\\
lbl2 = Label(app, text=result,font=('Arial', 20))
lbl2.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.N+tk.E)
app_scale.grid()
app.mainloop()