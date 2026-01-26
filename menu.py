import streamlit as st
import random
import time

st.set_page_config(page_title="PizzaBot")

# Initialize session state
if "order" not in st.session_state:
    st.session_state.order = {}
if "step" not in st.session_state:
    st.session_state.step = 0

st.title("🍕 PizzaBot – Online Pizza Ordering")

def bot(msg):
    st.markdown(f"**🤖 PizzaBot:** {msg}")

def user(msg):
    st.markdown(f"**🧑 You:** {msg}")

# ---------------- Step 0: Welcome ----------------
if st.session_state.step == 0:
    bot("Welcome! I can help you order pizza. Would you like to see our menu?")
    choice = st.radio("Choose an option:", ["Yes", "No"], index=0, key="choice0")
    
    if choice and "welcome" not in st.session_state:
        user(choice)
        st.session_state.welcome = choice
        if choice.lower() == "yes":
            st.session_state.step = 1
        else:
            bot("No worries! Come back anytime you crave pizza 🍕. Have a great day! 👋")
            st.stop()

# ---------------- Step 1: Size ----------------
if st.session_state.step == 1:
    bot("Which pizza size would you like?")
    size = st.selectbox("Select Size:", ["", "Small", "Medium", "Large"], index=0, key="size_input")

    if size != "" and "size" not in st.session_state.order:
        user(size)
        st.session_state.order["size"] = size
        st.session_state.step = 2

# ---------------- Step 2: Crust ----------------
if st.session_state.step == 2:
    bot("Which crust do you prefer?")
    crust = st.selectbox("Select Crust:", ["", "Thin", "Thick", "Cheese Burst"], index=0, key="crust_input")

    if crust != "" and "crust" not in st.session_state.order:
        user(crust)
        st.session_state.order["crust"] = crust
        st.session_state.step = 3

# ---------------- Step 3: Toppings ----------------
if st.session_state.step == 3:
    bot("Choose toppings (you can select multiple):")
    toppings = st.multiselect(
        "Select Toppings:",
        ["Pepperoni", "Mushrooms", "Olives", "Jalapenos", "Extra Cheese"],
        key="toppings_input"
    )

    if toppings and "toppings" not in st.session_state.order:
        user(", ".join(toppings))
        st.session_state.order["toppings"] = ", ".join(toppings)
        st.session_state.step = 4

# ---------------- Step 4: Drink ----------------
if st.session_state.step == 4:
    bot("Would you like a drink? (optional)")
    drink_options = ["None", "Coke", "Sprite", "Water"]
    drink = st.selectbox("Select Drink:", drink_options, index=0, key="drink_input")

    # Save drink only when user actively selects
    if "drink" not in st.session_state.order:
        if drink != "None":
            user(drink)
            st.session_state.order["drink"] = drink
            st.session_state.step = 5
        elif drink == "None" and st.button("No Drink"):
            user("No drink")
            st.session_state.order["drink"] = "None"
            st.session_state.step = 5

# ---------------- Step 5: Confirm Order ----------------
if st.session_state.step == 5:
    order_id = random.randint(1000, 9999)
    st.session_state.order["order_id"] = order_id

    bot(f""" **Order Confirmed!**
Order ID: **#{order_id}**

 Size: {st.session_state.order['size']}  
 Crust: {st.session_state.order['crust']}  
 Toppings: {st.session_state.order['toppings']}  
 Drink: {st.session_state.order['drink']}
""")
    bot("Your pizza is being prepared 🍕")
    time.sleep(2)
    bot("Pizza is baking 🔥")
    time.sleep(2)
    bot("Out for delivery 🚚")
    time.sleep(2)
    bot("Delivered! Enjoy your meal 😋")
