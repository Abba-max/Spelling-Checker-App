import hashlib
class BloomFilter:
    def __init__(self,size:int=1000,hash_count:int=3):
        # The higher the size, the lesser the false positives
        # The smaller the hash_count, the higher the accuracy
        self.size = size
        self.hahsh_count = hash_count
        self.bit_array = [0]*size
        
    def _hash(self,item:str,seed:int):
        hash_obj = hashlib.md5(f"{item}{seed}".encode())
        
        return int(hash_obj.hexdigest(),16)%self.size
    
    def add(self,item:str): # Method to add an itemm to a bloom filter
        item = item.lower()
        for i in range(self.hash_count):
            index = self._hash(item,i)
            self.bit_Array[index] = 1
    
    def contain(self,item:str): # Method to search for an item in a bloom filter
        item = item.lower()
        for i in range(self.hash_count):
            index = self._hash(item,i)
            if self.bit_array[index] == 0 :
                return False
        return True
    
    def __str__(self): # Displaying the size and nuumber of 1 bits in the bloom filter
        ones = sum(self.bit_array)
        return f"BloomFilter(size={self.size}, filled={ones}/{self.size})"