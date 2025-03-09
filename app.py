import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# dataset dibaca sebagai modularisasi
geoloc_df = pd.read_csv("./E-Commerce Public Dataset/geolocation_dataset.csv")
cust_df = pd.read_csv("./E-Commerce Public Dataset/customers_dataset.csv")
orders_df = pd.read_csv("./E-Commerce Public Dataset/orders_dataset.csv")
orders_items_df = pd.read_csv("./E-Commerce Public Dataset/order_items_dataset.csv")
orders_payment_df = pd.read_csv("./E-Commerce Public Dataset/order_payments_dataset.csv")
products_df = pd.read_csv("./E-Commerce Public Dataset/products_dataset.csv")
sellers_df = pd.read_csv("./E-Commerce Public Dataset/sellers_dataset.csv")
order_reviews = pd.read_csv("./E-Commerce Public Dataset/order_reviews_dataset.csv")

# Load the dataset 
big_orders = orders_df.merge(orders_payment_df, on='order_id', how='left')\
             .merge(order_reviews, on='order_id', how='left').merge(cust_df[['customer_id','customer_city', 'customer_state']], on='customer_id', how='left').dropna()

big_orders = big_orders[['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp',	'order_approved_at',
            'order_delivered_carrier_date',	'order_delivered_customer_date',	'order_estimated_delivery_date',
            'payment_type','payment_value', 'review_score', 'customer_city', 'customer_state']]

# Load external CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply CSS from an external file
load_css("style.css")


st.markdown("</div>", unsafe_allow_html=True) 

with st.sidebar:

    st.markdown("<h1> Olist Brazilian Dashboard</h1>", unsafe_allow_html=True)

    card_html = f"""
    <a href="#" class="card">
        <h5 class="card-title">Noteworthy Technology Acquisitions 2021</h5>
        <p class="card-text">Here are the biggest enterprise technology acquisitions of 2021 so far, in reverse chronological order.</p>
    </a>
    """

    st.markdown(card_html, unsafe_allow_html=True)
    
    values = st.slider(
        label='Select a range of values',
        min_value=0, max_value=100, value=(0, 100)
    )
    st.write('Values:', values)

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Kolom 1")
        st.image("https://static.streamlit.io/examples/dog.jpg")
    
    with col2:
        st.header("Kolom 2")
        st.image("https://static.streamlit.io/examples/dog.jpg")
    
    with col3:
        st.header("Kolom 3")
        st.image("https://static.streamlit.io/examples/owl.jpg")

with st.container():
    st.write("Inside the container")
    
    x = np.random.normal(15, 5, 250)
 
    fig, ax = plt.subplots()
    ax.hist(x=x, bins=15)
    st.pyplot(fig) 
 

st.markdown("<p class='main-title'>Welcome to the Styled Streamlit App!</p>", unsafe_allow_html=True)
st.write("This is a simple example of a Streamlit app with custom CSS styling.")
if st.button("Click Me"):
    st.success("Button Clicked!")