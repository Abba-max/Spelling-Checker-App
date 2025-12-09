class Worker:
    
    def __init__(self,worker_id:int,name:str):
        self.worker_id = worker_id
        self.name = name
        
    def __str__(self):
        return f"Worker {self.worker_id}: {self.name}"
    
    def __repr__(self):
        return f"Worker({self.worker_id}, {self.name})"
       