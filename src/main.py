from utilities.inventory_manager import InventoryManager
from ui.console_ui import ConsoleUI

def main():
    inventory = InventoryManager("data/stock.json")
    
    ui = ConsoleUI(inventory)
    
    ui.run()

if __name__ == "__main__":
      main()
