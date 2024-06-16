import tkinter as tk
from tkinter import ttk
import sqlite3

class DeliveryManager:
    def __init__(self, root, tree):
        self.root = root
        self.tree = tree

    def show_delivered_calves(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        cow_id = self.tree.item(selected_item[0], 'text')

        delivery_window = tk.Toplevel(self.root)
        delivery_window.title(f"Delivered Calves of Cow {cow_id}")

        delivery_tree = ttk.Treeview(delivery_window, columns=("parent_id", "child_id"))
        delivery_tree.heading("#0", text="")
        delivery_tree.column("#0", width=0, stretch=tk.NO)
        delivery_tree.heading("parent_id", text="Parent ID")
        delivery_tree.column("parent_id", stretch=tk.YES)
        delivery_tree.heading("child_id", text="Child ID")
        delivery_tree.column("child_id", stretch=tk.YES)
        delivery_tree.pack(expand=True, fill=tk.BOTH)

        delivery_btn_frame = ttk.Frame(delivery_window)
        delivery_btn_frame.pack(pady=5)

        ttk.Button(delivery_btn_frame, text="Add Delivery", command=lambda: self.add_delivery(cow_id, delivery_tree)).grid(row=0, column=0, padx=10)
        ttk.Button(delivery_btn_frame, text="Edit Delivery", command=lambda: self.edit_delivery(delivery_tree)).grid(row=0, column=1, padx=10)
        ttk.Button(delivery_btn_frame, text="Delete Delivery", command=lambda: self.delete_delivery(delivery_tree)).grid(row=0, column=2, padx=10)

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        c.execute("""SELECT parent_id, child_id 
                    FROM deliveries
                    WHERE parent_id = ?""", 
                      (cow_id,))
        rows = c.fetchall()

        for row in rows:
            delivery_tree.insert("", "end", values=row)

        conn.close()

    def add_delivery(self, cow_id, tree):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Delivery")

        ttk.Label(add_window, text="Child ID:").grid(row=0, column=0, padx=10, pady=10)
        child_id_entry = ttk.Entry(add_window)
        child_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(add_window, text="Save", command=lambda: self.add_delivery_to_db(add_window, cow_id, child_id_entry, tree)).grid(row=1, column=0, columnspan=2, pady=10)

    def add_delivery_to_db(self, add_window, cow_id, child_id_entry, tree):
        child_id = child_id_entry.get()

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute("""INSERT INTO deliveries (parent_id, child_id) 
                    VALUES (?, ?)""", 
                      (cow_id, child_id))
        conn.commit()
        conn.close()

        tree.insert("", "end", values=(cow_id, child_id))

        add_window.destroy()
        
    def edit_delivery(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            return

        delivery_id = tree.item(selected_item[0], 'text')
        values = tree.item(selected_item[0], 'values')

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Delivery")
        
        ttk.Label(edit_window, text="Child ID:").grid(row=0, column=0, padx=10, pady=10)
        child_id_entry = ttk.Entry(edit_window)
        child_id_entry.insert(0, values[1])
        child_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(edit_window, text="Save", command=lambda: self.update_delivery_in_db(edit_window, delivery_id, child_id_entry, tree, selected_item)).grid(row=1, column=0, columnspan=2, pady=10)

    def update_delivery_in_db(self, edit_window, delivery_id, child_id_entry, tree, selected_item):
        child_id = child_id_entry.get()
        
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute("""UPDATE deliveries
                    SET child_id = ?
                    WHERE delivery_id = ?""",
                      (child_id, delivery_id))
        conn.commit()
        conn.close()

        edit_window.destroy()

        tree.item(selected_item, values=(child_id,))

    def delete_delivery(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            return

        item = tree.item(selected_item)
        delivery_id = item['text']

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute("DELETE FROM deliveries WHERE delivery_id = ?", (delivery_id,))
        conn.commit()
        conn.close()
        tree.delete(selected_item)
