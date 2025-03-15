# **Smart Shopping Cart System**

## **📌 Overview**

This project is a **Smart Shopping Cart System** that allows customers to track their total spending while shopping. The system consists of a **Raspberry Pi 3**, a **barcode scanner**, and a **touchscreen LCD** to display the scanned products. Customers can remove items if they exceed their budget, providing a seamless shopping experience.

---

## **🛠️ Hardware Components**

| Component                     | Function                                    |
| ----------------------------- | ------------------------------------------- |
| **Raspberry Pi 3**            | Main controller for processing data         |
| **USB Barcode Scanner**       | Reads barcodes from products                |
| **Touchscreen LCD**           | Displays UI for scanned items & total price |
| **Breadboard & Jumper Wires** | Connects components if needed               |
| **Resistors**                 | Used if additional circuits are required    |

---

## **🔌 Hardware Connection Guide**

### **1️⃣ Connect the Touchscreen LCD**

- **HDMI-based LCD:**
  - Connect **HDMI cable** from Raspberry Pi to the LCD.
  - Power the LCD with a **micro USB cable** (if required).
- **GPIO-based LCD (SPI interface):**
  - Connect **LCD to GPIO pins** as per manufacturer instructions.
  - Enable the SPI interface in Raspberry Pi settings.

### **2️⃣ Connect the Barcode Scanner**

- **USB Barcode Scanner (Plug & Play):**
  - Plug the scanner into any **USB port** on the Raspberry Pi.
  - Test scanning with:
    ```bash
    cat /dev/hidraw0
    ```

### **3️⃣ (Optional) Breadboard & Jumper Wires**

- If adding **LED indicators** or **buzzers**, use jumper wires to connect them to GPIO pins.

---

## **💾 Product Database (products.csv)**

The system loads product information from a CSV file.

Create a file named **`products.csv`** with this format:

```
barcode,name,price
123456789012,Coca-Cola 1L,1.50
987654321098,Lay's Chips,2.00
456789123456,Milk 1L,1.20
321654987321,Orange Juice,3.00
159753456852,Bread Loaf,1.80
258369147258,Chocolate Bar,1.50
```

---

## **📜 Software Setup**

### **1️⃣ Update Raspberry Pi OS**

```bash
sudo apt update && sudo apt upgrade -y
```

### **2️⃣ Enable SPI for Touchscreen LCD (if needed)**

```bash
sudo raspi-config
```

- Go to **Interfacing Options > SPI > Enable**
- Reboot:
  ```bash
  sudo reboot
  ```

### **3️⃣ Install Dependencies**

```bash
sudo apt install python3 python3-tk
```

---

## **📜 Python Code for Smart Cart GUI**

```python
import tkinter as tk
from tkinter import ttk
import csv

# Load product database
products = {}
with open("products.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        products[row["barcode"]] = {"name": row["name"], "price": float(row["price"])}

cart = []
total_price = 0.0

# GUI Setup
root = tk.Tk()
root.title("Smart Cart Scanner")
root.geometry("480x320")
root.configure(bg="white")

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
    global total_price
    barcode = input("Scan Barcode: ").strip()
    if barcode in products:
        item = products[barcode]
        cart.append(item)
        total_price += item["price"]
        update_display()
    else:
        print("Unknown Product")

# Update GUI display
def update_display():
    cart_listbox.delete(0, tk.END)
    for item in cart:
        cart_listbox.insert(tk.END, f"{item['name']} - ${item['price']:.2f}")
    total_label.config(text=f"Total: ${total_price:.2f}")

remove_button = tk.Button(root, text="Remove Item", command=remove_item, bg="red", fg="white")
remove_button.pack(pady=5)

scan_button = tk.Button(root, text="Simulate Scan", command=read_barcode, bg="blue", fg="white")
scan_button.pack(pady=5)

root.mainloop()
```

---

## **🖥️ Running the System**

### **1️⃣ Save ****`products.csv`**** in the same directory as the script.**

### **2️⃣ Run the script:**

```bash
python3 smart_cart.py
```

---

## **🎨 Best Editors for Development**

| Editor         | Installation                  |
| -------------- | ----------------------------- |
| **Thonny**     | Pre-installed on Raspberry Pi |
| **VS Code**    | `sudo apt install code`       |
| **Geany**      | `sudo apt install geany`      |
| **Nano (CLI)** | Pre-installed                 |

---

## **✅ Features**

✔ **Scrollable product list** 🛍️\
✔ **Tap an item to remove** 🖐️\
✔ **Shows live total price** 🏷️\
✔ **Works with barcode scanner** 📷

---

## **🚀 Future Upgrades**

📊 **Cloud database integration**\
📡 **Wireless connectivity for real-time updates**\
⚠️ **Budget alerts for customers**

---

## **📌 Troubleshooting**

| Issue                         | Solution                                         |
| ----------------------------- | ------------------------------------------------ |
| Touchscreen not working       | Check `raspi-config` settings and SPI driver     |
| Barcode scanner not detecting | Try `cat /dev/hidraw0` and verify scanner output |
| GUI not displaying            | Check `tkinter` installation                     |

---

## **🔗 GitHub Repository**

[Project Repository](https://github.com/harhar25/shappee.git)

---

## **👨‍💻 Author**

**Harold Jey Nahid Madjos** (Gwapo)\
🚀 Passionate about AI, ethical hacking, and tech innovations\
📌 [GitHub Profile](https://github.com/harhar25)



