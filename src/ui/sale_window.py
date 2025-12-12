import tkinter as tk
from tkinter import ttk, messagebox
from models.receipt import Receipt

class SaleWindow:
    def __init__(self, parent, inventory, worker, update_callback):
        self.inventory = inventory
        self.worker = worker
        self.update_callback = update_callback
        self.cart = []
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Make Sale")
        self.window.geometry("800x600")
        self.create_widgets()
        
        # Make modal
        self.window.grab_set()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        customer_frame = ttk.LabelFrame(
            main_frame, 
            text="Customer Information", 
            padding="10"
        )
        customer_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(customer_frame, text="Customer Name:").pack(side=tk.LEFT, padx=5)
        self.customer_entry = ttk.Entry(customer_frame, width=30)
        self.customer_entry.pack(side=tk.LEFT, padx=5)
        self.customer_entry.focus()

        search_frame = ttk.LabelFrame(
            main_frame, 
            text="Add Products", 
            padding="10"
        )
        search_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        search_controls = ttk.Frame(search_frame)
        search_controls.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_controls, text="Search Product:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        self.search_entry = ttk.Entry(
            search_controls, 
            textvariable=self.search_var,
            width=30
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)

        results_frame = ttk.Frame(search_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_listbox = tk.Listbox(
            results_frame,
            yscrollcommand=scrollbar.set,
            height=8
        )
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_listbox.yview)

        self.results_listbox.bind('<Double-Button-1>', self.add_to_cart)
        
        ttk.Button(
            search_frame,
            text="Add to Cart",
            command=self.add_to_cart
        ).pack(pady=5)
        
        cart_frame = ttk.LabelFrame(main_frame, text="Cart", padding="10")
        cart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        columns = ('product', 'quantity', 'price', 'total')
        self.cart_tree = ttk.Treeview(
            cart_frame, 
            columns=columns, 
            show='headings',
            height=6
        )
        
        self.cart_tree.heading('product', text='Product')
        self.cart_tree.heading('quantity', text='Quantity')
        self.cart_tree.heading('price', text='Unit Price')
        self.cart_tree.heading('total', text='Total')
        
        self.cart_tree.column('product', width=300)
        self.cart_tree.column('quantity', width=100)
        self.cart_tree.column('price', width=100)
        self.cart_tree.column('total', width=100)
        
        cart_scrollbar = ttk.Scrollbar(
            cart_frame, 
            orient=tk.VERTICAL,
            command=self.cart_tree.yview
        )
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)
        
        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Remove button
        ttk.Button(
            cart_frame,
            text="Remove Selected",
            command=self.remove_from_cart
        ).pack(pady=5)
        
        # Total and actions frame
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X)
        
        # Total label
        self.total_label = ttk.Label(
            bottom_frame,
            text="Total: FCFA 0.00",
            font=('Arial', 14, 'bold')
        )
        self.total_label.pack(side=tk.LEFT, padx=10)
        
        # Buttons
        ttk.Button(
            bottom_frame,
            text="Complete Sale",
            command=self.complete_sale
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            bottom_frame,
            text="Cancel",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def on_search_change(self, *args):
        """Handle search text change"""
        search_term = self.search_var.get()
        if not search_term:
            self.results_listbox.delete(0, tk.END)
            return
        
        # Search products
        matches = self.inventory.search_with_autocomplete(search_term)
        
        # Update listbox
        self.results_listbox.delete(0, tk.END)
        for product in matches:
            display_text = f"{product.name} - Stock: {product.quantity} - FCFA {product.unit_price:.2f}"
            self.results_listbox.insert(tk.END, display_text)
        
        # Store matches for reference
        self.current_matches = matches
    
    def add_to_cart(self, event=None):
        """Add selected product to cart"""
        selection = self.results_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        if not hasattr(self, 'current_matches') or idx >= len(self.current_matches):
            return
        
        product = self.current_matches[idx]
        
        # Ask for quantity
        quantity_window = tk.Toplevel(self.window)
        quantity_window.title("Enter Quantity")
        quantity_window.geometry("300x150")
        quantity_window.grab_set()
        
        ttk.Label(
            quantity_window, 
            text=f"Quantity for {product.name}:"
        ).pack(pady=10)
        
        ttk.Label(
            quantity_window,
            text=f"Available: {product.quantity}"
        ).pack()
        
        quantity_var = tk.IntVar(value=1)
        quantity_spinbox = ttk.Spinbox(
            quantity_window,
            from_=1,
            to=product.quantity,
            textvariable=quantity_var,
            width=10
        )
        quantity_spinbox.pack(pady=10)
        quantity_spinbox.focus()
        
        def confirm():
            qty = quantity_var.get()
            if qty > product.quantity:
                messagebox.showerror(
                    "Error",
                    f"Only {product.quantity} available"
                )
                return
            
            # Add to cart
            self.cart.append({"product": product, "quantity": qty})
            self.update_cart_display()
            quantity_window.destroy()
        
        ttk.Button(
            quantity_window,
            text="Add",
            command=confirm
        ).pack(pady=5)
    
    def remove_from_cart(self):
        """Remove selected item from cart"""
        selection = self.cart_tree.selection()
        if not selection:
            return
        
        idx = self.cart_tree.index(selection[0])
        del self.cart[idx]
        self.update_cart_display()
    
    def update_cart_display(self):
        """Update cart treeview"""
        # Clear tree
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Add items
        total = 0
        for item in self.cart:
            product = item['product']
            quantity = item['quantity']
            unit_price = product.unit_price / 100
            item_total = unit_price * quantity
            total += item_total
            
            self.cart_tree.insert('', tk.END, values=(
                product.name,
                quantity,
                f"FCFA {unit_price:.2f}",
                f"FCFA {item_total:.2f}"
            ))
        
        # Update total
        self.total_label.config(text=f"Total: FCFA {total:.2f}")
    
    def complete_sale(self):
        """Complete the sale"""
        customer_name = self.customer_entry.get().strip()
        if not customer_name:
            messagebox.showerror("Error", "Please enter customer name")
            return
        
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty")
            return
        
        try:
            # Create receipt
            receipt = Receipt(customer_name, self.worker.name)
            
            # Add items to receipt and update inventory
            for item in self.cart:
                product = item['product']
                quantity = item['quantity']
                receipt.add_item(product, quantity)
                self.inventory.update_product_quantity(product, quantity)
            
            # Print receipt
            receipt.print_receipt()
            
            # Save receipt
            filename = receipt.save_to_file()
            
            # Save inventory
            self.inventory.save_products()
            
            # Show success message
            messagebox.showinfo(
                "Success",
                f"Sale completed!\nReceipt saved to: {filename}"
            )
            
            # Update statistics
            if self.update_callback:
                self.update_callback()
            
            # Close window
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing sale: {e}")