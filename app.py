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
to_datetime(q_1_df)

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

    tab1, tab2, tab3 = st.tabs(['Orders payment',"Trend Over Time", "Top Category"])
    
    with tab1:
        filtered_pay_df = payment_analysis[
            (payment_analysis['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) & 
            (payment_analysis['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))
        ]
        rev_status_counts = filtered_pay_df['payment_type'].value_counts()

        rev_percentage = (rev_status_counts / rev_status_counts.sum()) * 100
        rev_percentage = (rev_status_counts / rev_status_counts.sum()) * 100
        df_percentage = pd.DataFrame({
            "Metode Pembayaran": rev_percentage.index,
            "Persentase": rev_percentage.values,
            "Total": "Total 100%"  
        })

        st.subheader("Revenue Summary")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Credit Card", f"R$ {rev_status_counts.get('credit_card', 0):,}")
        col2.metric("Boleto", f"R$ {rev_status_counts.get('boleto', 0):,}")
        col3.metric("Debit Card", f"R$ {rev_status_counts.get('debit_card', 0):,}")
        col4.metric("Voucher", f"R$ {rev_status_counts.get('voucher', 0):,}")

        color_scale = ["#FFD700", "#FFA500", "#FF8C00", "#FF4500"]

        fig = px.bar(
            df_percentage,
            x="Persentase",
            y="Total", 
            color='Metode Pembayaran',
            text="Persentase", 
            labels={"Persentase": "Percentage (%)", "Total": ""},
            title="Payment Methods Distributions by Revenue",
            orientation="h",
            color_discrete_sequence=color_scale 
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%", textposition="inside",
        )

        st.plotly_chart(fig)

    with tab2:
        st.subheader("Orders Over Time")
        orders_time_series = filtered_orders.groupby(filtered_orders['order_purchase_timestamp'].dt.date).size()
        fig = px.line(orders_time_series, x=orders_time_series.index, y=orders_time_series.values, labels={'y': "Number of Orders", 'x': "Date"})
        st.plotly_chart(fig)

        orders_time_series = (
            filtered_orders.groupby(filtered_orders['order_purchase_timestamp'].dt.to_period('M'))
            .size()
        )
        orders_time_series.index = orders_time_series.index.astype(str)

        fig = px.line(
            orders_time_series, 
            x=orders_time_series.index, 
            y=orders_time_series.values, 
            labels={'y': "Number of Orders", 'x': "Month"},
            title="Orders Over Time (Monthly)"
        )

        st.subheader("Orders Over Time (Monthly)")
        st.plotly_chart(fig)

    with tab3:
        st.subheader("Top 10 Product Categories")
        filtered = q_1_df[(q_1_df['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) &
                                (q_1_df['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))]
        top_categories = (
            filtered.groupby("product_category_name")["order_id"]
            .nunique()
            .sort_values(ascending=False)
            .head(10)
        )

        fig = px.bar(
            top_categories,
            x=top_categories.values,
            y=top_categories.index,
            orientation="h",
            labels={"x": "Total Transactions", "y": "Product Category"},
            title="Total Transactions by Product Category",
            text=top_categories.values
        )

        fig.update_traces(marker_color="teal", textposition="outside")
        fig.update_layout(yaxis_categoryorder="total ascending") 

        st.plotly_chart(fig)

        avg_price_per_category = (
            filtered.groupby("product_category_name")["price"]
            .mean()
            .sort_values(ascending=False)
            .head(9) 
        )

        fig = px.bar(
            avg_price_per_category,
            x=avg_price_per_category.values,
            y=avg_price_per_category.index,
            orientation="h",
            labels={"x": "Average Price (BRL)", "y": "Products Category"},
            title="Average Price by Category",
            text=avg_price_per_category.round(2),
        )

        fig.update_traces(marker_color="darkred", textposition="outside")
        fig.update_layout(yaxis_categoryorder="total ascending")  

        st.plotly_chart(fig)    


elif page == "Customer & Seller Segmentation":
    st.title("Customer & Seller Segmentation")

    tab1, tab2, tab3 = st.tabs(['Location Segmentation', "Payment & Review Segmentation", "RFM Analysis"])

    with tab1:
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
    
    with tab2:
        with st.container():
            payment_binning = payment_analysis[['order_id', 'customer_id','payment_type', 'payment_value']]
            customer_payment = payment_binning.groupby("customer_id")["payment_value"].sum().reset_index()
            customer_payment.rename(columns={"payment_value": "total_payment"}, inplace=True)
            bins = [0, 50, 100, 200, 500, 1000, 5000, 14000]
            labels = ["0-50", "50-100", "100-200", "200-500", "500-1000", "1000-5000", "5000+"]

            customer_payment["payment_bin"] = pd.cut(customer_payment["total_payment"], bins=bins, labels=labels, right=False)
            customer_payment.groupby('payment_bin').agg({'customer_id':'count'})

            binned = customer_payment[['payment_bin', 'total_payment']].groupby("payment_bin").agg('sum').reset_index()

            fig = px.bar(
                binned,
                x="payment_bin",
                y="total_payment",
                text="total_payment", 
                labels={"payment_bin": "Bin Pembayaran", "total_payment": "Total Pembayaran (BRL)"},
                title="Total Payment by each bin (BRL)",
                color="total_payment",  
                color_continuous_scale="magma",
                hover_data={"total_payment": ":,.2f"}, 
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)
        
        st.subheader("Customer Reviews")
        review_counts = order_reviews['review_score'].value_counts().sort_index()
        fig = px.bar(review_counts, x=review_counts.index, y=review_counts.values, labels={'x': "Review Score", 'y': "Count"})
        st.plotly_chart(fig)
    
    with tab3:
        st.subheader("Distribution of RFM Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig_recency = px.histogram(rfm_df, x="Recency", nbins=50, title="Recency Distribution", color_discrete_sequence=["#FF7F50"])
            st.plotly_chart(fig_recency, use_container_width=True)

        with col2:
            fig_frequency = px.histogram(rfm_df, x="Frequency", nbins=20, title="Frequency Distribution", color_discrete_sequence=["#FFD700"])
            st.plotly_chart(fig_frequency, use_container_width=True)

        with col3:
            fig_monetary = px.histogram(rfm_df, x="Monetary", nbins=50, title="Monetary Distribution", color_discrete_sequence=["#32CD32"])
            st.plotly_chart(fig_monetary, use_container_width=True)

        st.subheader("Scatter Plot of RFM Metrics")
        fig_rf = px.scatter(rfm_df, x="Recency", y="Frequency", size="Monetary", title="Recency vs Frequency (Bubble Chart)", color="Monetary",
                            color_continuous_scale="Viridis", opacity=0.7)
        st.plotly_chart(fig_rf, use_container_width=True)
        
        st.subheader("3D Visualization of RFM Segmentation")
        fig_3d = px.scatter_3d(rfm_df, x="Recency", y="Frequency", z="Monetary", color="Monetary",
                                color_continuous_scale="Plasma", opacity=0.8, title="3D RFM Scatter Plot")
        st.plotly_chart(fig_3d, use_container_width=True)

        st.subheader("RFM Data")
        st.dataframe(rfm_df)