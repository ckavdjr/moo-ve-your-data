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

        milk_tree = ttk.Treeview(milk_window, columns=("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"))
        milk_tree.heading("#0", text="")
        milk_tree.column("#0", width=0, stretch=tk.NO)

        milk_tree.heading("jan", text="Jan")
        milk_tree.heading("feb", text="Feb")
        milk_tree.heading("mar", text="Mar")
        milk_tree.heading("apr", text="Apr")
        milk_tree.heading("may", text="May")
        milk_tree.heading("jun", text="Jun")
        milk_tree.heading("jul", text="Jul")
        milk_tree.heading("aug", text="Aug")
        milk_tree.heading("sep", text="Sep")
        milk_tree.heading("oct", text="Oct")
        milk_tree.heading("nov", text="Nov")
        milk_tree.heading("dec", text="Dec")

        window_width = milk_window.winfo_screenwidth()
        column_width = int(window_width / 12)
        milk_tree.column("jan", width=column_width, stretch=tk.NO)
        milk_tree.column("feb", width=column_width, stretch=tk.NO)
        milk_tree.column("mar", width=column_width, stretch=tk.NO)
        milk_tree.column("apr", width=column_width, stretch=tk.NO)
        milk_tree.column("may", width=column_width, stretch=tk.NO)
        milk_tree.column("jun", width=column_width, stretch=tk.NO)
        milk_tree.column("jul", width=column_width, stretch=tk.NO)
        milk_tree.column("aug", width=column_width, stretch=tk.NO)
        milk_tree.column("sep", width=column_width, stretch=tk.NO)
        milk_tree.column("oct", width=column_width, stretch=tk.NO)
        milk_tree.column("nov", width=column_width, stretch=tk.NO)
        milk_tree.column("dec", width=column_width, stretch=tk.NO)

        milk_tree.pack(expand=True, fill=tk.BOTH)

        milk_btn_frame = ttk.Frame(milk_window)
        milk_btn_frame.pack(pady=5)

        ttk.Button(milk_btn_frame, text="Edit Milk Production", command=lambda: self.edit_milk_production(cow_id, milk_tree)).grid(row=0, column=0, padx=10)
        ttk.Button(milk_btn_frame, text="Show Graph", command=lambda: self.plot_milk_production(cow_id)).grid(row=0, column=1, padx=10)

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        c.execute("SELECT jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec FROM milk WHERE cow_id = ?", (cow_id,))
        rows = c.fetchall()
        for row in rows:
            milk_tree.insert("", "end", text=cow_id, values=row)

        conn.close()

    def edit_milk_production(self, cow_id, milk_tree):
        selected_item = milk_tree.selection()
        if not selected_item:
            return

        values = milk_tree.item(selected_item[0], 'values')

        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Milk Production")

        months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        entries = {}

        for i, month in enumerate(months):
            tk.Label(edit_window, text=f"{month.capitalize()}:").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, values[i] if i < len(values) else 0)
            entries[month] = entry

        tk.Button(edit_window, text="Update", command=lambda: self.update_milk_production(cow_id, entries, edit_window, milk_tree)).grid(row=len(months), column=0, columnspan=2, pady=10)

    def update_milk_production(self, cow_id, entries, edit_window, milk_tree):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        updates = {month: entries[month].get() for month in entries}

        c.execute("""
            UPDATE milk SET
            jan = ?, feb = ?, mar = ?, apr = ?, may = ?, jun = ?, jul = ?, aug = ?, sep = ?, oct = ?, nov = ?, dec = ?
            WHERE cow_id = ?
        """, (*updates.values(), cow_id))

        conn.commit()
        conn.close()

        # Update the values in milk_tree
        selected_item = milk_tree.selection()[0]
        milk_tree.item(selected_item, values=tuple(updates.values()))

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
