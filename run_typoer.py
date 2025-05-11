import tkinter as tk
from typoer.gui import TypoerGUI

def main():
    root = tk.Tk()
    app = TypoerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 