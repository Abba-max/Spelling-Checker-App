import tkinter as tk
from tkinter import ttk, messagebox
from utilities.inventory_manager import InventoryManager
from ui.login_window import LoginWindow
from ui.main_window import MainWindow

class InventoryGUIApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window initially
        self.inventory = InventoryManager("data/stock.json")
        self.current_worker = None
        self.setup_styles()
        self.show_login()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#ECF0F1')
        style.configure('TLabel', background='#ECF0F1', foreground='#2C3E50')
        style.configure('TButton', background='#3498DB', foreground='white')
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'))
    
    def show_login(self):
        login_win = LoginWindow(self.root, self.on_login_success)
    
    def on_login_success(self,worker):
        self.current_worker = worker
        self.root.deiconify() # Show main window
    
        self.main_window = MainWindow(
            self.root, 
            self.inventory, 
            self.current_worker
        )
    
    def run(self):
        self.root.mainloop()