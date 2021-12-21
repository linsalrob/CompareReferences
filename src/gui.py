
import tkinter as tk
from filereader import FileReader

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Compare References from Google Scholar and ORCID")
    root.geometry("800x600")
    f = FileReader(root)
    root.mainloop()