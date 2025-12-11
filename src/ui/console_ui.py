from models.worker import Worker
from models.receipt import Receipt
from utilities.inventory_manager import InventoryManager

class ConsoleUI:
    def __init__(self, inventory_manager: InventoryManager):
        self.inventory = inventory_manager
        self.current_worker = None
        self.cart = []
        
    def display_menu(self):
        print("\n" + "="*50)
        print(" " * 15 + "MAIN MENU")
        print("="*50)
        print("1. Login as Worker")
        print("2. Make Sale")
        print("0. Add Product")
        print("3. View Inventory")
        print("4. Update Product")
        print("5. Save & Exit")
        print("="*50)
    
    def login_worker(self):
        worker_id = input("Enter Worker ID: ").strip()
        worker_name = input("Enter Worker Name: ").strip()
        self.current_worker = Worker(worker_id, worker_name)
        print(f"✓ Logged in as {self.current_worker}")
    
    def search_product_interactive(self):
        print("\n" + "-"*50)
        print("Type product name (autocomplete enabled)")
        print("Type 'done' when finished adding items")
        print("-"*50)
        while True:
            search_term = input("\nSearch product: ").strip()
            if search_term.lower() == 'done':
                break
            if not search_term:
                continue
            matches = self.inventory.search_with_autocomplete(search_term)  # Get autocompleted suggestions
            if not matches:
                print("✗ No products found matching '{}'".format(search_term))
                continue
            
            print(f"\n{'#':<4} {'Name':<20} {'Stock':<8} {'Price':<10}")  # Header for displaying matching products
            print("-"*45)
            
            for idx, product in enumerate(matches, 1):
                print(f"{idx:<4} {product.name:<20} {product.quantity:<8} ${product.unit_price/100:<9.2f}")

            try:
                choice = int(input("\nSelect product number: "))
                if 1 <= choice <= len(matches):
                    selected = matches[choice - 1]
                    quantity = int(input(f"Quantity for {selected.name}: "))
                    if quantity > selected.quantity:
                        print(f"✗ Only {selected.quantity} available")
                        continue
                    self.cart.append({"product": selected, "quantity": quantity})
                    print(f"✓ Added {quantity}x {selected.name} to cart")
                else:
                    print("✗ Invalid selection")
            except ValueError:
                print("✗ Invalid input")
                
    def make_sale(self):  # Adding products to cart and printing a receipt
        if not self.current_worker:
            print("✗ Please login first")
            return
        customer_name = input("\nCustomer Name: ").strip()
        if not customer_name:
            print("✗ Customer name required")
            return
        self.cart = []
        self.search_product_interactive()
        if not self.cart:
            print("✗ Cart is empty")
            return
        receipt = Receipt(customer_name, self.current_worker.name)  # Creating a Receipt Object
        
        try:
            for item in self.cart:
                product = item["product"]
                quantity = item["quantity"]
                receipt.add_item(product, quantity)
                self.inventory.update_product_quantity(product, quantity)

            receipt.print_receipt()
            filename = receipt.save_to_file()
            print(f"✓ Receipt saved to {filename}")

            self.inventory.save_products()
        except Exception as e:
            print(f"✗ Error processing sale: {e}")
            
    def add_product():
        # id = input("Enter product ID")
        # name = input("Enter product name")
        # category = input("Enter product category")
        # quantity_in_stock = eval(input("Enter quntity input in store"))
        # unit_price = eval(input("Enter unit price for {name}"))
        # expiry_date = input("Enter expiry date in format 'year-month-day' ")
        # supplier = input("Enter supplier name")
        
        # product = Product(id, name, category,quantity_in_stock,unit_price,expiry_date,supplier)
        # try: 
        #     with open(self.json_file, 'w') as f:
        #          json.dump(product.to_dict(), f, indent=2)  # Writing all product data in a json file, converting them to a dictionary before
        #          print("✓ New Product saved successfully")
        #          return True
        # except:
        #     print("An exception occured...")
        return
        
    
    
            
    def view_inventory(self):
        print("\nSort by:")
        print("1. Expiry Date")
        print("2. Name")
        print("3. Stock Level")
        choice = input("Choice (1-3): ").strip()
        sort_by = {"1": "expiry", "2": "name", "3": "stock"}.get(choice, "expiry")
        self.inventory.display_inventory(sort_by)

    def update_product(self):
        product_id = input("\nProduct ID to update: ").strip()
        
        product = None
        for p in self.inventory.products:
            if p.product_id == product_id:
                product = p
                break
        if not product:
            print("✗ Product not found")
            return
        print(f"\nCurrent: {product}")
        print("\nWhat to update?")
        print("1. Quantity")
        print("2. Price")
        print("3. Both")
        
        choice = input("Choice: ").strip()
        
        try:
            if choice in ["1", "3"]:
                new_quantity = int(input("New quantity: "))
                product.quantity = new_quantity
            if choice in ["2", "3"]:
                new_price = float(input("New price (in cents): "))
                product.unit_price = new_price
            self.inventory.save_products()
            print(f"✓ Updated {product.name}")
        except ValueError as e:
            print(f"✗ Error: {e}")
            
    def run(self):
        print("\n" + "="*50)
        print(" " * 10 + "INVENTORY MANAGEMENT SYSTEM")
        print(" " * 12 + "Bloom Filter + Trie Search")
        print("="*50)
        
        while True:
            self.display_menu()
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                self.login_worker()
            elif choice == "2":
                self.make_sale()
            elif choice == "3":
                self.view_inventory()
            elif choice == "4":
                self.update_product()
            elif choice == "5":
                self.inventory.save_products()
                print("\n✓ Goodbye!")
                break
            else:
                print("✗ Invalid option")