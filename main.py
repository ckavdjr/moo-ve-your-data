import os
import tkinter as tk
from tkinter import ttk

from cow import CowManager
from medical import MedicalManager
from transaction import TransactionManager
from delivery import DeliveryManager
from milk import MilkManager
from tables import create_tables


class FarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Farm Management System")
        
        self.create_main_frame()
        self.create_treeview()
        self.initialize_manager_modules()
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

    def initialize_manager_modules(self):
        self.cow_manager = CowManager(self.root, self.tree)
        self.medical_manager = MedicalManager(self.root, self.tree)
        self.transaction_manager = TransactionManager(self.root, self.tree)
        self.delivery_manager = DeliveryManager(self.root, self.tree)
        self.milk_manager = MilkManager(self.root, self.tree)

    def create_buttons(self):
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Add Cow", command=self.cow_manager.add_cow).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Edit Cow", command=self.cow_manager.edit_cow).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete Cow", command=self.cow_manager.delete_cow).grid(row=0, column=2, padx=5)
        # Other buttons...
        ttk.Button(btn_frame, text="Medical History", command=self.medical_manager.show_medical_history).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Transaction Details", command=self.transaction_manager.show_transaction_details).grid(row=0, column=4, padx=5)
        ttk.Button(btn_frame, text="Deliveries", command=self.delivery_manager.show_delivered_calves).grid(row=0, column=5, padx=5)
        ttk.Button(btn_frame, text="Milk Production", command=self.milk_manager.show_milk_production).grid(row=0, column=6, padx=5)

    def load_data(self):
        self.cow_manager.load_data()

if __name__ == "__main__":
    if not os.path.exists("farm.db"):
        create_tables()
    root = tk.Tk()
    app = FarmApp(root)
    root.mainloop()
