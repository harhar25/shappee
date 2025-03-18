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
        self.root.geometry("600x600")

        # Check if background image exists
        bg_image_path = "background.png"
        if os.path.exists(bg_image_path):
            self.bg_image = tk.PhotoImage(file=bg_image_path)
            self.bg_label = tk.Label(root, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
        else:
            self.root.configure(bg="#f8f9fa")

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
        self.total_label = tk.Label(root, text="Total: ₱0", font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#333")
        self.total_label.pack()

        # Button Styling
        self.button_frame = tk.Frame(root, bg="#f8f9fa")
        self.button_frame.pack()

        self.remove_btn = tk.Button(self.button_frame, text="Remove Item", command=self.remove_item, bg="#dc3545", fg="white", font=("Arial", 14, "bold"), padx=15, pady=8)
        self.remove_btn.grid(row=0, column=0, padx=5, pady=5)

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
            product = products[barcode]
            self.cart.append(product)
            formatted_price = self.format_price(product['price'])
            self.listbox.insert(tk.END, f"{product['name']} - ₱{formatted_price}")
            self.update_total()
        else:
            print("Unknown product.")  # You can replace with a label if needed

        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def remove_item(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.cart.pop(index)
            self.listbox.delete(index)
            self.update_total()
        else:
            print("No item selected for removal.")

    def update_total(self):
        self.total = sum(item['price'] for item in self.cart)
        self.total_label.config(text=f"Total: ₱{self.format_price(self.total)}")

    def refocus_entry(self, event):
        """Refocus barcode entry field when user clicks anywhere."""
        self.entry.focus_set()

    def format_price(self, price):
        """Format prices: No decimals if whole, otherwise two decimal places."""
        return f"{price:.2f}".rstrip('0').rstrip('.')  # Removes .00 but keeps decimals when needed

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCartApp(root)
    root.mainloop()
