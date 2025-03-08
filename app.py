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

# Load external CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply CSS from an external file
load_css("style.css")

# Streamlit layout with sidebar styling
st.sidebar.header("Navigation")
st.sidebar.markdown("<div class='sidebar-container'>", unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ["Home", "About"])
st.sidebar.markdown("</div>", unsafe_allow_html=True)

if page == "Home":
    st.markdown("<p class='main-title'>Welcome to the Styled Streamlit App!</p>", unsafe_allow_html=True)
    st.write("This is a simple example of a Streamlit app with custom CSS styling.")
    if st.button("Click Me"):
        st.success("Button Clicked!")
    with st.container():
        st.write("Inside the container")
        
        x = np.random.normal(15, 5, 250)
    
        fig, ax = plt.subplots()
        ax.hist(x=x, bins=15)
        st.pyplot(fig) 

elif page == "About":
    st.markdown("<p class='main-title'>About This App</p>", unsafe_allow_html=True)
    st.write("This app demonstrates how to use CSS in Streamlit.")
