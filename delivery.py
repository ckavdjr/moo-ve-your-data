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
        delivery_tree.heading("child_id", text="Child ID")
        delivery_tree.pack(expand=True, fill=tk.BOTH)

        delivery_btn_frame = ttk.Frame(delivery_window)
        delivery_btn_frame.pack(pady=5)

        ttk.Button(delivery_btn_frame, text="Add Delivery", command=lambda: self.add_delivery(cow_id, delivery_tree)).grid(row=0, column=0, padx=10)
        ttk.Button(delivery_btn_frame, text="Edit Delivery", command=lambda: self.edit_delivery(delivery_tree)).grid(row=0, column=1, padx=10)
        ttk.Button(delivery_btn_frame, text="Delete Delivery", command=lambda: self.delete_delivery(delivery_tree)).grid(row=0, column=2, padx=10)

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        query = """
        SELECT parent_id, child_id 
        FROM deliveries
        WHERE parent_id = ?
        """
        c.execute(query, (cow_id,))
        rows = c.fetchall()

        for row in rows:
            delivery_tree.insert("", "end", values=row)

        conn.close()

    def add_delivery(self, cow_id, delivery_tree):
        def save_delivery():
            child_id = entry_child_id.get()
            conn = sqlite3.connect("farm.db")
            c = conn.cursor()
            c.execute("INSERT INTO deliveries (parent_id, child_id) VALUES (?, ?)", (cow_id, child_id))
            conn.commit()
            conn.close()
            delivery_tree.insert("", "end", values=(cow_id, child_id))
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Delivery")

        ttk.Label(add_window, text="Child ID:").grid(row=0, column=0, padx=10, pady=10)
        entry_child_id = ttk.Entry(add_window)
        entry_child_id.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(add_window, text="Save", command=save_delivery).grid(row=1, column=0, columnspan=2, pady=10)

    def edit_delivery(self, delivery_tree):
        selected_item = delivery_tree.selection()
        if not selected_item:
            return

        def save_edit():
            new_child_id = entry_child_id.get()
            conn = sqlite3.connect("farm.db")
            c = conn.cursor()
            c.execute("UPDATE deliveries SET child_id = ? WHERE parent_id = ? AND child_id = ?", 
                      (new_child_id, parent_id, old_child_id))

            conn.commit()
            conn.close()
            delivery_tree.item(selected_item, values=(parent_id, new_child_id))
            edit_window.destroy()

        item = delivery_tree.item(selected_item)
        parent_id, old_child_id = item['values']

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Delivery")

        ttk.Label(edit_window, text="Child ID:").grid(row=0, column=0, padx=10, pady=10)
        entry_child_id = ttk.Entry(edit_window)
        entry_child_id.insert(0, old_child_id)
        entry_child_id.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(edit_window, text="Save", command=save_edit).grid(row=1, column=0, columnspan=2, pady=10)

    def delete_delivery(self, delivery_tree):
        selected_item = delivery_tree.selection()
        if not selected_item:
            return

        item = delivery_tree.item(selected_item)
        parent_id, child_id = item['values']

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute("DELETE FROM deliveries WHERE parent_id = ? AND child_id = ?", (parent_id, child_id))
        conn.commit()
        conn.close()
        delivery_tree.delete(selected_item)
