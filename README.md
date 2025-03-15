# Smart Cart

## Description
Smart Cart is a Python-based system that integrates a barcode scanner with a shopping cart. It allows customers to scan products as they shop and track their total spending in real time, ensuring they stay within budget.

## Features
- Scans barcodes of products using an attached scanner
- Loads product details from `products.csv`
- Calculates and displays the total cost of scanned items
- Alerts users if they exceed their predefined budget
- Supports adding and removing scanned items dynamically

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/harhar25/smart-cart.git
   ```
2. Navigate to the project directory:
   ```sh
   cd smart-cart
   ```
3. Ensure you have Python installed (Python 3.x recommended).
4. Install required dependencies if any:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Connect a barcode scanner to your system.
2. Place your `products.csv` file in the same directory as `smart_cart.py`.
3. Run the script:
   ```sh
   python smart_cart.py
   ```
4. Scan product barcodes to add them to your cart.
5. Check your total cost in real time and receive alerts if you exceed your budget.

## File Structure
```
smart-cart/
├── smart_cart.py  # Main script
├── products.csv   # Product inventory file
├── README.md      # Documentation
```

## Example Products CSV Format
Ensure the `products.csv` file is formatted correctly:
```csv
barcode,name,price,quantity
123456789012,Apple,0.50,100
987654321098,Banana,0.30,150
567890123456,Orange,0.40,120
```




--- Connection Linux/Raspbian---

* 🔌 Step-by-Step Wiring & Connections:
1️⃣ Connect the LCD to Raspberry Pi 3
If you are using a touchscreen LCD, follow the manufacturer’s instructions to connect via HDMI or GPIO.
For a 16x2 LCD with I2C Module:

VCC (LCD) → 5V (RPI 3)
GND (LCD) → GND (RPI 3)
SDA (LCD) → GPIO 2 (SDA1 on RPI 3)
SCL (LCD) → GPIO 3 (SCL1 on RPI 3)

2️⃣ Connect the Barcode Scanner
If it’s a USB Barcode Scanner, just plug it into any USB port on the RPI 3. The system will detect it as a keyboard input device.
If it’s a Serial Barcode Scanner (TTL/UART):
TX (Scanner) → GPIO 14 (TXD0 on RPI 3)
RX (Scanner) → GPIO 15 (RXD0 on RPI 3)
GND (Scanner) → GND (RPI 3)
Configure serial communication via ttyS0 or ttyAMA0.

3️⃣ Powering Everything Up
Connect the Raspberry Pi 3 to a 5V/2.5A power adapter.
Make sure the LCD is properly powered.
The barcode scanner should light up or beep when powered.

* Run the following in the Raspberry Pi terminal:
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip
pip3 install tkinter pandas pyserial smbus2

2️⃣ Enable I2C & Serial on RPI 3
sudo raspi-config

Go to Interfacing Options → Enable I2C & Serial
Reboot with:
sudo reboot

3️⃣ Modify the Code to Use GPIO & Serial Input
If using USB Barcode Scanner, it acts like a keyboard. The barcode is entered where the cursor is active.
If using Serial Barcode Scanner, modify the Python code:
import serial

ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)  # Adjust for your scanner

def read_barcode():
    barcode = ser.readline().decode('utf-8').strip()
    return barcode if barcode else None

## Replace self.entry.get() in the scan_barcode function with read_barcode().


* ✅ Final Steps:
Run the Python UI Code:

python3 smart_cart.py

* Scan a Product:
If using USB: Just scan, and it will appear on the screen.
If using Serial: The barcode will be read from /dev/ttyS0.

* Check the LCD Display:
It should show the product name and total cost.

* Remove Items from Cart:
Select an item and press "Remove Item."

* Budget Monitoring:
The total price will update dynamically.



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
## Future Enhancements
- Implement a graphical user interface (GUI)
- Add discount and promo code features
- Support database integration for larger inventories
- Introduce AI-based budget recommendations

## License
This project is licensed under the MIT License.

## Author
Developed by [@harhar25](https://github.com/harhar25) 🚀