import tkinter as tk
from tkinter import ttk
import sqlite3

class MedicalManager:
    def __init__(self, root, tree):
        self.root = root
        self.tree = tree

    def show_medical_history(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        cow_id = self.tree.item(selected_item[0], 'text')

        history_window = tk.Toplevel(self.root)
        history_window.title("Medical History")

        # Diseases
        disease_frame = ttk.Frame(history_window)
        disease_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        disease_tree = ttk.Treeview(disease_frame, columns=("disease", "date"))
        disease_tree.heading("#0", text="ID")
        disease_tree.column("#0", width=0, stretch=tk.NO)
        disease_tree.heading("disease", text="Disease")
        disease_tree.heading("date", text="Date")
        disease_tree.pack(expand=True, fill=tk.BOTH)

        disease_btn_frame = ttk.Frame(disease_frame)
        disease_btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(disease_btn_frame, text="Add Disease", command=lambda: self.add_medical(cow_id, disease_tree, "Disease")).pack(side=tk.LEFT, padx=5)
        ttk.Button(disease_btn_frame, text="Edit Disease", command=lambda: self.edit_medical(disease_tree, "Disease")).pack(side=tk.LEFT, padx=5)
        ttk.Button(disease_btn_frame, text="Delete Disease", command=lambda: self.delete_medical(disease_tree, "Disease")).pack(side=tk.LEFT, padx=5)

        # Vaccinations
        vaccination_frame = ttk.Frame(history_window)
        vaccination_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        vaccination_tree = ttk.Treeview(vaccination_frame, columns=("vaccination", "date"))
        vaccination_tree.heading("#0", text="ID")
        vaccination_tree.column("#0", width=0, stretch=tk.NO)
        vaccination_tree.heading("vaccination", text="Vaccination")
        vaccination_tree.heading("date", text="Date")
        vaccination_tree.pack(expand=True, fill=tk.BOTH)

        vaccination_btn_frame = ttk.Frame(vaccination_frame)
        vaccination_btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(vaccination_btn_frame, text="Add Vaccination", command=lambda: self.add_medical(cow_id, vaccination_tree, "Vaccination")).pack(side=tk.LEFT, padx=5)
        ttk.Button(vaccination_btn_frame, text="Edit Vaccination", command=lambda: self.edit_medical(vaccination_tree, "Vaccination")).pack(side=tk.LEFT, padx=5)
        ttk.Button(vaccination_btn_frame, text="Delete Vaccination", command=lambda: self.delete_medical(vaccination_tree, "Vaccination")).pack(side=tk.LEFT, padx=5)

        self.load_medical_history(cow_id, disease_tree, vaccination_tree)

    def load_medical_history(self, cow_id, disease_tree, vaccination_tree):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        c.execute("SELECT disease_id, disease, date FROM diseases WHERE cow_id = ?", (cow_id,))
        disease_rows = c.fetchall()
        for row in disease_rows:
            disease_tree.insert("", "end", text=row[0], values=row[1:])

        c.execute("SELECT vaccination_id, vaccination, date FROM vaccinations WHERE cow_id = ?", (cow_id,))
        vaccination_rows = c.fetchall()
        for row in vaccination_rows:
            vaccination_tree.insert("", "end", text=row[0], values=row[1:])

        conn.close()

    def add_medical(self, cow_id, tree, medical_type):
        add_window = tk.Toplevel(self.root)
        add_window.title(f"Add {medical_type}")

        ttk.Label(add_window, text=medical_type).grid(row=0, column=0, padx=5, pady=5)
        medical_entry = tk.Entry(add_window)
        medical_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(add_window, text="Add", command=lambda: self.add_medical_to_db(add_window, cow_id, medical_entry, date_entry, tree, medical_type)).grid(row=2, column=0, columnspan=2, pady=10)

    def add_medical_to_db(self, add_window, cow_id, medical_entry, date_entry, tree, medical_type):
        medical = medical_entry.get()
        date = date_entry.get()

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute(f"""INSERT INTO {medical_type}s (cow_id, {medical_type}, date) 
                    VALUES (?, ?, ?)""",
                      (cow_id, medical, date))
        conn.commit()
        conn.close()

        add_window.destroy()
        tree.insert("", "end", values=(medical, date))

    def edit_medical(self, tree, medical_type):
        selected_item = tree.selection()
        if not selected_item:
            return
        
        medical_id = tree.item(selected_item[0], 'text')
        values = tree.item(selected_item[0], 'values')

        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit {medical_type}")

        ttk.Label(edit_window, text=f"{medical_type}:").grid(row=0, column=0, padx=5, pady=5)
        medical_entry = tk.Entry(edit_window)
        medical_entry.grid(row=0, column=1, padx=5, pady=5)
        medical_entry.insert(0, values[0])

        ttk.Label(edit_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        date_entry = tk.Entry(edit_window)
        date_entry.grid(row=1, column=1, padx=5, pady=5)
        date_entry.insert(0, values[1])

        ttk.Button(edit_window, text="Update", command=lambda: self.update_medical_in_db(edit_window, medical_id, medical_entry, date_entry, tree, selected_item, medical_type)).grid(row=2, column=0, columnspan=2, pady=10)

    def update_medical_in_db(self, edit_window, medical_id, medical_entry, date_entry, tree, selected_item, medical_type):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        medical = medical_entry.get()
        date = date_entry.get()

        c.execute(f"""UPDATE {medical_type}s
                    SET {medical_type} = ?, date = ?
                    WHERE {medical_type}_id = ?""", 
                      (medical, date, medical_id))
        conn.commit()
        conn.close()

        edit_window.destroy()

        tree.item(selected_item, values=(medical, date))

    def delete_medical(self, tree, medical_type):
        selected_item = tree.selection()
        if not selected_item:
            return

        medical_id = tree.item(selected_item[0], 'text')

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute(f"DELETE FROM {medical_type}s WHERE {medical_type}_id = ?", (medical_id,))
        conn.commit()
        conn.close()
        
        tree.delete(selected_item[0])