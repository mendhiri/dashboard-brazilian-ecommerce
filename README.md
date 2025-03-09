# dashboard-brazilian-ecommerce

### Overview
Business Analysis Dashboard ini dikembangkan menggunakan **Streamlit** untuk menganalisis performa bisnis berdasarkan data penjualan, segmentasi pelanggan (RFM Analysis), pola geografis pelanggan & penjual, serta performa kategori produk. Dashboard ini memberikan wawasan visual yang interaktif untuk mendukung pengambilan keputusan bisnis.

---

## Fitur
###  Overview
- Menampilkan ringkasan tujuan dan cakupan analisis bisnis.

### RFM Analysis
- Segmentasi pelanggan berdasarkan **Recency, Frequency, dan Monetary (RFM)**.
- Visualisasi distribusi **Recency** menggunakan histogram.
- Tabel rangkuman statistik RFM (mean, median, min, max).

### Geographical Insights
- Analisis distribusi **pelanggan berdasarkan kota**.
- Analisis distribusi **penjual berdasarkan negara bagian**.
- Grafik interaktif untuk mengeksplorasi pola geografis.

###  Sales Performance
- **Kategori produk dengan pendapatan tertinggi**.
- **Tren pendapatan bulanan** untuk memantau kinerja penjualan.
- Grafik interaktif untuk memahami pola pembelian.

---

## Instalasi & Menjalankan Aplikasi
### 1️ Prasyarat
Pastikan sudah telah menginstal **Python 3.7+** dan memiliki paket berikut:
```sh
pip install streamlit pandas plotly geopandas
```

### 2️ Clone Repository
```sh
https://github.com/mendhiri/dashboard-brazilian-ecommerce
cd dashboard-brazilian-ecommerce
```

### 3️ Jalankan Aplikasi
```sh
streamlit run app.py
```


