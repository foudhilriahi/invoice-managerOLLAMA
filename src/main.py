from tkinter import Tk
from gui import InvoiceApp
from database import init_db

if __name__ == "__main__":
    init_db()
    root = Tk()
    app = InvoiceApp(root)
    root.mainloop()
