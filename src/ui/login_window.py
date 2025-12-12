import tkinter as tk
from tkinter import ttk, messagebox
from models.worker import Worker

class LoginWindow:
    def __init__(self,parent,on_success_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Login - Inventory Management System")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.on_success = on_success_callback
        # self.center_window() # Place the window at the center of the screen
        self.create_widgets() # Create UI
        self.window.grab_set()
        self.window.focus_set()
        
    def center_window():
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')   
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        title = ttk.Label(
            main_frame, 
            text="Inventory System", 
            style='Title.TLabel'
            )
        title.pack(pady=(0, 10))
        subtitle = ttk.Label(main_frame, text="Worker Login")
        subtitle.pack(pady=(0, 30))
        
        #WorkerID
        ttk.Label(main_frame, text="Worker ID:").pack(anchor=tk.W, pady=(0, 5))
        self.worker_id_entry = ttk.Entry(main_frame, width=30)
        self.worker_id_entry.pack(pady=(0, 15))
        self.worker_id_entry.focus()
        
        #WorkerName
        ttk.Label(main_frame, text="Worker Name:").pack(anchor=tk.W, pady=(0, 5))
        self.worker_name_entry = ttk.Entry(main_frame, width=30)
        self.worker_name_entry.pack(pady=(0, 20))
        
        #Login button
        login_btn = ttk.Button(
            main_frame, 
            text="Login", 
            command=self.login,
            style='TButton'
        )
        login_btn.pack(pady=(10,0))
        
        self.window.bind('<Return>', lambda e: self.login())
        
    def login(self):
        worker_id = self.worker_id_entry.get().strip()
        worker_name = self.worker_name_entry.get().strip()
        if not worker_id or not worker_name:
             messagebox.showerror(
                            "Error", 
                            "Please enter both Worker ID and Name"
                        )
             return
        worker = Worker(worker_id, worker_name)
        self.window.destroy() # Close login window
        self.on_success(worker)