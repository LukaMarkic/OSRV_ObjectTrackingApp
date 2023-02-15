
from tkinter.filedialog import askopenfilename
import tkinter as tk

def getVideo():
    root = tk.Tk()
    root.withdraw()
    filePath = askopenfilename(filetypes=[("Video files", "*.mp4"),("Video files", "*.avi") ]) 
    root.destroy()

    return filePath

