import tkinter as tk
import os
from tkinter import *

os.system("taskkill /f /im explorer.exe")

root = tk.Tk()

root.overrideredirect(True)

width, height = 2080, 50
root.attributes('-topmost', True)
root.geometry(f"{width}x{height}+0+1032")

root.mainloop()