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

st.title("🍕 Qureshi's PizzaBot")
st.sidebar.info(f"🆔 **Current Order ID: #{st.session_state.order_id}**")

if st.session_state.step == 0:
    bot(f"Welcome! Your unique order ID for this session is **#{st.session_state.order_id}**.")
    choice = st.radio("Ready to order?", ["Select...", "Yes", "No"], index=0)
    
    if st.button("Proceed"):
        if choice == "Yes":
            st.session_state.step = 1
            st.rerun()
        elif choice == "No":
            st.session_state.step = -1
            st.rerun()

if st.session_state.step == -1:
    bot("No worries! Come back anytime. 👋")
    if st.button("Restart New Order"):
        st.session_state.clear()
        st.rerun()
        
if st.session_state.step == 1:
    bot("Choose your category and select your pizzas:")
    cat = st.selectbox("Select Category:", [""] + list(MENU.keys()))
    if cat:
        pizzas = st.multiselect(f"Select your {cat} Pizzas:", MENU[cat])
        if pizzas and st.button("Next"):
            st.session_state.order["names"] = pizzas
            st.session_state.step = 2
            st.rerun()

if st.session_state.step == 2:
    bot(f"How many units of each do you want?")
    qty = st.number_input("Total Quantity:", min_value=1, max_value=20, value=1)
    if st.button("Confirm Quantity"):
        st.session_state.order["qty"] = qty
        st.session_state.step = 3
        st.rerun()
        
if st.session_state.step == 3:
    bot("Select Size and Crust types:")
    sz = st.selectbox("Size:", ["", "Small", "Medium", "Large"])
    crusts = st.multiselect("Crust Types:", ["Thin", "Thick", "Cheese Burst"])
    if sz and crusts and st.button("Next"):
        st.session_state.order["size"] = sz
        st.session_state.order["crusts"] = crusts
        st.session_state.step = 4
        st.rerun()

if st.session_state.step == 4:
    bot("Toppings & Drinks:")
    tops = st.multiselect("Toppings (Rs. 50 each):", ["Pepperoni", "Mushrooms", "Olives", "Jalapenos"])
    drnk = st.selectbox("Drink:", ["None", "Coke", "Sprite", "Water"])
    if st.button("Finalize Order"):
        st.session_state.order["toppings"] = tops
        st.session_state.order["drink"] = drnk
        st.session_state.step = 5
        st.rerun()

if st.session_state.step == 5:
    o = st.session_state.order
    base_p = PRICES["Size"][o["size"]]
    crust_p = PRICES["Crust"][o["crusts"][0]] 
    topping_total = len(o["toppings"]) * PRICES["Topping"]
    drink_p = PRICES["Drink"][o["drink"]]
    grand_total = ((base_p + crust_p + topping_total) * o["qty"]) + drink_p
    final_record = {
        "OrderID": st.session_state.order_id,
        "Pizzas": ", ".join(o["names"]),
        "Qty": o["qty"],
        "Size": o["size"],
        "Crusts": ", ".join(o["crusts"]),
        "TotalBill": grand_total,
        "Time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if "saved" not in st.session_state:
        save_to_csv(final_record)
        st.session_state.saved = True

    st.success(f"### 🎉 Order Confirmed! ID: #{st.session_state.order_id}")
    st.table(pd.DataFrame([final_record]).T.rename(columns={0: "Details"}))

    with st.status("Processing...") as s:
        time.sleep(2)
        st.write("Order saved to database! ✅")
        s.update(label="Order Delivered! 😋", state="complete")

    if st.button("View All Orders (Admin)"):
        if os.path.exists("pizza_orders.csv"):
            st.dataframe(pd.read_csv("pizza_orders.csv"))
    
    if st.button("New Order"):
        st.session_state.clear()
        st.rerun()
