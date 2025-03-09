import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd

orders_df = pd.read_csv('./E-Commerce Public Dataset/orders_dataset.csv')
q_1_df = pd.read_csv('./E-Commerce Public Dataset/Dashboard Data/q_1_df.csv')
payment_analysis = pd.read_csv('./E-Commerce Public Dataset/Dashboard Data/payment_analysis.csv')
cust_merged_gdf = pd.read_csv('./E-Commerce Public Dataset/Dashboard Data/cust_merged_gdf.csv')
sellers_merged_gdf = pd.read_csv('./E-Commerce Public Dataset/Dashboard Data/sellers_merged_gdf.csv')
rfm_df = pd.read_csv('./E-Commerce Public Dataset/Dashboard Data/rfm_df.csv')
order_reviews = pd.read_csv("./E-Commerce Public Dataset/order_reviews_dataset.csv")

def to_datetime(df):
    date_list = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 
                'order_delivered_customer_date','order_estimated_delivery_date'] 
    for col in date_list:
        df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S', errors='coerce')

to_datetime(orders_df)
to_datetime(payment_analysis)

geojson_path = "./E-Commerce Public Dataset/brazil-states.geojson"  
brazil_states_gdf = gpd.read_file(geojson_path)

st.sidebar.title("E-Commerce Dashboard")
page = st.sidebar.radio("Go to", ["Business Overview", "Customer & Seller Segmentation"])

if page == "Business Overview":
    st.title("Business Overview")

    min_date, max_date = orders_df['order_purchase_timestamp'].min(), orders_df['order_purchase_timestamp'].max()
    date_range = st.sidebar.date_input("Select Date Range", [min_date.date(), max_date.date()], min_value=min_date.date(), max_value=max_date.date())
    filtered_orders = orders_df[(orders_df['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) &
                                (orders_df['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))]
    
    order_status_counts = filtered_orders['order_status'].value_counts()
    st.subheader("Order Status Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Delivered", f"{order_status_counts.get('delivered', 0):,}")
    col2.metric("Processing", f"{order_status_counts.get('processing', 0):,}")
    col3.metric("Canceled", f"{order_status_counts.get('canceled', 0):,}")
    
    filtered_pay_df = payment_analysis[
        (payment_analysis['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) & 
        (payment_analysis['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))
    ]
    rev_status_counts = filtered_pay_df['payment_type'].value_counts()

    st.subheader("Revenue Summary")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Credit Card", f"R$ {rev_status_counts.get('credit_card', 0):,}")
    col2.metric("Boleto", f"R$ {rev_status_counts.get('boleto', 0):,}")
    col3.metric("Debit Card", f"R$ {rev_status_counts.get('debit_card', 0):,}")
    col4.metric("Voucher", f"R$ {rev_status_counts.get('voucher', 0):,}")


    st.subheader("Orders Over Time")
    orders_time_series = filtered_orders.groupby(filtered_orders['order_purchase_timestamp'].dt.date).size()
    fig = px.line(orders_time_series, x=orders_time_series.index, y=orders_time_series.values, labels={'y': "Number of Orders", 'x': "Date"})
    st.plotly_chart(fig)

    st.subheader("Best and Worst Performing Categories")
    category_counts = q_1_df['product_category_name'].value_counts()
    col1, col2 = st.columns(2)
    col1.write("Top 5 Categories")
    col1.dataframe(category_counts.head(5))
    col2.write("Bottom 5 Categories")
    col2.dataframe(category_counts.tail(5))

elif page == "Customer & Seller Segmentation":
    st.title("Customer & Seller Segmentation")

    with st.container():
        st.markdown("## Customer Distribution")
        fig = px.choropleth(
            cust_merged_gdf,
            geojson=brazil_states_gdf,  
            locations="sigla",  
            featureidkey="properties.sigla", 
            color="customer_count",
            hover_name="name",
            title="Customer Distribution in Brazil",
            color_continuous_scale="viridis"
        )
        fig.update_geos(fitbounds="locations", visible=False) 
        st.plotly_chart(fig)
    
    with st.container():
            st.markdown("## Seller Distribution")
            fig = px.choropleth(
                sellers_merged_gdf,
                geojson=brazil_states_gdf,
                locations="sigla",
                featureidkey="properties.sigla",
                color="customer_count",
                hover_name="name",
                title="Seller Distribution in Brazil",
                color_continuous_scale="viridis"
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
    
    st.subheader("RFM Segmentation")
    st.dataframe(rfm_df)
    
    st.subheader("Customer Reviews")
    review_counts = order_reviews['review_score'].value_counts().sort_index()
    fig = px.bar(review_counts, x=review_counts.index, y=review_counts.values, labels={'x': "Review Score", 'y': "Count"})
    st.plotly_chart(fig)