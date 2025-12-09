import json
from datetime import datetime
from typing import List, Optional
from models.product import Product
from models.receipt import Receipt
from utilities.bloom_filter import BloomFilter
from utilities.trie import Trie

class InventoryManager:
    def __init__(self, json_file:str="dat/stock.json"):
        self.json_file = json_file
        self.products = []
        self.bloom_filter = BloomFilter(size=1000,hash_count=3)
        self.trie = Trie()
    
    def load_products(self): # Load products from JSON file
        try:
            with open(Self.json_file,'r') as f: # Open JSON file in read lony mode
                data = json.load(f)
                for prod_data in data.get("products",[]): # Loop through all products
                    product = Product(
                        product_id=prod_data["product_id"],
                        name=prod_data["name"],
                        unit_price=prod_data["unit_price"],
                        quantity=prod_data["quantity_in_stock"],
                        expiry_date=prod_data["expiry_date"],
                        supplier=prod_data["supplier"],
                        category=prod_data.get("category", "")
                    )
                    self.products.append(product)
                    self.bloom_filter.add(product.name)
                    self.trie.insert(product)
                    
                print(f"✓ Loaded {len(self.products)} products")
        except FileNotFoundError:
            print(f"✗ Error: {self.json_file} not found")
        except Exception as e:
            print(f"✗ Error loading products: {e}")
            
    def save_products(self):
        try:
            with open(self.json_file,'r') as f:
                data = json.load(f)
                data["products"] = [p.to_dict() for p in self.products] # Converting product to dictionary and saving in data
                data["metadata"]["total_products"] = len(self.products) # Total size of products
                data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Date saved
        
            with open(self.json_file, 'w') as f:
                json.dump(data,f,indent=2) # Writing all product data in a json file
            
            print("✓ Inventory saved successfully")
            return True
        except Exception as e:
          print(f"✗ Error saving products: {e}")
          return False

    def search_with_autocomplete(self,prefix:str):
        if not prefix.strip(): # Removes leading and trailing whitespaces from prefix 
            return []
        if not self.bloom_filter.contain(prefix):
            return []
        
        return self.trie.search_prefix(prefix)
    
    def get_products_sorted_by_expiry(self):
        return sorted(self.products, key=lambda p: datetime.strptime(p.expiry_date, "%Y-%m-%d"))
    
    def update_product_quantity(Self,product:Product,quantity_sold:int):
        if quantity_sold > product.quantity:
            raise ValueError(f"Cannot sell more than available stock ({product.quantity})")
        product.quantity = product.quantity - quantity_sold
        
    def add_product(self,product:Product):
        self.products.append(product)
        self.bloom_filter.add(product.name)
        self.trie.insert(product)
    
    def update_product(self, product_id:str,**kwargs):
        for product in self.products:
            if product.product_id ==product_id:
                for key,value in kwargs.items():
                    if hasattr(product,key):
                        setattr(product,key,value)
                return True
        return False
    
    def display_inventory(self,sort_by="expiry"): # By default, products are sorted by expiry_date
        if sort_by == "expiry":
            products = self.get_products_sorted_by_expiry()
        elif sort_by == "name":
            products = sorted(self.products, key=lambda p: p.name)
        elif sort_by == "stock":
            products = sorted(self.products, key=lambda p: p.quantity)
        else:
            products = self.products
        
        print("\n" + "=" * 100)
        print(" " * 40 + "INVENTORY")
        print("=" * 100)
        print(f"{'ID':<8} {'Name':<18} {'Category':<15} {'Stock':<8} {'Price':<10} {'Expiry':<12} {'Supplier':<15}")
        print("-" * 100)
        
        for p in products:
            stock_status = "⚠ LOW" if p.quantity < 30 else str(p.quantity)
            print(f"{p.product_id:<8} {p.name:<18} {p.category:<15} {stock_status:<8} "
                  f"${p.unit_price/100:<9.2f} {p.expiry_date:<12} {p.supplier:<15}")
        
        print("=" * 100 + "\n")
            
    
        