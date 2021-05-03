import tkinter as tk


class FileSavedGui:
    def __init__(self, root: tk.Tk):
        self.window = tk.Toplevel(root)
        self.window.title("Plik zapisany")

    def display_file_saved(self, filepath: str):
        tk.Label(self.window, text='Plik został zapisany w: ').grid(row=1, column=0)
        tk.Label(self.window, text=filepath).grid(row=2, column=0)
        tk.Button(self.window, text='Ok', command=self.window.destroy).grid(row=3, column=0)
