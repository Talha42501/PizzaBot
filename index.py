import streamlit as st
import random
import time
import pandas as pd
import os

st.set_page_config(page_title="Qureshi's PizzaBot", page_icon="🍕")

if "order" not in st.session_state:
    st.session_state.order = {}
if "step" not in st.session_state:
    st.session_state.step = 0
if "order_id" not in st.session_state:
    st.session_state.order_id = random.randint(10000, 99999)
    
def save_to_csv(order_data):
    file_name = "pizza_orders.csv"
    df_new = pd.DataFrame([order_data])
    if os.path.isfile(file_name):
        df_old = pd.read_csv(file_name)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
        df_final.to_csv(file_name, index=False)
    else:
        df_new.to_csv(file_name, index=False)
        
MENU = {
    "Classic": ["Margherita", "Fajita", "Tikka", "Cheese"],
    "Premium": ["Pepperoni Feast", "Veggie Supreme", "BBQ Chicken"],
    "Exclusive": ["Cheese Burst Special", "Qureshi's Delight"]
}
PRICES = {
    "Size": {"Small": 600, "Medium": 1000, "Large": 1400},
    "Crust": {"Thin": 0, "Thick": 100, "Cheese Burst": 200},
    "Topping": 50,
    "Drink": {"None": 0, "Coke": 120, "Sprite": 120, "Water": 60}
}

def bot(msg):
    st.markdown(f"**🤖 PizzaBot:** {msg}")
    
st.sidebar.title("🛡️ Admin Portal")
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    user_input = st.sidebar.text_input("Admin Username")
    pass_input = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if user_input == "admin" and pass_input == "pizza123":
            st.session_state.admin_logged_in = True
            st.rerun()
        else:
            st.sidebar.error("Ghalat Password!")
else:
    st.sidebar.success("Logged in as Admin")
    if st.sidebar.checkbox("📂 View Sales Database"):
        if os.path.exists("pizza_orders.csv"):
            data = pd.read_csv("pizza_orders.csv")
            st.sidebar.write(f"Total Orders: {len(data)}")
            st.subheader("📋 Customer Orders History")
            st.dataframe(data)
        else:
            st.sidebar.info("Abhi tak koi data nahi hai.")
    
    if st.sidebar.button("Logout"):
        st.session_state.admin_logged_in = False
        st.rerun()
st.title("🍕 Qureshi's PizzaBot")
st.write(f"--- Session ID: **#{st.session_state.order_id}** ---")

if st.session_state.step == 0:
    bot("Welcome! Would you like to place an order today?")
    choice = st.radio("Select an option:", ["Select...", "Yes", "No"], index=0)
    if st.button("Proceed"):
        if choice == "Yes": st.session_state.step = 1; st.rerun()
        elif choice == "No": st.session_state.step = -1; st.rerun()

if st.session_state.step == -1:
    bot("Thank you for visiting! Have a great day. 👋")

if st.session_state.step == 1:
    bot("Please select a category and your favorite pizzas:")
    cat = st.selectbox("Category:", [""] + list(MENU.keys()))
    if cat:
        pizzas = st.multiselect(f"{cat} Menu:", MENU[cat])
        if pizzas and st.button("Next"):
            st.session_state.order["names"] = pizzas
            st.session_state.step = 2; st.rerun()

if st.session_state.step == 2:
    bot("How many pizzas would you like to order?")
    qty = st.number_input("Quantity:", min_value=1, max_value=20, value=1)
    if st.button("Next"):
        st.session_state.order["qty"] = qty
        st.session_state.step = 3; st.rerun()

if st.session_state.step == 3:
    bot("Select your preferred Size and Crust type(s):")
    sz = st.selectbox("Size:", ["", "Small", "Medium", "Large"])
    crusts = st.multiselect("Crust Types:", ["Thin", "Thick", "Cheese Burst"])
    if sz and crusts and st.button("Next"):
        st.session_state.order["size"] = sz
        st.session_state.order["crusts"] = crusts
        st.session_state.step = 4; st.rerun()

if st.session_state.step == 4:
    bot("Almost done! Please provide your delivery address and select a drink:")
    addr = st.text_area("Delivery Address:")
    drnk = st.selectbox("Drink:", ["None", "Coke", "Sprite", "Water"])
    tops = st.multiselect("Toppings:", ["Pepperoni", "Mushrooms", "Olives", "Jalapenos"])
    if st.button("Finish Order"):
        if not addr: st.error("Address is required for delivery!")
        else:
            st.session_state.order["address"] = addr
            st.session_state.order["drink"] = drnk
            st.session_state.order["toppings"] = tops
            st.session_state.step = 5; st.rerun()

if st.session_state.step == 5:
    o = st.session_state.order
    total = ((PRICES["Size"][o["size"]] + PRICES["Crust"][o["crusts"][0]] + (len(o["toppings"])*50)) * o["qty"]) + PRICES["Drink"][o["drink"]]
    
    final_data = {
        "OrderID": st.session_state.order_id,
        "Customer_Address": o["address"],
        "Pizzas": ", ".join(o["names"]),
        "Qty": o["qty"],
        "Bill": f"Rs. {total}",
        "Time": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    if "saved" not in st.session_state:
        save_to_csv(final_data)
        st.session_state.saved = True

    st.success(f"🎉 🎉 Order Confirmed! ID: #{st.session_state.order_id}")
    st.table(pd.DataFrame([final_data]).T.rename(columns={0: "Details"}))
    
    with st.status("Processing your order...") as s:
        time.sleep(3)
        s.update(label="Delivered! Enjoy your meal 😋", state="complete")

    if st.button("Place New Order"):
        st.session_state.clear()
        st.rerun()
