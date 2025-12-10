from datetime import datetime
from typing import List
import json
import os

class Receipt:
    def __init__(self, customer_name: str, worker_name: str):
        self.customer_name = customer_name
        self.worker_name = worker_name
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.items = []
        self.total = 0.0
    
    def add_item(self, product, quantity: int):  # Method to add an item to the list of items bought
        if quantity > product.quantity:
            raise ValueError(f"Insufficient stock for {product.name}")
        
        item_total_price = (product.unit_price) * quantity
        self.items.append({
            "product_id": product.product_id,
            "name": product.name,
            "quantity": quantity,
            "unit_price": product.unit_price,
            "total": item_total_price
        })
        
        self.total += item_total_price
        
    def generate_text_receipt(self):  # Function to generate a receipt
        lines = []  # Used to contain the content of the receipt
        lines.append("=" * 60)
        lines.append(" " * 23 + "RECEIPT")
        lines.append("=" * 60)
        lines.append(f"Date: {self.date}")
        lines.append(f"Customer: {self.customer_name}")
        lines.append(f"Served by: {self.worker_name}")
        lines.append("-" * 60)
        lines.append(f"{'Item':<25} {'Qty':>5} {'Price':>12} {'Total':>12}")  # Header of the receipt spaced
        lines.append("-" * 60)
        
        for item in self.items:
            lines.append(
                f"{item['name'][:25]:<25} {item['quantity']:>5}"
                f"${item['unit_price']:>11.2f} ${item['total']:>11.2f}"
            )
        
        lines.append("-" * 60)
        lines.append(f"{'':>35} {'TOTAL:':<10} ${self.total / 100:>11.2f}")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def print_receipt(self):
        print("\n" + self.generate_text_receipt() + "\n")
        
    def save_to_file(self, directory="receipts"):  # Method to save receipt to json file
        os.makedirs(directory, exist_ok=True)
        
        filename = f"{directory}/receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        receipt_data = {
            "date": self.date,
            "customer": self.customer_name,
            "worker": self.worker_name,
            "items": self.items,
            "total": self.total
        }
        
        with open(filename, "w") as f:
            json.dump(receipt_data, f, indent=2)
            
        return filename