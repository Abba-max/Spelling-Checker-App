class Product:
    
    def _init_(self,product_id:int,name:str, unit_price:float, quantity:int,expiry_date:str,supplier:str):
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.supplier = supplier

@property
def getID(self):
    return self.__product_id

@name.setter
def setID(self,product_id):
    if(type(name)==str):
        self.__product_id = product_id
    else:
        print("Enter a valid ID")

@property
def getName(self):
    return self.__name

@name.setter
def setName(self,name):
    if(type(name)==str):
        self.__name = name
    else:
        print("Enter a str as product name")

@property
def getQuantity(Self):
    return self.__quantity

@quantity.setter
def setQuantity(self,quantity):
    if(type(quantity)==int):
        self.__quantity = quantity
    else:
        f"{self.__name} out of stock"

@property
def getExpiry_date(Self):
    return self.__expiry_date

@property
def getSupplier(Self):
    return self.__supplier


product1 = Product() 
    
    