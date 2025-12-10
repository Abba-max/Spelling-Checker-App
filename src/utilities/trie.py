class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.product = None
        
class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, product):  # Inserting a product in the Trie
        node = self.root
        word = product.name.lower()
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.product = product
        
    def search_prefix(self, prefix: str):  # Searching for a product in a Trie based on a prefix
        node = self.root
        prefix_lower = prefix.lower()
        
        # Navigate to prefix node
        for char in prefix_lower:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all products with the current prefix
        return self._collect_products(node)
    
    def _collect_products(self, node, products=None):  # Collecting products starting with the suggested prefix
        if products is None:
            products = []
            
        if node.is_end_of_word and node.product:
            products.append(node.product)
            
        for child in node.children.values():
            self._collect_products(child, products)
            
        return products
    
    def __str__(self):
        return f"Trie(root with {len(self.root.children)} children)"