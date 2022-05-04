from tkinter import *
import tkinter as tk 
import time

app = Tk()
app.title("入場")
app_scale = Canvas(height=150, width=600)
lbl1 = Label(app, text="車牌號碼",font=('Arial', 30))#製作一個label並顯示車牌號碼和控制字體、大小
lbl1.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.N+tk.E)
#\抓取系統時間\
localtime = time.localtime()
result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
#\\\\\\\\\\\\\\
lbl2 = Label(app, text=result,font=('Arial', 20))
lbl2.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.N+tk.E)
app_scale.grid()
app.mainloop()

app.fullScreenState = not app.fullScreenState
app.window.attributes("-zoomed", app.fullScreenState)