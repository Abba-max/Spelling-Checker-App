import tkinter as tk
from tkinter import ttk, messagebox
from ui.sale_window import SaleWindow
from ui.inventory_window import InventoryWindow
from datetime import datetime

class MainWindow:
    def __init__(self,root,inventory,worker):
        self.root = root
        self.inventory = inventory
        self.worker = worker
        
        self.root.title(f"Inventory Management System - {worker.name}") #Set Window Title and subtitle
        self.root.geometry("900x600")
        self.create_menu_bar() # Create the menu bar
        self.create_widgets() # Create the main inteface
        self.update_statistics()  # Update Statistics
        
    def create_menu_bar():
          menubar = tk.Menu(self.root)
          self.root.config(menu=menubar)

          file_menu = tk.Menu(menubar, tearoff=0)
          menubar.add_cascade(label="File", menu=file_menu)
          file_menu.add_command(label="Save Inventory", command=self.save_inventory)
          file_menu.add_separator()
          file_menu.add_command(label="Exit", command=self.root.quit)

          sales_menu = tk.Menu(menubar, tearoff=0)
          menubar.add_cascade(label="Sales", menu=sales_menu)
          sales_menu.add_command(label="New Sale", command=self.open_sale_window)
          sales_menu.add_command(label="View Receipts", command=self.view_receipts)

          inventory_menu = tk.Menu(menubar, tearoff=0)
          menubar.add_cascade(label="Inventory", menu=inventory_menu)
          inventory_menu.add_command(
              label="View All Products", 
              command=self.open_inventory_window
              )
          inventory_menu.add_command(
              label="Add New Product", 
              command=self.add_product
              )
          help_menu = tk.Menu(menubar, tearoff=0)
          menubar.add_cascade(label="Help", menu=help_menu)
          help_menu.add_command(label="About", command=self.show_about)
          
    def create_widgets():
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(
            header_frame, 
            text="Dashboard", 
            style='Header.TLabel'
).pack(side=tk.LEFT)
        ttk.Label(
            header_frame,
            text=f"Logged in as: {self.worker.name}"
).pack(side=tk.RIGHT)

        actions_frame = ttk.LabelFrame(
            main_frame, 
            text="Quick Actions", 
            padding="10"
)
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Button(
            actions_frame,
            text="📦Make Sale",
            command=self.open_sale_window,width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            actions_frame,
            text="📋View Inventory",
            command=self.open_inventory_window,width=2).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            actions_frame,
            text="💾 Save Changes",
            command=self.save_inventory,
            width=20).pack(side=tk.LEFT, padx=5)
        stats_frame = ttk.LabelFrame(
            main_frame, 
            text="Statistics", 
            padding="10"
          )
        stats_frame.pack(fill=tk.BOTH, expand=True)
        self.stats_labels = {}
        stats_info = [
            ("total_products", "Total Products:"),
            ("low_stock", "Low Stock Items:"),
            ("expiring_soon", "Expiring Soon:"),
            ("out_of_stock", "Out of Stock:")
            ]
        for i, (key, label) in enumerate(stats_info):
                frame = ttk.Frame(stats_frame)
                frame.grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=5)
                ttk.Label(frame, text=label, font=('Arial', 10, 'bold')).pack(anchor=tk.W)
                self.stats_labels[key] = ttk.Label(frame, text="0", font=('Arial', 14))
                self.stats_labels[key].pack(anchor=tk.W)
                
        
        def update_statistics():
            total = len(self.inventory.products)
            low_stock = sum(1 for p in self.inventory.products if p.quantity < 30)
            out_of_stock = sum(1 for p in self.inventory.products if p.quantity == 0)

            expiring_soon = 0
            today = datetime.now()
            for p in self.inventory.products:
                     try:
                            expiry = datetime.strptime(p.expiry_date, "%Y-%m-%d")
                            days_until_expiry = (expiry - today).days
                            if 0 <= days_until_expiry <= 7:
                                   expiring_soon += 1
                     except:
                            pass
            self.stats_labels['total_products'].config(text=str(total))
            self.stats_labels['low_stock'].config(
            text=str(low_stock), 
            foreground='#F39C12' if low_stock > 0 else '#27AE60'
            )
            self.stats_labels['expiring_soon'].config(
            text=str(expiring_soon),
            foreground='#E74C3C' if expiring_soon > 0 else '#27AE60'
            )
            self.stats_labels['out_of_stock'].config(
            text=str(out_of_stock),
            foreground='#E74C3C' if out_of_stock > 0 else '#27AE60'
            )
            
        def open_sale_window(self): # Open sale window
                SaleWindow(self.root, self.inventory, self.worker, self.update_statistics) 