import tkinter as tk
from pywinauto import Desktop
import win32ui
import win32gui
import win32con
import win32api
import psutil
import os
from PIL import Image, ImageTk
import time

# Create a folder for icons
icons_folder = "iconcache"
os.makedirs(icons_folder, exist_ok=True)

def focus_window(window_title):
    for window in Desktop(backend="uia").windows():
        if window.window_text() == window_title:
            window.set_focus()

def save_icon(exe_file, out_file):
    ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
    ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
    large, small = win32gui.ExtractIconEx(exe_file, 0)

    # Check if the 'large' list is not empty before proceeding
    if large:
        win32gui.DestroyIcon(large[0])

        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), small[0])
        hbmp.SaveBitmapFile(hdc, os.path.join("iconcache", f"{out_file}"))

root = tk.Tk()

width, height = 2080, 50
root.overrideredirect(True)
root.attributes('-topmost', True)
root.geometry(f"{width}x{height}+0+1032")
root.title("Dock")
root.configure(background='#1B3769')

def update_buttons():
    # Destroy existing buttons
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()

    programbutton = tk.Button(root, activebackground="#1F355A", bd=6, width=5, height=3, bg="#346BCA", highlightcolor="#3D5887", highlightthickness=0)
    programbutton.pack(side=tk.LEFT)

    # List and create buttons for each open window with icons
    windows = Desktop(backend="uia").windows()
    for window in windows:
        process_id = window.process_id()
        process = psutil.Process(process_id)
        exe_path = process.exe()

        # Extract the executable name from the path
        executable_name = os.path.basename(exe_path)
        cleaned_executable_name = ''.join(c if c.isalnum() or c in ['_', '-', ' ', '.', '(', ')'] else '' for c in executable_name)
        icon_path = f"{cleaned_executable_name}.png"

        try:
            save_icon(exe_path, icon_path)

            pil_image = Image.open(os.path.join(icons_folder, icon_path))
            tk_image = ImageTk.PhotoImage(pil_image)

            button = tk.Button(root, bd=6, activebackground="#000000", bg="#000000", image=tk_image, highlightthickness=0, height=70, command=lambda title=window.window_text(): focus_window(title))
            button.pack(side=tk.LEFT, anchor='nw')
            button.image = tk_image
            button.pack(side=tk.LEFT)
        except FileNotFoundError:
            # Skip this window if icon extraction fails
            continue
        
    root.after(800, update_buttons)

# Initial update
update_buttons()

root.mainloop()