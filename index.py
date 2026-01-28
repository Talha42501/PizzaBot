import streamlit as st
import random
import time

st.set_page_config(page_title="Qureshi's PizzaBot", page_icon="🍕")

if "order" not in st.session_state:
    st.session_state.order = {}
if "step" not in st.session_state:
    st.session_state.step = 0
if "order_id" not in st.session_state:
    st.session_state.order_id = random.randint(10000, 99999)
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
st.sidebar.info(f"🆔 **Order ID: #{st.session_state.order_id}**")

if st.session_state.step == 0:
    bot(f"Welcome! I am your Pizza Assistant. Your session ID is **#{st.session_state.order_id}**.")
    bot("Would you like to see our menu and place an order?")
    choice = st.radio("Choose an option:", ["Select...", "Yes", "No"], index=0)
    
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
    p_list = ", ".join(st.session_state.order["names"])
    bot(f"How many units of **{p_list}** do you want?")
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
    bot("Any extra toppings or drinks?")
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
    
    st.success(f"### 🎉 Order Confirmed! ID: #{st.session_state.order_id}")
    
    st.table({
        "Order Detail": ["Order ID", "Pizzas", "Quantity", "Size", "Crusts", "Toppings", "Drink", "Total Bill"],
        "Value": [
            f"#{st.session_state.order_id}",
            ", ".join(o["names"]), 
            o["qty"], 
            o["size"], 
            ", ".join(o["crusts"]), 
            ", ".join(o["toppings"]) if o["toppings"] else "None", 
            o["drink"],
            f"Rs. {grand_total}"
        ]
    })

    with st.status("Tracing your order...") as s:
        st.write("Baking your selections... 🍕")
        time.sleep(2)
        st.write("Handing over to delivery partner... 🛵")
        time.sleep(2)
        s.update(label="Order Delivered! Enjoy! 😋", state="complete")

    if st.button("Place Another Order"):
        st.session_state.clear()
        st.rerun()
