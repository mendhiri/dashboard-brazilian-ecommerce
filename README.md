## Brazilian E-Commerce Dashboard

Proyek ini merupakan analisis data dan visualisasi dashboard dari *Brazilian E-Commerce Public Dataset by Olist*. Analisis dilakukan untuk menjawab pertanyaan bisnis utama terkait performa penjualan, kategori produk, pola geografis pelanggan dan penjual, serta segmentasi pelanggan berdasarkan perilaku pembelian.

### Daftar Isi
- [Deskripsi Proyek](#deskripsi-proyek)
- [Struktur Folder](#struktur-folder)
- [Dataset](#dataset)
- [Instalasi & Menjalankan](#instalasi--menjalankan)
- [Fitur Analisis](#fitur-analisis)
- [Hasil Utama](#hasil-utama)
- [Referensi](#referensi)

## Deskripsi Proyek
Analisis dilakukan menggunakan Python (pandas, seaborn, matplotlib, geopandas) dan divisualisasikan dalam bentuk dashboard interaktif menggunakan Streamlit. Studi kasus ini bertujuan memberikan insight terkait perilaku konsumen, tren penjualan, serta rekomendasi strategi bisnis berbasis data.

## Struktur Folder
```
analysis-notebook.ipynb         # Notebook utama analisis data
app.py                         # Dashboard Streamlit
requirements.txt               # Daftar dependensi Python
E-Commerce Public Dataset/     # Folder dataset mentah dan hasil olahan
	 brazil_geo.json
	 brazil-states.geojson
	 customers_dataset.csv
	 ...
	 Dashboard Data/            # Data hasil wrangling/analisis
		  cust_merged_gdf.csv
		  payment_analysis.csv
		  q_1_df.csv
		  rfm_df.csv
		  sellers_merged_gdf.csv
```

## Dataset
Dataset utama diambil dari [Kaggle: Brazilian E-Commerce Public Dataset by Olist](https://doi.org/10.34740/KAGGLE/DSV/195341). Dataset ini berisi data transaksi, pelanggan, penjual, produk, pembayaran, review, dan geolokasi dari marketplace Olist di Brazil tahun 2016-2018.

## Instalasi & Menjalankan
1. **Clone repository**
	```
	git clone https://github.com/mendhiri/dashboard-brazilian-ecommerce.git
	cd dashboard-brazilian-ecommerce
	```
2. **Install dependencies**
	```
	pip install -r requirements.txt
	```
3. **Jalankan notebook analisis**
	Buka `analysis-notebook.ipynb` di Jupyter Notebook atau VS Code.
4. **Jalankan dashboard Streamlit**
	```
	streamlit run app.py
	```

## Fitur Analisis
- Data wrangling dan eksplorasi data (EDA)
- Visualisasi tren penjualan harian dan bulanan
- Analisis performa penjualan per kategori produk
- Analisis geospasial distribusi pelanggan dan penjual
- Segmentasi pelanggan berdasarkan pembayaran dan review
- RFM Analysis (Recency, Frequency, Monetary)

## Hasil Utama
- Penjualan meningkat signifikan sejak November 2016
- Kategori produk dengan penjualan tertinggi: tempat tidur & meja kamar mandi, kecantikan & kesehatan, olahraga & santai
- Sebaran pelanggan dan penjual terpusat di São Paulo dan Rio de Janeiro
- Mayoritas pelanggan hanya melakukan satu kali transaksi, dengan nilai transaksi terbanyak di bawah 150 BRL
- Rekomendasi: strategi retensi pelanggan, promosi pada kategori unggulan, dan optimalisasi logistik di wilayah utama

## Referensi
- Olist, and André Sionek. (2018). Brazilian E-Commerce Public Dataset by Olist [Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/195341
- Code for Germany. (n.d.). Click that hood. GitHub. https://github.com/codeforgermany/click_that_hood


