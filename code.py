import sqlite3

# Initialize the SQLite database and create tables if they don't exist
conn = sqlite3.connect("sales_management.db")
cursor = conn.cursor()

# Create Product, Customer, and SalesOrder tables
cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Customer (
                    customer_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS SalesOrder (
                    order_id INTEGER PRIMARY KEY,
                    customer_id INTEGER,
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
                )''')

# Commit the changes and close the database connection
conn.commit()
conn.close()

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

class SalesOrder:
    def __init__(self, order_id, customer, products):
        self.order_id = order_id
        self.customer = customer
        self.products = products

# Define functions to interact with the database
def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    conn = sqlite3.connect("sales_management.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Product (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()
    print("Product added successfully!")

def list_products():
    conn = sqlite3.connect("sales_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    conn.close()
    for product in products:
        print(f"Product ID: {product[0]}, Name: {product[1]}, Price: ${product[2]:.2f}")

def add_customer():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    conn = sqlite3.connect("sales_management.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Customer (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    print("Customer added successfully!")

def list_customers():
    conn = sqlite3.connect("sales_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()
    conn.close()
    for customer in customers:
        print(f"Customer ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}")

def create_sales_order():
    customer_id = int(input("Enter customer ID: "))
    conn = sqlite3.connect("sales_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer WHERE customer_id=?", (customer_id,))
    customer = cursor.fetchone()
    if customer is None:
        conn.close()
        print("Customer not found.")
        return

    order_products = []
    while True:
        product_id = int(input("Enter product ID (0 to finish): "))
        if product_id == 0:
            break
        cursor.execute("SELECT * FROM Product WHERE product_id=?", (product_id,))
        product = cursor.fetchone()
        if product is None:
            print("Product not found.")
        else:
            order_products.append(Product(product[0], product[1], product[2]))

    if not order_products:
        conn.close()
        print("No products added to the order.")
        return

    cursor.execute("INSERT INTO SalesOrder (customer_id) VALUES (?)", (customer_id,))
    order_id = cursor.lastrowid
    for product in order_products:
        cursor.execute("INSERT INTO OrderProduct (order_id, product_id) VALUES (?, ?)", (order_id, product.product_id))
    conn.commit()
    conn.close()
    print("Sales order created successfully!")

def list_sales_orders():
    conn = sqlite3.connect("sales_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SalesOrder")
    orders = cursor.fetchall()
    for order in orders:
        cursor.execute("SELECT * FROM OrderProduct WHERE order_id=?", (order[0],))
        order_products = cursor.fetchall()
        customer_id = order[1]
        cursor.execute("SELECT name FROM Customer WHERE customer_id=?", (customer_id,))
        customer_name = cursor.fetchone()[0]
        print(f"Order ID: {order[0]}, Customer: {customer_name}")
        for product in order_products:
            cursor.execute("SELECT name, price FROM Product WHERE product_id=?", (product[1],))
            product_data = cursor.fetchone()
            print(f"  Product: {product_data[0]}, Price: ${product_data[1]:.2f}")
        total_price = sum([product_data[1] for product_data in cursor.fetchall()])
        print(f"  Total Price: ${total_price:.2f}")
    conn.close()

# Main program loop
while True:
    print("\nSales Management System")
    print("1. Add a new product")
    print("2. List all products")
    print("3. Add a new customer")
    print("4. List all customers")
    print("5. Create a new sales order")
    print("6. List all sales orders")
    print("7. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_product()
    elif choice == "2":
        list_products()
    elif choice == "3":
        add_customer()
    elif choice == "4":
        list_customers()
    elif choice == "5":
        create_sales_order()
    elif choice == "6":
        list_sales_orders()
    elif choice == "7":
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection when the program exits
conn.close()

