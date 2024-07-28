import tkinter as tk
from tkinter import ttk
import sqlite3

class TransactionManager:
    def __init__(self, root, tree):
        self.root = root
        self.tree = tree

    def show_transaction_details(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        cow_id = self.tree.item(selected_item[0], 'text')

        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("Transaction Details")

        transaction_tree = ttk.Treeview(transaction_window, columns=("date", "amount", "source", "transactor", "insured_amt"))
        transaction_tree.heading("#0", text="")
        transaction_tree.column("#0", width=0, stretch=tk.NO)
        transaction_tree.heading("date", text="Date")
        transaction_tree.heading("amount", text="Amount")
        transaction_tree.heading("source", text="Source")
        transaction_tree.heading("transactor", text="Transactor")
        transaction_tree.heading("insured_amt", text="Insured Amount")
        transaction_tree.pack(expand=True, fill=tk.BOTH)

        btn_frame = ttk.Frame(transaction_window)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Edit Transaction", command=lambda: self.edit_transaction(transaction_tree)).pack(side=tk.LEFT, padx=5)

        self.load_transaction_data(self, cow_id, transaction_tree)

    def load_transaction_data(self, cow_id, transaction_tree):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute("""SELECT date, amount, source, transactor, insured_amt
                    FROM purchases
                    WHERE cow_id = ?""", 
                      (cow_id,))
        rows = c.fetchall()
        for row in rows:
            transaction_tree.insert("", "end", values=row)
        conn.close()

    def edit_transaction(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            return

        transaction_id = tree.item(selected_item[0], 'text')
        values = tree.item(selected_item[0], 'values')

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Transaction")

        ttk.Label(edit_window, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        date_entry = tk.Entry(edit_window)
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        date_entry.insert(0, values[0])

        ttk.Label(edit_window, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        amount_entry = tk.Entry(edit_window)
        amount_entry.grid(row=1, column=1, padx=5, pady=5)
        amount_entry.insert(0, values[1])

        ttk.Label(edit_window, text="Source:").grid(row=2, column=0, padx=5, pady=5)
        source_entry = tk.Entry(edit_window)
        source_entry.grid(row=2, column=1, padx=5, pady=5)
        source_entry.insert(0, values[2])

        ttk.Label(edit_window, text="Transactor:").grid(row=3, column=0, padx=5, pady=5)
        transactor_entry = tk.Entry(edit_window)
        transactor_entry.grid(row=3, column=1, padx=5, pady=5)
        transactor_entry.insert(0, values[3])

        ttk.Label(edit_window, text="Insured Amount:").grid(row=4, column=0, padx=5, pady=5)
        insured_amt_entry = tk.Entry(edit_window)
        insured_amt_entry.grid(row=4, column=1, padx=5, pady=5)
        insured_amt_entry.insert(0, values[4])

        ttk.Button(edit_window, text="Update Transaction", command=lambda: self.update_transaction_in_db(edit_window, transaction_id, date_entry, amount_entry, source_entry, transactor_entry, insured_amt_entry, tree, selected_item)).grid(row=5, column=0, columnspan=2, padx=5, pady=10)

    def update_transaction_in_db(self, edit_window, transaction_id, date_entry, amount_entry, source_entry, transactor_entry, insured_amt_entry, tree, selected_item):
        date = date_entry.get()
        amount = amount_entry.get()
        source = source_entry.get()
        transactor = transactor_entry.get()
        insured_amt = insured_amt_entry.get()

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()
        c.execute("""UPDATE purchases
                    SET date = ?, amount = ?, source = ?, transactor = ?, insured_amt = ?
                    WHERE purchase_id = ?""",
                  (date, amount, source, transactor, insured_amt, transaction_id))
        conn.commit()
        conn.close()

        edit_window.destroy()

        tree.item(selected_item, values=(date, amount, source, transactor, insured_amt))
