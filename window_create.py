
from tkinter import ttk
import tkinter as tk


def selectTracker():
    main_window = tk.Tk()
    main_window.geometry("280x220")
    main_window.title("Odabir metode")

    l1 = tk.Label(main_window,  text='Molimo odaberite metodu praćenja objekta', width=32 )  

    l1.grid(row=0, column=0, sticky="NSWE", padx=(20, 10), pady=(7.5, 0))

    combo = ttk.Combobox(
        state="readonly",
        values=["CSRT", "KCF", "BOOSTING", "MIL", "TLD", "MEDIANFLOW", "MOSSE"]
    )
    combo.place(x=50, y=50)

    
    b1 = tk.Button(main_window,  text='OK', command=lambda: my_show() )  
    b1.place(x=100, y=80)

    def my_show():
        if combo.get() != "":
            global trackerType
            trackerType = combo.get()
            main_window.destroy()

    main_window.mainloop()

    return trackerType


def chooseToRecord():
  
    root = tk.Tk()
    root.geometry("340x120")
    root.title("Potvrda pohrane")
    var = tk.IntVar()

    tk.Label(root, 
            text="Želite li snimiti i pohraniti video sekvencu praćenje objekta?",
            justify = tk.CENTER,
            padx = 20).pack()

    tk.Radiobutton(root, 
                text="Da",
                padx = 20, 
                variable=var, 
                value=True).pack(anchor=tk.W)

    tk.Radiobutton(root, 
                text="Ne",
                padx = 20, 
                variable=var, 
                value=False).pack(anchor=tk.W)

    def my_show():
        if var.get() is not None:
            global saveStatus
            saveStatus = var.get()
            root.destroy()
    
    b1 = tk.Button(root,  text='OK', command=lambda: my_show() )  
    b1.place(x=145, y=80)

    root.mainloop()

    return saveStatus

