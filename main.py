import tkinter as tk
import os
from tkinter import *

os.system("taskkill /f /im explorer.exe")

root = tk.Tk()

root.overrideredirect(True)

width, height = 2080, 50
root.attributes('-topmost', True)
root.geometry(f"{width}x{height}+0+1032")
root.configure(background='#1B3769')

border_canvas = tk.Canvas(root, width=width, height=height, background='#1B3769', highlightthickness=0)
border_canvas.pack()

border_width = 3
border_canvas.create_rectangle(0, 0, width, border_width, fill='#0D204D', outline='#0D204D')  # Top border
border_canvas.create_rectangle(0, 0, border_width, height, fill='#0D204D', outline='#0D204D')  # Left border

root.mainloop()
