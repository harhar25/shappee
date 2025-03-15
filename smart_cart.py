import tkinter as tk
from tkinter import ttk
import csv

# Load product database
products = {}
with open("products.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        products[row["barcode"]] = {"name": row["name"], "price": float(row["price"])}

# Cart Data
cart = []
total_price = 0.0

# GUI Setup
root = tk.Tk()
root.title("Smart Cart Scanner")
root.geometry("480x320")
root.configure(bg="white")

# UI Elements
cart_listbox = tk.Listbox(root, width=50, height=10)
cart_listbox.pack(pady=10)

total_label = tk.Label(root, text="Total: $0.00", font=("Arial", 16), bg="white")
total_label.pack()

# Remove item function
def remove_item():
    global total_price
    try:
        selected_index = cart_listbox.curselection()[0]
        removed_item = cart.pop(selected_index)
        total_price -= removed_item["price"]
        update_display()
    except IndexError:
        pass

# Read barcode function
def read_barcode():
    barcode = input("Scan Barcode: ").strip()
    if barcode in products:
        item = products[barcode]
        cart.append(item)
        update_display()
    else:
        print("Unknown Product")

# Update GUI display
def update_display():
    cart_listbox.delete(0, tk.END)
    for item in cart:
        cart_listbox.insert(tk.END, f"{item['name']} - ${item['price']:.2f}")
    total_label.config(text=f"Total: ${total_price:.2f}")

# Remove button
remove_button = tk.Button(root, text="Remove Item", command=remove_item, bg="red", fg="white")
remove_button.pack(pady=5)

# Simulate scanning (for testing)
scan_button = tk.Button(root, text="Simulate Scan", command=read_barcode, bg="blue", fg="white")
scan_button.pack(pady=5)

root.mainloop()