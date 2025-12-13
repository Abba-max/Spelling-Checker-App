import tkinter as tk
from tkinter import ttk, messagebox
from models.Product import Product
from datetime import datetime

class AddProductWindow:
    def __init__(self, parent, inventory, update_callback):
        self.inventory = inventory
        self.update_callback = update_callback
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Add New Product")
        self.window.geometry("500x600")
        self.window.grab_set()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(
            main_frame, 
            text="Add New Product", 
            font=('Arial', 16, 'bold')
        ).pack(pady=(0, 20))
        
        # Product ID
        id_frame = ttk.Frame(main_frame)
        id_frame.pack(fill=tk.X, pady=10)
        ttk.Label(id_frame, text="Product ID:", width=15).pack(side=tk.LEFT, padx=5)
        self.id_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.id_var, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Label(id_frame, text="(e.g., P021)", foreground='gray').pack(side=tk.LEFT)
        
        # Product Name
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=10)
        ttk.Label(name_frame, text="Product Name:", width=15).pack(side=tk.LEFT, padx=5)
        self.name_var = tk.StringVar()
        ttk.Entry(name_frame, textvariable=self.name_var, width=30).pack(side=tk.LEFT, padx=5)
        
        # Category
        category_frame = ttk.Frame(main_frame)
        category_frame.pack(fill=tk.X, pady=10)
        ttk.Label(category_frame, text="Category:", width=15).pack(side=tk.LEFT, padx=5)
        self.category_var = tk.StringVar()
        categories = ["Electronics", "Furniture", "Clothing", "Food", "Other"]
        ttk.Combobox(
            category_frame, 
            textvariable=self.category_var, 
            values=categories,
            width=28,
            state='readonly'
        ).pack(side=tk.LEFT, padx=5)
        self.category_var.set("Electronics")
        
        # Quantity
        qty_frame = ttk.Frame(main_frame)
        qty_frame.pack(fill=tk.X, pady=10)
        ttk.Label(qty_frame, text="Quantity:", width=15).pack(side=tk.LEFT, padx=5)
        self.qty_var = tk.IntVar(value=0)
        ttk.Spinbox(
            qty_frame,
            from_=0,
            to=10000,
            textvariable=self.qty_var,
            width=28
        ).pack(side=tk.LEFT, padx=5)
        
        # Unit Price (in cents)
        price_frame = ttk.Frame(main_frame)
        price_frame.pack(fill=tk.X, pady=10)
        ttk.Label(price_frame, text="Unit Price (cents):", width=15).pack(side=tk.LEFT, padx=5)
        self.price_var = tk.IntVar(value=0)
        price_entry = ttk.Entry(price_frame, textvariable=self.price_var, width=15)
        price_entry.pack(side=tk.LEFT, padx=5)
        
        # Display dollar amount
        self.dollar_label = ttk.Label(price_frame, text="$0.00", foreground='blue')
        self.dollar_label.pack(side=tk.LEFT, padx=5)
        self.price_var.trace('w', self.update_dollar_label)
        
        # Helper text
        ttk.Label(
            main_frame, 
            text="Enter price in FCFA ",
            foreground='gray',
            font=('Arial', 9)
        ).pack(pady=(0, 10))
        
        # Expiry Date
        expiry_frame = ttk.Frame(main_frame)
        expiry_frame.pack(fill=tk.X, pady=10)
        ttk.Label(expiry_frame, text="Expiry Date:", width=15).pack(side=tk.LEFT, padx=5)
        self.expiry_var = tk.StringVar()
        expiry_entry = ttk.Entry(expiry_frame, textvariable=self.expiry_var, width=30)
        expiry_entry.pack(side=tk.LEFT, padx=5)
        
        # Set default date to one year from now
        default_date = datetime.now().replace(year=datetime.now().year + 1)
        self.expiry_var.set(default_date.strftime("%Y-%m-%d"))
        
        ttk.Label(
            main_frame, 
            text="Format: YYYY-MM-DD (e.g., 2026-12-31)",
            foreground='gray',
            font=('Arial', 9)
        ).pack(pady=(0, 10))
        
        # Supplier
        supplier_frame = ttk.Frame(main_frame)
        supplier_frame.pack(fill=tk.X, pady=10)
        ttk.Label(supplier_frame, text="Supplier:", width=15).pack(side=tk.LEFT, padx=5)
        self.supplier_var = tk.StringVar()
        ttk.Entry(supplier_frame, textvariable=self.supplier_var, width=30).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, pady=20)
        
        ttk.Button(
            button_frame,
            text="Add Product",
            command=self.add_product,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.window.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def update_dollar_label(self, *args):
        try:
            price = self.price_var.get()
            self.dollar_label.config(text=f"${price/100:.2f}")
        except:
            self.dollar_label.config(text="$0.00")
    
    def validate_date(self, date_string):
        """Validate date format YYYY-MM-DD"""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def add_product(self):
        """Add new product to inventory"""
        try:
            # Get values
            product_id = self.id_var.get().strip()
            name = self.name_var.get().strip()
            category = self.category_var.get()
            quantity = self.qty_var.get()
            unit_price = self.price_var.get()
            expiry_date = self.expiry_var.get().strip()
            supplier = self.supplier_var.get().strip()
            
            # Validate required fields
            if not product_id:
                messagebox.showerror("Error", "Product ID is required")
                return
            
            if not name:
                messagebox.showerror("Error", "Product name is required")
                return
            
            if not supplier:
                messagebox.showerror("Error", "Supplier is required")
                return
            
            # Check if product ID already exists
            for p in self.inventory.products:
                if p.product_id == product_id:
                    messagebox.showerror("Error", f"Product ID '{product_id}' already exists")
                    return
            
            # Validate quantity and price
            if quantity < 0:
                messagebox.showerror("Error", "Quantity cannot be negative")
                return
            
            if unit_price < 0:
                messagebox.showerror("Error", "Price cannot be negative")
                return
            
            # Validate expiry date
            if not self.validate_date(expiry_date):
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return
            
            # Create new product
            new_product = Product(
                product_id=product_id,
                name=name,
                unit_price=unit_price,
                quantity=quantity,
                expiry_date=expiry_date,
                supplier=supplier,
                category=category
            )
            
            # Add to inventory
            self.inventory.add_product(new_product)
            
            # Save inventory
            if self.inventory.save_products():
                messagebox.showinfo("Success", f"Product '{name}' added successfully!")
                
                # Update statistics
                if self.update_callback:
                    self.update_callback()
                
                # Close window
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save product")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {e}")