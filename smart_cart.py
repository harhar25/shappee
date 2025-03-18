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
    return products

products = load_products()

class SmartCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Cart Scanner")
        self.root.attributes("-fullscreen", True)  # Set to true fullscreen

        self.cart = {}
        self.total = 0.0

        # Header Styling
        self.header_label = tk.Label(root, text="🛒 Smart Cart Scanner 🛒", font=("Arial", 20, "bold"), bg="#28a745", fg="white", pady=10)
        self.header_label.pack(fill=tk.X)

        # Frame for Products List
        self.frame = tk.Frame(root, bg="#f8f9fa", bd=5, relief="ridge")
        self.frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Styled Listbox (Now using Treeview for better display)
        self.tree = ttk.Treeview(self.frame, columns=("Product", "Quantity", "Price", "Actions"), show="headings", height=15)
        self.tree.heading("Product", text="Product")
        self.tree.heading("Quantity", text="Qty")
        self.tree.heading("Price", text="Price")
        self.tree.column("Product", width=250)
        self.tree.column("Quantity", width=100, anchor="center")
        self.tree.column("Price", width=100, anchor="center")
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Total Price Display
        self.total_label = tk.Label(root, text="Total: ₱0", font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#333")
        self.total_label.pack()

        # Button Frame
        self.button_frame = tk.Frame(root, bg="#f8f9fa")
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.remove_btn = tk.Button(self.button_frame, text="Remove Item", command=self.remove_item, bg="#F9D3D3", fg="black", font=("Arial", 14, "bold"), padx=15, pady=8, relief="flat", bd=0, activebackground="#e74c3c", activeforeground="white")
        self.remove_btn.pack(side=tk.LEFT, ipadx=10, ipady=5, padx=5, pady=5)
        self.remove_btn.bind("<Enter>", lambda e: self.remove_btn.config(bg="#e74c3c", fg="white"))
        self.remove_btn.bind("<Leave>", lambda e: self.remove_btn.config(bg="#F9D3D3", fg="black"))
        
        self.clear_btn = tk.Button(self.button_frame, text="Clear Cart", command=self.clear_cart, bg="#D3E5F9", fg="black", font=("Arial", 14, "bold"), padx=15, pady=8, relief="flat", bd=0, activebackground="#3399ff", activeforeground="white")
        self.clear_btn.pack(side=tk.RIGHT, ipadx=10, ipady=5, padx=5, pady=5)
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg="#3399ff", fg="white"))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg="#D3E5F9", fg="black"))

        # Hidden Entry Box for Barcode Scanning
        self.entry = ttk.Entry(root, font=("Arial", 1))  # Tiny font
        self.entry.place(x=-100, y=-100)  # Position it off-screen
        self.entry.bind("<Return>", self.scan_barcode)
        self.entry.focus_set()

        # Auto-focus the entry field even when the user clicks elsewhere
        self.root.bind("<Button-1>", self.refocus_entry)

    def scan_barcode(self, event=None):
        barcode = self.entry.get().strip()
        if barcode in products:
            if barcode in self.cart:
                self.cart[barcode]['quantity'] += 1
            else:
                self.cart[barcode] = {**products[barcode], 'quantity': 1}
            self.update_cart_display()
        else:
            print("Unknown product.")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def update_cart_display(self):
        self.tree.delete(*self.tree.get_children())
        for barcode, item in self.cart.items():
            row_id = self.tree.insert("", tk.END, values=(item['name'], item['quantity'], f"₱{self.format_price(item['price'] * item['quantity'])}"))
            self.tree.set(row_id, column="Actions", value="[ + ]  [ - ]")
            self.tree.bind("<Double-1>", self.modify_quantity)
        self.update_total()

    def modify_quantity(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            for barcode, item in self.cart.items():
                if item['name'] == item_values[0]:
                    if event.x > 50:  # Clicked on "-"
                        if item['quantity'] > 1:
                            item['quantity'] -= 1
                        else:
                            del self.cart[barcode]
                    else:  # Clicked on "+"
                        item['quantity'] += 1
                    break
            self.update_cart_display()

    def remove_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            for barcode, item in list(self.cart.items()):
                if item['name'] == item_values[0]:
                    del self.cart[barcode]
                    break
            self.update_cart_display()
        else:
            print("No item selected for removal.")

    def clear_cart(self):
        self.cart.clear()
        self.update_cart_display()

    def update_total(self):
        self.total = sum(item['price'] * item['quantity'] for item in self.cart.values())
        self.total_label.config(text=f"Total: ₱{self.format_price(self.total)}")

    def refocus_entry(self, event):
        self.entry.focus_set()

    def format_price(self, price):
        return f"{price:.2f}".rstrip('0').rstrip('.')

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCartApp(root)
    root.mainloop()
