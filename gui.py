import tkinter as tk
from tkinter import ttk,messagebox
window = tk.Tk()
window.title('小红书舆情综合分析系统')
window.geometry('800x600')
label=tk.Label(window,text='请输入你想研究的话题',font=("Arial",16))
label.pack(pady=10)
entry=tk.Entry(window,width=50,font=('Arial',20))
entry.pack(pady=20)
window.mainloop()