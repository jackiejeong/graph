import tkinter as tk
from tkinter import filedialog
import pandas as pd

def Load():
    loadpath = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("Excel files","*.xlsx"),
                                          ("all files", "*.*")))
    data = pd.read_excel(loadpath)
    return data

def Save():
    savepath = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                          filetypes=(("Excel files","*.xlsx"),
                                          ("all files", "*.*")))


    