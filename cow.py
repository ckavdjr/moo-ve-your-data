import tkinter as tk
from tkinter import ttk
import sqlite3

class CowManager:
    def __init__(self, root, tree):
        self.root = root
        self.tree = tree

    # def create_treeview(self):
    #     self.tree = ttk.Treeview(self.root, columns=("gender", "dob", "colour", "breed", "identification_mark"))
    #     self.tree.heading("#0", text="ID")
    #     self.tree.heading("gender", text="Gender")
    #     self.tree.heading("dob", text="DOB")
    #     self.tree.heading("colour", text="Colour")
    #     self.tree.heading("breed", text="Breed")
    #     self.tree.heading("identification_mark", text="Identification Mark")
    #     self.tree.pack(expand=True, fill=tk.BOTH)

    def add_cow(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Cow")

        tk.Label(add_window, text="Cow ID:").grid(row=0, column=0, padx=5, pady=5)
        cow_id_entry = tk.Entry(add_window)
        cow_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Gender:").grid(row=1, column=0, padx=5, pady=5)
        gender_entry = tk.Entry(add_window)
        gender_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="DOB (DD-MM-YYYY):").grid(row=2, column=0, padx=5, pady=5)
        dob_entry = tk.Entry(add_window)
        dob_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Colour:").grid(row=3, column=0, padx=5, pady=5)
        colour_entry = tk.Entry(add_window)
        colour_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Breed:").grid(row=4, column=0, padx=5, pady=5)
        breed_entry = tk.Entry(add_window)
        breed_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Identification Mark:").grid(row=5, column=0, padx=5, pady=5)
        mark_entry = tk.Entry(add_window)
        mark_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(add_window, text="Add Cow", command=lambda: self.add_cow_to_db(add_window, cow_id_entry, gender_entry, dob_entry, colour_entry, breed_entry, mark_entry)).grid(row=6, column=0, columnspan=2, padx=5, pady=10)

    def add_cow_to_db(self, add_window, cow_id_entry, gender_entry, dob_entry, colour_entry, breed_entry, mark_entry):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        cow_id = cow_id_entry.get()
        gender = gender_entry.get()
        dob = dob_entry.get()
        colour = colour_entry.get()
        breed = breed_entry.get()
        identification_mark = mark_entry.get()

        c.execute("INSERT INTO cows (cow_id, gender, dob, colour, breed, identification_mark) VALUES (?, ?, ?, ?, ?, ?)",
                  (cow_id, gender, dob, colour, breed, identification_mark))

        c.execute("INSERT INTO purchases (cow_id, date, amount, source, transactor, insured_amt) VALUES (?, '', 0, '', '', 0)",
                  (cow_id,))
        
        c.execute("""INSERT INTO milk (cow_id, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec) 
                     VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)""",
                  (cow_id,))
        
        conn.commit()
        conn.close()

        add_window.destroy()
        self.tree.delete(*self.tree.get_children())
        self.load_data()

    def edit_cow(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        cow_id = self.tree.item(selected_item[0], 'text')
        values = self.tree.item(selected_item[0], 'values')

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Cow")

        tk.Label(edit_window, text="Cow ID:").grid(row=0, column=0, padx=5, pady=5)
        cow_id_entry = tk.Entry(edit_window)
        cow_id_entry.grid(row=0, column=1, padx=5, pady=5)
        cow_id_entry.insert(0, cow_id)
        cow_id_entry.config(state='disabled')

        tk.Label(edit_window, text="Gender:").grid(row=1, column=0, padx=5, pady=5)
        gender_entry = tk.Entry(edit_window)
        gender_entry.grid(row=1, column=1, padx=5, pady=5)
        gender_entry.insert(0, values[0])

        tk.Label(edit_window, text="DOB (DD-MM-YYYY):").grid(row=2, column=0, padx=5, pady=5)
        dob_entry = tk.Entry(edit_window)
        dob_entry.grid(row=2, column=1, padx=5, pady=5)
        dob_entry.insert(0, values[1])

        tk.Label(edit_window, text="Colour:").grid(row=3, column=0, padx=5, pady=5)
        colour_entry = tk.Entry(edit_window)
        colour_entry.grid(row=3, column=1, padx=5, pady=5)
        colour_entry.insert(0, values[2])

        tk.Label(edit_window, text="Breed:").grid(row=4, column=0, padx=5, pady=5)
        breed_entry = tk.Entry(edit_window)
        breed_entry.grid(row=4, column=1, padx=5, pady=5)
        breed_entry.insert(0, values[3])

        tk.Label(edit_window, text="Identification Mark:").grid(row=5, column=0, padx=5, pady=5)
        mark_entry = tk.Entry(edit_window)
        mark_entry.grid(row=5, column=1, padx=5, pady=5)
        mark_entry.insert(0, values[4])

        tk.Button(edit_window, text="Update Cow", command=lambda: self.update_cow_in_db(edit_window, cow_id, gender_entry, dob_entry, colour_entry, breed_entry, mark_entry)).grid(row=6, column=0, columnspan=2, padx=5, pady=10)

    def update_cow_in_db(self, edit_window, cow_id, gender_entry, dob_entry, colour_entry, breed_entry, mark_entry):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        gender = gender_entry.get()
        dob = dob_entry.get()
        colour = colour_entry.get()
        breed = breed_entry.get()
        identification_mark = mark_entry.get()

        c.execute("""UPDATE cows
                     SET gender = ?, dob = ?, colour = ?, breed = ?, identification_mark = ?
                     WHERE cow_id = ?""",
                  (gender, dob, colour, breed, identification_mark, cow_id))

        conn.commit()
        conn.close()

        edit_window.destroy()
        self.tree.delete(*self.tree.get_children())
        self.load_data()

    def delete_cow(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        cow_id = self.tree.item(selected_item[0], 'text')

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        c.execute("DELETE FROM cows WHERE cow_id = ?", (cow_id,))

        conn.commit()
        conn.close()

        self.tree.delete(selected_item[0])

    def load_data(self):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        c.execute("SELECT * FROM cows")
        rows = c.fetchall()

        for row in rows:
            self.tree.insert("", "end", text=row[0], values=row[1:])

        conn.close()
