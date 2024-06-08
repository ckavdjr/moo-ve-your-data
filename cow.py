import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt


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
        ttk.Button(btn_frame, text="Show Medical History", command=self.show_medical_history).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Transaction Details", command=self.show_transaction_details).grid(row=0, column=4, padx=5)
        ttk.Button(btn_frame, text="Deliveries", command=self.show_delivered_calves).grid(row=0, column=5, padx=5)
        ttk.Button(btn_frame, text="Milk Production", command=self.show_milk_production).grid(row=0, column=6, padx=5)


    def load_data(self):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        c.execute("SELECT * FROM cows")
        rows = c.fetchall()

        for row in rows:
            self.tree.insert("", "end", text=row[0], values=row[1:])

        conn.close()


    def add_cow(self):
        # Create a new window for adding a cow
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Cow")

        # Create labels and entry fields for input
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

        # Button to confirm adding cow
        tk.Button(add_window, text="Add Cow", command=lambda: self.add_cow_to_db(add_window, cow_id_entry, gender_entry, dob_entry, colour_entry, breed_entry, mark_entry)).grid(row=6, column=0, columnspan=2, padx=5, pady=10)

    def add_cow_to_db(self, add_window, cow_id_entry, gender_entry, dob_entry, colour_entry, breed_entry, mark_entry):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        # Retrieve values from entry fields
        cow_id = cow_id_entry.get()
        gender = gender_entry.get()
        dob = dob_entry.get()
        colour = colour_entry.get()
        breed = breed_entry.get()
        identification_mark = mark_entry.get()

        # Insert values into the database
        c.execute("INSERT INTO cows (cow_id, gender, dob, colour, breed, identification_mark) VALUES (?, ?, ?, ?, ?, ?)",
                (cow_id, gender, dob, colour, breed, identification_mark))

        # Insert an empty transaction into the purchases table
        c.execute("INSERT INTO purchases (cow_id, date, amount, source, transactor, insured_amt) VALUES (?, '', 0, '', '', 0)",
                (cow_id,))
        
        # Insert an empty milk production record into the milk table
        c.execute("""INSERT INTO milk (cow_id, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec) 
            VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)""",
                (cow_id,))
        
        conn.commit()
        conn.close()

        # Close the add window
        add_window.destroy()

        # Refresh the data in the treeview
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

        # Create labels and entry fields pre-filled with existing values
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

        # Button to confirm editing cow
        tk.Button(edit_window, text="Update Cow", command=lambda: self.update_cow_in_db(edit_window, cow_id, gender_entry, dob_entry, colour_entry, breed_entry, mark_entry)).grid(row=6, column=0, columnspan=2, padx=5, pady=10)

    def update_cow_in_db(self, edit_window, cow_id, gender_entry, dob_entry, colour_entry, breed_entry, mark_entry):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        # Retrieve values from entry fields
        gender = gender_entry.get()
        dob = dob_entry.get()
        colour = colour_entry.get()
        breed = breed_entry.get()
        identification_mark = mark_entry.get()

        # Update values in the database
        c.execute("""UPDATE cows
                     SET gender = ?, dob = ?, colour = ?, breed = ?, identification_mark = ?
                     WHERE cow_id = ?""",
                  (gender, dob, colour, breed, identification_mark, cow_id))

        conn.commit()
        conn.close()

        # Close the edit window
        edit_window.destroy()

        # Refresh the data in the treeview
        self.tree.delete(*self.tree.get_children())
        self.load_data()

    def delete_cow(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        cow_id = self.tree.item(selected_item[0], 'text')

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        # Delete the selected cow from the database
        c.execute("DELETE FROM cows WHERE cow_id = ?", (cow_id,))

        conn.commit()
        conn.close()

        # Remove the selected item from the treeview
        self.tree.delete(selected_item[0])


    def show_medical_history(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        cow_id = self.tree.item(selected_item[0], 'text')

        # Create a new window to show the medical history
        history_window = tk.Toplevel(self.root)
        history_window.title("Medical History")

        # Treeview for diseases
        disease_frame = ttk.Frame(history_window)
        disease_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        disease_tree = ttk.Treeview(disease_frame, columns=("disease", "date"))
        disease_tree.heading("#0", text="ID")
        disease_tree.heading("disease", text="Disease")
        disease_tree.heading("date", text="Date")
        disease_tree.pack(expand=True, fill=tk.BOTH)

        # Buttons for diseases
        disease_btn_frame = ttk.Frame(disease_frame)
        disease_btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(disease_btn_frame, text="Add Disease", command=lambda: self.add_medical(cow_id, disease_tree, "Disease")).pack(side=tk.LEFT, padx=5)
        ttk.Button(disease_btn_frame, text="Edit Disease", command=lambda: self.edit_medical(cow_id, disease_tree, "Disease")).pack(side=tk.LEFT, padx=5)
        ttk.Button(disease_btn_frame, text="Delete Disease", command=lambda: self.delete_medical(disease_tree, "Disease")).pack(side=tk.LEFT, padx=5)

        # Treeview for vaccinations
        vaccination_frame = ttk.Frame(history_window)
        vaccination_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        vaccination_tree = ttk.Treeview(vaccination_frame, columns=("vaccination", "date"))
        vaccination_tree.heading("#0", text="ID")
        vaccination_tree.heading("vaccination", text="Vaccination")
        vaccination_tree.heading("date", text="Date")
        vaccination_tree.pack(expand=True, fill=tk.BOTH)

        # Buttons for vaccinations
        vaccination_btn_frame = ttk.Frame(vaccination_frame)
        vaccination_btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(vaccination_btn_frame, text="Add Vaccination", command=lambda: self.add_medical(cow_id, vaccination_tree, "Vaccination")).pack(side=tk.LEFT, padx=5)
        ttk.Button(vaccination_btn_frame, text="Edit Vaccination", command=lambda: self.edit_medical(cow_id, vaccination_tree, "Vaccination")).pack(side=tk.LEFT, padx=5)
        ttk.Button(vaccination_btn_frame, text="Delete Vaccination", command=lambda: self.delete_medical(vaccination_tree, "Vaccination")).pack(side=tk.LEFT, padx=5)

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        # Retrieve diseases
        c.execute("SELECT disease_id, disease, date FROM diseases WHERE cow_id = ?", (cow_id,))
        disease_rows = c.fetchall()
        for row in disease_rows:
            disease_tree.insert("", "end", text=row[0], values=row[1:])

        # Retrieve vaccinations
        c.execute("SELECT vaccination_id, vaccination, date FROM vaccinations WHERE cow_id = ?", (cow_id,))
        vaccination_rows = c.fetchall()
        for row in vaccination_rows:
            vaccination_tree.insert("", "end", text=row[0], values=row[1:])

        conn.close()

    def add_medical(self, cow_id, tree, medical_type):
        add_window = tk.Toplevel(self.root)
        add_window.title(f"Add {medical_type}")

        tk.Label(add_window, text=medical_type).grid(row=0, column=0, padx=5, pady=5)
        medical_entry = tk.Entry(add_window)
        medical_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(add_window, text="Add", command=lambda: self.add_medical_to_db(add_window, cow_id, medical_entry, date_entry, tree, medical_type)).grid(row=2, column=0, columnspan=2, pady=10)

    def add_medical_to_db(self, add_window, cow_id, medical_entry, date_entry, tree, medical_type):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        medical = medical_entry.get()
        date = date_entry.get()

        c.execute(f"INSERT INTO {medical_type}s (cow_id, {medical_type}, date) VALUES (?, ?, ?)", (cow_id, medical, date))

        conn.commit()
        conn.close()

        add_window.destroy()
        tree.insert("", "end", values=(medical, date))

    def edit_medical(self, cow_id, tree, medical_type):
        selected_item = tree.selection()
        if not selected_item:
            return
        
        medical_id = tree.item(selected_item[0], 'text')

        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit {medical_type}")

        tk.Label(edit_window, text=f"{medical_type}:").grid(row=0, column=0, padx=5, pady=5)
        medical_entry = tk.Entry(edit_window)
        medical_entry.grid(row=0, column=1, padx=5, pady=5)
        medical_entry.insert(0, tree.item(selected_item[0], 'values')[0])

        tk.Label(edit_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        date_entry = tk.Entry(edit_window)
        date_entry.grid(row=1, column=1, padx=5, pady=5)
        date_entry.insert(0, tree.item(selected_item[0], 'values')[1])

        tk.Button(edit_window, text="Update", command=lambda: self.edit_medical_in_db(edit_window, medical_id, medical_entry, date_entry, tree, selected_item, medical_type)).grid(row=2, column=0, columnspan=2, pady=10)

    def edit_medical_in_db(self, edit_window, medical_id, medical_entry, date_entry, tree, selected_item, medical_type):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        medical = medical_entry.get()
        date = date_entry.get()

        c.execute(f"UPDATE {medical_type}s SET {medical_type} = ?, date = ? WHERE {medical_type}_id = ?", (medical, date, medical_id))

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


    def show_transaction_details(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        cow_id = self.tree.item(selected_item[0], 'text')

        # Create a new window to show the transaction details
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("Transaction Details")

        # Create a Treeview to display transactions
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

        ttk.Button(btn_frame, text="Edit Transaction", command=lambda: self.edit_transaction(cow_id, transaction_tree)).pack(side=tk.LEFT, padx=5)

        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        # Retrieve transactions
        c.execute("SELECT purchase_id, date, amount, source, transactor, insured_amt FROM purchases WHERE cow_id = ?", (cow_id,))
        transaction_rows = c.fetchall()
        for row in transaction_rows:
            transaction_tree.insert("", "end", text=row[0], values=row[1:])

        conn.close()

    def edit_transaction(self, cow_id, tree):
        selected_item = tree.selection()
        if not selected_item:
            return

        transaction_id = tree.item(selected_item[0], 'text')
        values = tree.item(selected_item[0], 'values')

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Transaction")

        # Create labels and entry fields pre-filled with existing values
        tk.Label(edit_window, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        date_entry = tk.Entry(edit_window)
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        date_entry.insert(0, values[0])

        tk.Label(edit_window, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        amount_entry = tk.Entry(edit_window)
        amount_entry.grid(row=1, column=1, padx=5, pady=5)
        amount_entry.insert(0, values[1])

        tk.Label(edit_window, text="Source:").grid(row=2, column=0, padx=5, pady=5)
        source_entry = tk.Entry(edit_window)
        source_entry.grid(row=2, column=1, padx=5, pady=5)
        source_entry.insert(0, values[2])

        tk.Label(edit_window, text="Transactor:").grid(row=3, column=0, padx=5, pady=5)
        transactor_entry = tk.Entry(edit_window)
        transactor_entry.grid(row=3, column=1, padx=5, pady=5)
        transactor_entry.insert(0, values[3])

        tk.Label(edit_window, text="Insured Amount:").grid(row=4, column=0, padx=5, pady=5)
        insured_amt_entry = tk.Entry(edit_window)
        insured_amt_entry.grid(row=4, column=1, padx=5, pady=5)
        insured_amt_entry.insert(0, values[4])

        # Button to confirm editing transaction
        tk.Button(edit_window, text="Update Transaction", command=lambda: self.update_transaction_in_db(edit_window, transaction_id, date_entry, amount_entry, source_entry, transactor_entry, insured_amt_entry, tree, selected_item)).grid(row=5, column=0, columnspan=2, padx=5, pady=10)

    def update_transaction_in_db(self, edit_window, transaction_id, date_entry, amount_entry, source_entry, transactor_entry, insured_amt_entry, tree, selected_item):
        conn = sqlite3.connect("farm.db")
        c = conn.cursor()

        # Retrieve values from entry fields
        date = date_entry.get()
        amount = amount_entry.get()
        source = source_entry.get()
        transactor = transactor_entry.get()
        insured_amt = insured_amt_entry.get()

        # Update values in the database
        c.execute("""UPDATE purchases
                     SET date = ?, amount = ?, source = ?, transactor = ?, insured_amt = ?
                     WHERE purchase_id = ?""",
                  (date, amount, source, transactor, insured_amt, transaction_id))

        conn.commit()
        conn.close()

        # Close the edit window
        edit_window.destroy()

        # Update the values in the treeview
        tree.item(selected_item, values=(date, amount, source, transactor, insured_amt))


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


    def add_delivery(self, parent_id, tree):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Delivery")

        tk.Label(add_window, text="Child ID:").grid(row=0, column=0, padx=5, pady=5)
        child_id_entry = tk.Entry(add_window)
        child_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(add_window, text="Add Delivery", command=lambda: self.add_delivery_to_db(add_window, parent_id, child_id_entry, date_entry, tree)).grid(row=2, column=0, columnspan=2, pady=10)

    
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


if __name__ == "__main__":
    root = tk.Tk()
    app = FarmApp(root)
    root.mainloop()
