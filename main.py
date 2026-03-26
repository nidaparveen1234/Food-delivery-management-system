import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient, errors

# ---------------- DATABASE CONNECTION ----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["food_delivery_db"]

customers = db["customers"]
foods = db["food_items"]
orders = db["orders"]

customers.create_index("customer_id", unique=True)
foods.create_index("food_id", unique=True)
orders.create_index("order_id", unique=True)

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Food Delivery Management System")
root.geometry("1100x600")
root.configure(bg="#ffe5b4")

# ---------------- TITLE ----------------
title = tk.Label(root,
text="🍔 Food Delivery Management System",
font=("Helvetica",20,"bold"),
bg="#ff914d",
fg="white",
pady=10)

title.grid(row=0,column=0,columnspan=3,sticky="ew")

# =====================================================
# CUSTOMER SECTION
# =====================================================

customer_frame = tk.LabelFrame(root,text="Customer Section",
font=("Arial",12,"bold"),bg="#fff4e6",padx=10,pady=10)

customer_frame.grid(row=1,column=0,padx=20,pady=20)

tk.Label(customer_frame,text="Customer ID",bg="#fff4e6").grid(row=0,column=0)
cust_id = tk.Entry(customer_frame)
cust_id.grid(row=0,column=1)

tk.Label(customer_frame,text="Name",bg="#fff4e6").grid(row=1,column=0)
cust_name = tk.Entry(customer_frame)
cust_name.grid(row=1,column=1)

tk.Label(customer_frame,text="Phone",bg="#fff4e6").grid(row=2,column=0)
cust_phone = tk.Entry(customer_frame)
cust_phone.grid(row=2,column=1)

tk.Label(customer_frame,text="Address",bg="#fff4e6").grid(row=3,column=0)
cust_address = tk.Entry(customer_frame)
cust_address.grid(row=3,column=1)

# ---------- CLEAR CUSTOMER ----------
def clear_customer():
    cust_id.delete(0,tk.END)
    cust_name.delete(0,tk.END)
    cust_phone.delete(0,tk.END)
    cust_address.delete(0,tk.END)

# ---------- CUSTOMER FUNCTIONS ----------
def add_customer():
    try:
        customers.insert_one({
        "customer_id":cust_id.get(),
        "name":cust_name.get(),
        "phone":cust_phone.get(),
        "address":cust_address.get()
        })
        messagebox.showinfo("Success","Customer Added!")
        clear_customer()

    except errors.DuplicateKeyError:
        messagebox.showerror("Error","Customer ID already exists!")

def update_customer():
    customers.update_one(
    {"customer_id":cust_id.get()},
    {"$set":{
    "name":cust_name.get(),
    "phone":cust_phone.get(),
    "address":cust_address.get()
    }}
    )
    messagebox.showinfo("Updated","Customer Updated")

def delete_customer():
    customers.delete_one({"customer_id":cust_id.get()})
    messagebox.showinfo("Deleted","Customer Deleted")
    clear_customer()

def view_customers():

    window=tk.Toplevel(root)
    window.title("Customer List")

    tree=ttk.Treeview(window,
    columns=("ID","Name","Phone","Address"),
    show="headings")

    tree.heading("ID",text="Customer ID")
    tree.heading("Name",text="Name")
    tree.heading("Phone",text="Phone")
    tree.heading("Address",text="Address")

    tree.pack(fill="both",expand=True)

    for c in customers.find():
        tree.insert("", "end",
        values=(c["customer_id"],c["name"],c["phone"],c["address"]))

tk.Button(customer_frame,text="Add Customer",bg="#ff914d",fg="white",command=add_customer).grid(row=4,column=0,columnspan=2,pady=5)
tk.Button(customer_frame,text="Update Customer",bg="#3498db",fg="white",command=update_customer).grid(row=5,column=0,columnspan=2,pady=5)
tk.Button(customer_frame,text="Delete Customer",bg="#e74c3c",fg="white",command=delete_customer).grid(row=6,column=0,columnspan=2,pady=5)
tk.Button(customer_frame,text="View Customers",bg="#f39c12",fg="white",command=view_customers).grid(row=7,column=0,columnspan=2,pady=5)


# =====================================================
# FOOD SECTION
# =====================================================

food_frame = tk.LabelFrame(root,text="Food Section",
font=("Arial",12,"bold"),bg="#e6fff2",padx=10,pady=10)

food_frame.grid(row=1,column=1,padx=20,pady=20)

tk.Label(food_frame,text="Food ID",bg="#e6fff2").grid(row=0,column=0)
food_id=tk.Entry(food_frame)
food_id.grid(row=0,column=1)

tk.Label(food_frame,text="Food Name",bg="#e6fff2").grid(row=1,column=0)
food_name=tk.Entry(food_frame)
food_name.grid(row=1,column=1)

tk.Label(food_frame,text="Price",bg="#e6fff2").grid(row=2,column=0)
food_price=tk.Entry(food_frame)
food_price.grid(row=2,column=1)

def clear_food():
    food_id.delete(0,tk.END)
    food_name.delete(0,tk.END)
    food_price.delete(0,tk.END)

def add_food():
    try:
        foods.insert_one({
        "food_id":food_id.get(),
        "food_name":food_name.get(),
        "price":float(food_price.get())
        })

        messagebox.showinfo("Success","Food Added!")
        clear_food()

    except errors.DuplicateKeyError:
        messagebox.showerror("Error","Food ID already exists!")

def update_food():
    foods.update_one(
    {"food_id":food_id.get()},
    {"$set":{
    "food_name":food_name.get(),
    "price":float(food_price.get())
    }}
    )
    messagebox.showinfo("Updated","Food Updated")

def delete_food():
    foods.delete_one({"food_id":food_id.get()})
    messagebox.showinfo("Deleted","Food Deleted")
    clear_food()

def view_food():

    window=tk.Toplevel(root)
    window.title("Food Items")

    tree=ttk.Treeview(window,
    columns=("ID","Name","Price"),
    show="headings")

    tree.heading("ID",text="Food ID")
    tree.heading("Name",text="Food Name")
    tree.heading("Price",text="Price")

    tree.pack(fill="both",expand=True)

    for f in foods.find():
        tree.insert("", "end",
        values=(f["food_id"],f["food_name"],f["price"]))

tk.Button(food_frame,text="Add Food",bg="#00b894",fg="white",command=add_food).grid(row=3,column=0,columnspan=2,pady=5)
tk.Button(food_frame,text="Update Food",bg="#00cec9",fg="white",command=update_food).grid(row=4,column=0,columnspan=2,pady=5)
tk.Button(food_frame,text="Delete Food",bg="#d63031",fg="white",command=delete_food).grid(row=5,column=0,columnspan=2,pady=5)
tk.Button(food_frame,text="View Food",bg="#27ae60",fg="white",command=view_food).grid(row=6,column=0,columnspan=2,pady=5)


# =====================================================
# ORDER SECTION
# =====================================================

order_frame = tk.LabelFrame(root,text="Order Section",
font=("Arial",12,"bold"),bg="#e6f2ff",padx=10,pady=10)

order_frame.grid(row=1,column=2,padx=20,pady=20)

tk.Label(order_frame,text="Order ID",bg="#e6f2ff").grid(row=0,column=0)
order_id=tk.Entry(order_frame)
order_id.grid(row=0,column=1)

tk.Label(order_frame,text="Customer ID",bg="#e6f2ff").grid(row=1,column=0)
order_customer=tk.Entry(order_frame)
order_customer.grid(row=1,column=1)

tk.Label(order_frame,text="Food ID",bg="#e6f2ff").grid(row=2,column=0)
order_food=tk.Entry(order_frame)
order_food.grid(row=2,column=1)

tk.Label(order_frame,text="Quantity",bg="#e6f2ff").grid(row=3,column=0)
order_quantity=tk.Entry(order_frame)
order_quantity.grid(row=3,column=1)

def clear_order():
    order_id.delete(0,tk.END)
    order_customer.delete(0,tk.END)
    order_food.delete(0,tk.END)
    order_quantity.delete(0,tk.END)

def create_order():
    try:

        food=foods.find_one({"food_id":order_food.get()})

        if food:

            total=int(order_quantity.get())*food["price"]

            orders.insert_one({
            "order_id":order_id.get(),
            "customer_id":order_customer.get(),
            "food_id":order_food.get(),
            "quantity":int(order_quantity.get()),
            "total_price":total,
            "status":"Pending"
            })

            messagebox.showinfo("Success","Order Created!")
            clear_order()

        else:
            messagebox.showerror("Error","Food not found")

    except errors.DuplicateKeyError:
        messagebox.showerror("Error","Order ID exists")

def delete_order():
    orders.delete_one({"order_id":order_id.get()})
    messagebox.showinfo("Deleted","Order Deleted")
    clear_order()

def view_orders():

    window=tk.Toplevel(root)
    window.title("Orders")

    tree=ttk.Treeview(window,
    columns=("OrderID","CustomerID","FoodID","Qty","Total","Status"),
    show="headings")

    tree.heading("OrderID",text="Order ID")
    tree.heading("CustomerID",text="Customer ID")
    tree.heading("FoodID",text="Food ID")
    tree.heading("Qty",text="Quantity")
    tree.heading("Total",text="Total")
    tree.heading("Status",text="Status")

    tree.pack(fill="both",expand=True)

    for o in orders.find():
        tree.insert("", "end",
        values=(o["order_id"],o["customer_id"],o["food_id"],
        o["quantity"],o["total_price"],o["status"]))

tk.Button(order_frame,text="Create Order",bg="#0984e3",fg="white",command=create_order).grid(row=4,column=0,columnspan=2,pady=5)
tk.Button(order_frame,text="Delete Order",bg="#c0392b",fg="white",command=delete_order).grid(row=5,column=0,columnspan=2,pady=5)
tk.Button(order_frame,text="View Orders",bg="#6c5ce7",fg="white",command=view_orders).grid(row=6,column=0,columnspan=2,pady=5)



root.mainloop()
