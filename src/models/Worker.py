class Worker:
    
    def _init_(self,worker_id:int,name:str,quantity:int,date:str,customer_name:str,products:list):
        self.worker_id = worker_id
        self.name = name
        self.products = products
        self.date = date
        self.customer_name = customer_name
       