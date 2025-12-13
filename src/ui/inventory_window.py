import tkinter as tk
from tkinter import ttk, messagebox

class InventoryWindow:
    def __init__(self, parent, inventory, update_callback):
        self.inventory = inventory
        self.update_callback = update_callback
        self.window = tk.Toplevel(parent)
        self.window.title("View Inventory")
        self.window.geometry("1000x600")
        self.create_widgets()
        self.load_products()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Sort options
        ttk.Label(controls_frame, text="Sort by:").pack(side=tk.LEFT, padx=5)
        self.sort_var = tk.StringVar(value="name")
        sort_options = [
            ("Name", "name"),
            ("Stock Level", "stock"),
            ("Expiry Date", "expiry"),
            ("Price", "price")
        ]
        for text, value in sort_options:
            ttk.Radiobutton(
                controls_frame,
                text=text,
                variable=self.sort_var,
                value=value,
                command=self.load_products
            ).pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        ttk.Button(
            controls_frame,
            text="🔄 Refresh",
            command=self.load_products
        ).pack(side=tk.RIGHT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_products)
        ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30
        ).pack(side=tk.LEFT, padx=5)
        
        # Treeview frame
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        columns = ('id', 'name', 'category', 'stock', 'price', 'expiry', 'supplier')
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Configure columns
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('category', text='Category')
        self.tree.heading('stock', text='Stock')
        self.tree.heading('price', text='Price')
        self.tree.heading('expiry', text='Expiry Date')
        self.tree.heading('supplier', text='Supplier')
        
        self.tree.column('id', width=80)
        self.tree.column('name', width=150)
        self.tree.column('category', width=120)
        self.tree.column('stock', width=80)
        self.tree.column('price', width=100)
        self.tree.column('expiry', width=100)
        self.tree.column('supplier', width=120)
        
        # Configure scrollbars
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double-click to edit
        self.tree.bind('<Double-Button-1>', self.edit_product)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            buttons_frame,
            text="Edit Selected",
            command=self.edit_product
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Close",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
    def load_products(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get sort option
        sort_by = self.sort_var.get()
        if sort_by == "name":
            products = sorted(self.inventory.products, key=lambda p: p.name)
        elif sort_by == "stock":
            products = sorted(self.inventory.products, key=lambda p: p.quantity)
        elif sort_by == "expiry":
            products = self.inventory.get_products_sorted_by_expiry()
        elif sort_by == "price":
            products = sorted(self.inventory.products, key=lambda p: p.unit_price)
        else:
            products = self.inventory.products
        
        for product in products:
            tags = ()
            if product.quantity == 0:
                tags = ('out_of_stock',)
            elif product.quantity < 30:
                tags = ('low_stock',)
            
            self.tree.insert('', tk.END, values=(
                product.product_id,
                product.name,
                product.category,
                product.quantity,
                f"FCFA {product.unit_price:.2f}",
                product.expiry_date,
                product.supplier
            ), tags=tags)
        
        # Configure tag colors
        self.tree.tag_configure('low_stock', background='#FFF3CD')
        self.tree.tag_configure('out_of_stock', background='#F8D7DA')
    
    def filter_products(self, *args):
        search_term = self.search_var.get().lower()
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter and display
        for product in self.inventory.products:
            if (search_term in product.name.lower() or
                search_term in product.category.lower() or
                search_term in product.product_id.lower()):
                
                tags = ()
                if product.quantity == 0:
                    tags = ('out_of_stock',)
                elif product.quantity < 30:
                    tags = ('low_stock',)
                
                self.tree.insert('', tk.END, values=(
                    product.product_id,
                    product.name,
                    product.category,
                    product.quantity,
                    f"FCFA {product.unit_price:.2f}",
                    product.expiry_date,
                    product.supplier
                ), tags=tags)
    
    def edit_product(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return
        
        # Get selected product
        item = self.tree.item(selection[0])
        product_id = item['values'][0]
        
        # Find product object
        product = None
        for p in self.inventory.products:
            if p.product_id == product_id:
                product = p
                break
        
        if not product:
            return
        
        # Create edit dialog
        EditProductDialog(self.window, product, self.inventory, self.load_products, self.update_callback)


class EditProductDialog:
    def __init__(self, parent, product, inventory, reload_callback, update_callback):
        self.product = product
        self.inventory = inventory
        self.reload_callback = reload_callback
        self.update_callback = update_callback
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Edit Product - {product.name}")
        self.dialog.geometry("400x300")
        self.dialog.grab_set()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Product name (read-only)
        ttk.Label(main_frame, text=f"Product: {self.product.name}", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 20))
        
        # Quantity
        qty_frame = ttk.Frame(main_frame)
        qty_frame.pack(fill=tk.X, pady=10)
        ttk.Label(qty_frame, text="Quantity:").pack(side=tk.LEFT, padx=5)
        self.qty_var = tk.IntVar(value=self.product.quantity)
        ttk.Spinbox(
            qty_frame,
            from_=0,
            to=10000,
            textvariable=self.qty_var,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Price
        price_frame = ttk.Frame(main_frame)
        price_frame.pack(fill=tk.X, pady=10)
        ttk.Label(price_frame, text="Price ( FCFA ):").pack(side=tk.LEFT, padx=5)
        self.price_var = tk.IntVar(value=self.product.unit_price)
        ttk.Entry(
            price_frame,
            textvariable=self.price_var,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Display dollar amount
        self.dollar_label = ttk.Label(
            price_frame,
            text=f"FCFA {self.product.unit_price:.2f}"
        )
        self.dollar_label.pack(side=tk.LEFT, padx=5)
        
        # Update dollar label on price change
        self.price_var.trace('w', self.update_dollar_label)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, pady=20)
        
        ttk.Button(
            button_frame,
            text="Save",
            command=self.save
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def update_dollar_label(self, *args):
        try:
            price = self.price_var.get()
            self.dollar_label.config(text=f"FCFA {price:.2f}")
        except:
            pass
    
    def save(self):
        try:
            new_qty = self.qty_var.get()
            new_price = self.price_var.get()
            
            if new_qty < 0 or new_price < 0:
                messagebox.showerror("Error", "Values cannot be negative")
                return
            
            # Update product
            self.product.quantity = new_qty
            self.product.unit_price = new_price
            
            # Save inventory
            self.inventory.save_products()
            
            # Update displays
            if self.reload_callback:
                self.reload_callback()
            if self.update_callback:
                self.update_callback()
            
            messagebox.showinfo("Success", "Product updated successfully!")
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {e}")
            
    def delete_product(self):
        selection = self.tree.selection()
        if not selection:
          return
        product_id = self.tree.item(selection[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete this product?"):
           if self.inventory.delete_product(product_id):
             self.load_products()
             messagebox.showinfo("Success", "Product deleted")
             ttk.Button(
                        buttons_frame,
                        text="Delete Selected",
                        command=self.delete_product
                    ).pack(side=tk.LEFT, padx=5)