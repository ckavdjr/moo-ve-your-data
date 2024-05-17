import tkinter as tk
from tkinter import ttk
import sqlite3

class FarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Farm Management System")
        
        self.create_main_frame()
        self.create_treeview()
        self.create_buttons()
        
        self.load_data()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

    def create_treeview(self):
        self.tree = ttk.Treeview(self.main_frame, columns=("gender", "dob", "colour", "breed", "identification_mark"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("dob", text="DOB")
        self.tree.heading("colour", text="Colour")
        self.tree.heading("breed", text="Breed")
        self.tree.heading("identification_mark", text="Identification Mark")
        self.tree.pack(expand=True, fill=tk.BOTH)

    def create_buttons(self):
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Add Cow", command=self.add_cow).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Edit Cow", command=self.edit_cow).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete Cow", command=self.delete_cow).grid(row=0, column=2, padx=5)

    def load_data(self):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        c.execute("SELECT * FROM cows")
        rows = c.fetchall()

        for row in rows:
            self.tree.insert("", "end", text=row[0], values=row[1:])

        conn.close()

    def add_cow(self):
        pass

    def edit_cow(self):
        pass

    def delete_cow(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = FarmApp(root)
    root.mainloop()
