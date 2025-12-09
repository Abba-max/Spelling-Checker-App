class Product:
    def __init__(self, product_id: str, name: str, unit_price: float, 
                 quantity: int, expiry_date: str, supplier: str, category: str = ""):
        self.__product_id = product_id
        self.__name = name
        self.__unit_price = unit_price
        self.__quantity = quantity
        self.__expiry_date = expiry_date
        self.__supplier = supplier
        self.__category = category
@property
def product_id(self):
    return self.__product_id

@property
def name(self):
    return self.__name

@name.setter
def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self.__name = value
@property
def quantity(self):
    return self.__quantity

@quantity.setter
def quantity(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Quantity must be a non-negative integer")
        self.__quantity = value
@property
def unit_price(self):
    return self.__unit_price

@unit_price.setter
def unit_price(self, value):
    if not isinstance(value, (int, float)) or value < 0:
        raise ValueError("Price must be a non-negative number")
    self.__unit_price = value
    
@property
def expiry_date(self):
    return self.__expiry_date
    
@property
def supplier(self):
    return self.__supplier
    
@property
def category(self):
    return self.__category

#Function to convert product to dictionary for JSON serialization
def to_dict(self):
   return {
            "product_id": self.__product_id,
            "name": self.__name,
            "category": self.__category,
            "quantity_in_stock": self.__quantity,
            "unit_price": self.__unit_price,
            "expiry_date": self.__expiry_date,
            "supplier": self.__supplier
        }
   
#Function to display product's id and name
def __repr__(self):
     return f"Product({self.__product_id}, {self.__name})"
 



