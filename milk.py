import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt

class MilkManager:
    def __init__(self, root, tree):
        self.root = root
        self.tree = tree

    def show_milk_production(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        cow_id = self.tree.item(selected_item[0], 'text')

        milk_window = tk.Toplevel(self.root)
        milk_window.title(f"Milk Production of Cow {cow_id}") 

        months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

        milk_tree = ttk.Treeview(milk_window, columns=months)
        
        window_width = milk_window.winfo_screenwidth()
        column_width = int(window_width / 12)

        milk_tree.heading("#0", text="")
        milk_tree.column("#0", width=0, stretch=tk.NO)

        for month in months:
            milk_tree.heading(month, text=month.capitalize())
            milk_tree.column(month, width=column_width, stretch=tk.NO)

        milk_tree.pack(expand=True, fill=tk.BOTH)

        milk_btn_frame = ttk.Frame(milk_window)
        milk_btn_frame.pack(pady=5)

        ttk.Button(milk_btn_frame, text="Edit Milk Production", command=lambda: self.edit_milk_production(cow_id, milk_tree)).grid(row=0, column=0, padx=10)
        ttk.Button(milk_btn_frame, text="Show Graph", command=lambda: self.plot_milk_production(cow_id)).grid(row=0, column=1, padx=10)

        self.load_milk_data(cow_id, milk_tree)

    def load_milk_data(self, cow_id, milk_tree):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute("""SELECT jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec 
                    FROM milk 
                    WHERE cow_id = ?""", 
                      (cow_id,))
        rows = c.fetchall()
        for row in rows:
            milk_tree.insert("", "end", values=row)
        conn.close()

    def edit_milk_production(self, cow_id, tree):
        selected_item = tree.selection()
        if not selected_item:
            return

        values = tree.item(selected_item[0], 'values')

        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Milk Production")

        months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        entries = {}

        for i, month in enumerate(months):
            ttk.Label(edit_window, text=f"{month.capitalize()}:").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, values[i] if i < len(values) else 0)  # TODO: Condition removal
            entries[month] = entry

        ttk.Button(edit_window, text="Update", command=lambda: self.update_milk_production_in_db(cow_id, entries, edit_window, tree)).grid(row=len(months), column=0, columnspan=2, pady=10)

    def update_milk_production_in_db(self, cow_id, entries, edit_window, tree):
        updates = {month: entries[month].get() for month in entries}
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute("""UPDATE milk SET
                    jan = ?, feb = ?, mar = ?, apr = ?, may = ?, jun = ?, jul = ?, aug = ?, sep = ?, oct = ?, nov = ?, dec = ?
                    WHERE cow_id = ?""", 
                  (*updates.values(), cow_id))
        conn.commit()
        conn.close()

        selected_item = tree.selection()[0]
        tree.item(selected_item, values=tuple(updates.values()))

        edit_window.destroy()

    def plot_milk_production(self, cow_id):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute("SELECT jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec FROM milk WHERE cow_id = ?", (cow_id,))
        row = c.fetchone()
        conn.close()

        if row:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            milk_production = list(row)

            plt.figure(figsize=(10, 5))
            plt.plot(months, milk_production, marker='o')
            plt.title(f"Milk Production for Cow {cow_id}")
            plt.xlabel("Month")
            plt.ylabel("Milk Production (liters)")
            plt.grid(True)
            plt.show()
