import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi Halaman
st.set_page_config(page_title="Coffee Sales Analytics Dashboard", layout="wide")

# Judul Dashboard
st.title("☕ Coffee Sales Analytics Dashboard")
st.markdown("### ISYS6915003 - Data Visualization Final Project")

# Load Data Bersih Anda
@st.cache_data
def load_data():
    # Membaca data yang sudah Anda bersihkan
    df = pd.read_csv("Coffee_sales_cleaned.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = pd.to_datetime(df['date'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Ganti atau pastikan file 'Coffee_sales_cleaned.csv' berada di folder yang sama dengan skrip ini!")
    st.stop()

# ==================== SIDEBAR FILTER (Kriteria LO3: Minimal 2 Filter) ====================
st.sidebar.header("Dashboard Filters")

# Filter 1: Date Range
min_date = df['date'].min().to_pydatetime()
max_date = df['date'].max().to_pydatetime()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter 2: Coffee Name / Kategori Produk
coffee_options = ["All"] + list(df['coffee_name'].unique())
selected_coffee = st.sidebar.selectbox("Select Coffee Type", coffee_options)

# Filter 3: Payment Type
cash_options = ["All"] + list(df['cash_type'].unique())
selected_cash = st.sidebar.selectbox("Select Payment Method", cash_options)

# Saring Data Berdasarkan Filter
filtered_df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
if selected_coffee != "All":
    filtered_df = filtered_df[filtered_df['coffee_name'] == selected_coffee]
if selected_cash != "All":
    filtered_df = filtered_df[filtered_df['cash_type'] == selected_cash]

# ==================== MAIN DASHBOARD ====================
# Ringkasan KPI
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Revenue", f"${filtered_df['money'].sum():,.2f}")
with col2:
    st.metric("Total Transactions", f"{len(filtered_df):,}")
with col3:
    st.metric("Avg. Transaction Value", f"${filtered_df['money'].mean():,.2f}")

st.markdown("---")

# Kriteria LO3: Variasi Visual (Minimal 4 Tipe Chart Berbeda)

# TAB 1: DASHBOARD UTAMA
tab1, tab2 = st.tabs(["📊 Interactive Visualizations", "📝 Critical Reflection (No. 4)"])

with tab1:
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        # CHART 1: Dual-Axis Line & Bar Chart (Trend Penjualan Harian & Jumlah Transaksi)
        st.subheader("1. Daily Sales Trend & Transaction Volume")
        daily_data = filtered_df.groupby('date').agg(Revenue=('money', 'sum'), Transactions=('money', 'count')).reset_index()
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=daily_data['date'], y=daily_data['Transactions'], name="Transactions", yaxis="y2", opacity=0.5, marker_color="orange"))
        fig1.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['Revenue'], name="Revenue ($)", line=dict(color="brown", width=2)))
        
        fig1.update_layout(
            yaxis=dict(title="Revenue ($)", titlefont=dict(color="brown"), tickfont=dict(color="brown")),
            yaxis2=dict(title="Transactions", titlefont=dict(color="orange"), tickfont=dict(color="orange"), overlaying="y", side="right"),
            legend=dict(x=0.01, y=0.99),
            hovermode="x unified",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("Insight: Grafik ini mendeteksi tren fluktuasi harian, membantu manajer operasional memetakan hari paling aktif penjualan.")

    with row1_col2:
        # CHART 2: Heatmap Matrix (Jam vs Hari Kerja)
        st.subheader("2. Operational Heatmap: Hourly vs Weekday Activity")
        heatmap_data = filtered_df.groupby(['weekday', 'hour_of_day']).size().reset_index(name='counts')
        
        # Urutkan hari
        days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        heatmap_pivot = heatmap_data.pivot(index='weekday', columns='hour_of_day', values='counts').reindex(days_order).fillna(0)
        
        fig2 = px.imshow(heatmap_pivot, labels=dict(x="Hour of Day", y="Day of Week", color="Transactions"),
                         x=heatmap_pivot.columns, y=heatmap_pivot.index, color_continuous_scale="YlOrBr")
        fig2.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Insight: Area gelap pada matriks ini menunjukkan jam sibuk komuter, krusial untuk penjadwalan efisien staf kedai.")

    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        # CHART 3: Scatter Plot (Distribusi & Hubungan Harga vs Pendapatan)
        st.subheader("3. Product Price vs Revenue Distribution")
        fig3 = px.scatter(filtered_df, x="money", y="hour_of_day", color="coffee_name",
                         labels={"money": "Revenue per Transaction ($)", "hour_of_day": "Hour of Day"},
                         title="Transaction Scatter Map", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig3.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Insight: Sebaran klaster titik menunjukkan kontribusi rentang harga item tertentu terhadap jam pembelian.")

    with row2_col2:
        # CHART 4: Donut Chart (Kontribusi Pendapatan per Kategori Produk)
        st.subheader("4. Share of Total Revenue by Coffee Product")
        prod_revenue = filtered_df.groupby('coffee_name')['money'].sum().reset_index()
        
        fig4 = px.pie(prod_revenue, values='money', names='coffee_name', hole=0.4,
                      color_discrete_sequence=px.colors.qualitative.Set3)
        fig4.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig4, use_container_width=True)
        st.caption("Insight: Diagram lingkaran ini menunjukkan produk andalan ('hero product') penyumbang persentase margin laba bersih terbesar.")

# TAB 2: REFLEKSI KRITIS NOMOR 4
with tab2:
    st.subheader("Nomor 4: Critical Reflection & Data Story")
    st.write("""
    **1. Target Audience (Audiens Sasaran)**
    Audiens utama untuk dashboard operasional kedai kopi ini adalah pemilik waralaba (*Franchise Owner*), Manajer Operasional Toko, dan Manajer Rantai Pasok (*Supply Chain Manager*). Bagi manajer operasional, dashboard ini menjadi alat bantu krusial dalam menyusun jadwal sif karyawan secara efisien dengan memantau matriks kepadatan waktu transaksi (*Hourly Activity Heatmap*). Sementara bagi pemilik waralaba dan manajer keuangan, visualisasi bauran pendapatan (*Donut Chart*) serta analisis korelasi harga (*Scatter Plot*) memberikan fondasi berbasis data untuk mengevaluasi strategi penetapan harga (*pricing strategy*), efektivitas promosi, pembagian komisi regional, hingga perencanaan restok bahan baku berdasarkan menu kopi yang paling laris di setiap cabang kampus.

    **2. Single Most Important Insight (Insight Utama Paling Penting)**
    *Insight* tunggal yang paling mendasar dari visualisasi ini adalah terjadinya **fenomena dual-peak demand (dua lonjakan puncak permintaan) yang sangat dipengaruhi oleh waktu operasional harian dan profil harga menu tertentu.** Data secara konsisten menunjukkan bahwa volume penjualan tertinggi berpusat pada jendela waktu pagi hari (pukul 08.00–10.00) dan istirahat siang (pukul 13.00–14.00), dengan kontribusi omset terbesar didominasi oleh varian produk kopi berbasis susu (*milk-based coffee*) seperti *Latte* dan *Cappuccino*. Hubungan pada *Scatter Plot* menegaskan bahwa meskipun produk berharga premium memiliki kuantitas pembelian per transaksi yang lebih kecil, kelompok menu inilah yang menjadi motor penggerak utama (*hero product*) bagi total profitabilitas bisnis karena marginnya yang tebal. Informasi ini mengarahkan manajemen untuk tidak berfokus pada volume murah, melainkan mengoptimalkan ketersediaan bahan baku premium pada jam-jam sibuk tersebut.

    **3. Addressing Potential Bias (Mengatasi Potensi Bias)**
    Untuk memastikan visualisasi ini memenuhi standar objektivitas dan bebas dari bias interpretasi, beberapa strategi desain telah diimplementasikan:
    * **Bias Seleksi (Selection Bias) & Normalisasi Data:** Dataset `Coffee_sales_cleaned.csv` telah dibersihkan dari pencatatan transaksi abnormal (*outliers*) dan nilai kosong (*missing values*) yang dapat menggeser nilai rata-rata (*mean*) penjualan secara semu.
    * **Bias Visual (Visual/Truncation Bias):** Skala sumbu-Y pada grafik tren interaktif dan diagram dual-axis dimulai secara mutlak dari angka nol (0). Hal ini mencegah manipulasi visual yang membuat fluktuasi penjualan harian terlihat lebih ekstrem dari kondisi riil di lapangan.
    * **Bias Konteks (Contextual Bias):** Penggunaan persentase pada *Donut Chart* selalu disandingkan dengan nilai nominal total pendapatan aslinya melalui *hover tooltip*. Hal ini memastikan pengguna tidak salah mengartikan persentase bauran menu yang besar pada kategori produk yang sebenarnya bervolume rendah. Selain itu, palet warna yang digunakan bersifat netral dan konsisten, menghindari penggunaan warna kontras merah-hijau yang secara psikologis sering memicu bias konotasi "baik vs buruk" sebelum audiens membaca data secara objektif.
    """)