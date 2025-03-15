import tkinter as tk
import csv
from tkinter import ttk
import os

# Load products from CSV
def load_products(filename="products.csv"):
    products = {}
    with open(filename, newline="", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products[row['barcode']] = {'name': row['name'], 'price': float(row['price'])}
    print("Loaded products:", products)  # Debug log
    return products

products = load_products()

class SmartCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Cart Scanner")
        self.root.geometry("600x600")  # Adjusted for better UI
        
        # Check if background image exists
        bg_image_path = "background.png"
        if os.path.exists(bg_image_path):
            self.bg_image = tk.PhotoImage(file=bg_image_path)
            self.bg_label = tk.Label(root, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
        else:
            self.root.configure(bg="#f8f9fa")  # Default background color
        
        self.cart = []
        self.total = 0.0
        
        # Header Styling
        self.header_label = tk.Label(root, text="🛒 Smart Cart Scanner 🛒", font=("Arial", 20, "bold"), bg="#28a745", fg="white", pady=10)
        self.header_label.pack(fill=tk.X)
        
        # Frame for Products List
        self.frame = tk.Frame(root, bg="#f8f9fa")
        self.frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Styled Listbox
        self.listbox = tk.Listbox(self.frame, width=60, height=10, font=("Arial", 14), bg="white", fg="#333", bd=2, relief="solid")
        self.listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Total Price Display
        self.total_label = tk.Label(root, text=f"Total: ₱0.00", font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#333")
        self.total_label.pack()
        
        # Button Styling
        self.button_frame = tk.Frame(root, bg="#f8f9fa")
        self.button_frame.pack()
        
        self.remove_btn = tk.Button(self.button_frame, text="Remove Item", command=self.remove_item, bg="#dc3545", fg="white", font=("Arial", 14, "bold"), padx=15, pady=8)
        self.remove_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.scan_btn = tk.Button(self.button_frame, text="Scan Barcode", command=self.scan_barcode, bg="#007bff", fg="white", font=("Arial", 14, "bold"), padx=15, pady=8)
        self.scan_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Entry Box for Manual Barcode Input
        self.entry = ttk.Entry(root, font=("Arial", 14), justify="center")
        self.entry.pack(pady=10, ipadx=10, ipady=5, fill=tk.X, padx=10)
        self.entry.bind("<Return>", self.scan_barcode)
        
    def scan_barcode(self, event=None):
        barcode = self.entry.get().strip()
        print(f"Scanned barcode: {barcode}")  # Debug log
        
        if barcode in products:
            product = products[barcode]
            print(f"Valid product: {product}")  # Debug log
            self.cart.append(product)
            self.listbox.insert(tk.END, f"{product['name']} - ₱{product['price']:.2f}")
            self.update_total()
        else:
            print("Unknown product.")  # Debug log
        
        self.entry.delete(0, tk.END)
        
    def remove_item(self):
        print("Remove item triggered")  # Debug log
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            removed_product = self.cart.pop(index)
            print(f"Removed product: {removed_product}")  # Debug log
            self.listbox.delete(index)
            self.update_total()
        else:
            print("No item selected for removal.")  # Debug log
        
    def update_total(self):
        self.total = sum(item['price'] for item in self.cart)
        print(f"Updated total: {self.total}")  # Debug log
        self.total_label.config(text=f"Total: ₱{self.total:.2f}")
        
if __name__ == "__main__":
    print("Starting Smart Cart Application")  # Debug log
    root = tk.Tk()
    app = SmartCartApp(root)
    root.mainloop()
