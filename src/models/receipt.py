from datetime import datetime
from typing import List
import json
class Receipt:
    def __init__(self, customer_name: str, worker_name: str):
        self.customer_name = customer_name
        self.worker_name = worker_name
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.items = []
        self.total = 0.0