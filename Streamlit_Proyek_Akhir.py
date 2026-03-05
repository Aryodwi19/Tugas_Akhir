import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Air Quality Analysis Dashboard", layout="wide", page_icon="🌤️")

# --- DATA LOADING & CLEANING (CACHED) ---
@st.cache_data
def load_data():
    # Asumsikan file CSV berada di dalam folder ini
    data_folder = "C:/Users/aryod/OneDrive/PRSA_Data_20130301-20170228"
    
    # Jika folder tidak ada, buat dummy data atau beri peringatan
    if not os.path.exists(data_folder):
        st.error(f"Folder '{data_folder}' tidak ditemukan! Pastikan dataset sudah diekstrak ke folder tersebut.")
        return pd.DataFrame()

    csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.csv')]
    
    df_list = [pd.read_csv(f) for f in csv_files]
    df = pd.concat(df_list, ignore_index=True)
    
    # Cleaning Data
    df = df.reset_index(drop=True)
    df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]], errors="coerce")
    df = df.dropna(subset=["datetime"])
    df = df.sort_values(by="datetime").set_index("datetime")
    
    # Imputasi Missing Values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    category_cols = df.select_dtypes(include=['object']).columns
    for col in category_cols:
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna("Unknown")
            
    df = df.ffill().bfill()
    df = df[~df.index.duplicated(keep="last")]
    
    # Feature Engineering Tambahan
    df['hour'] = df.index.hour
    df['day_name'] = df.index.day_name()
    df['is_weekend'] = df.index.dayofweek.map({
        0: 'Weekday', 1: 'Weekday', 2: 'Weekday',
        3: 'Weekday', 4: 'Weekday', 5: 'Weekend', 6: 'Weekend'
    })
    
    return df

# Memuat data
df = load_data()

# --- SIDEBAR ---
st.sidebar.title("☁️ Air Quality Dashboard")
st.sidebar.markdown("""
**Nama:** Aryo Dwi Haryanto  
**Email:** aryodwi122@gmail.com  
**ID Dicoding:** aryo_dwi_h
""")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Pilih Halaman:", ["Gambaran Data", "Analisis & Visualisasi", "Kesimpulan & Saran"])

# --- MAIN CONTENT ---
if df.empty:
    st.stop() # Menghentikan eksekusi jika data tidak ada

if menu == "Gambaran Data":
    st.title("Gambaran Dataset Kualitas Udara (Beijing 2013-2017)")
    st.write("Dataset ini merupakan gabungan dari 12 stasiun pemantauan kualitas udara di Beijing.")
    
    st.subheader("Cuplikan Data (Top 5)")
    st.dataframe(df.head())
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Statistik Deskriptif")
        st.dataframe(df.describe())
    
    with col2:
        st.subheader("Total Missing Value (Setelah Cleaning)")
        st.dataframe(df.isnull().sum(), column_config={"0": "Missing Values"})

elif menu == "Analisis & Visualisasi":
    st.title("Visualisasi & Explanatory Analysis")
    
    # --- Pertanyaan 1 ---
    st.subheader("1. Pola dan Tren Konsentrasi PM2.5 (2013-2017)")
    tab1, tab2 = st.tabs(["Pola Musiman (Bulanan)", "Tren Tahunan per Stasiun"])
    
    with tab1:
        monthly_trend = df['PM2.5'].resample('ME').mean()
        fig, ax = plt.subplots(figsize=(15, 6))
        ax.plot(monthly_trend, color='darkblue', marker='o', linewidth=2)
        ax.set_title("Pola Musiman PM2.5 di Beijing (2013-2017)", fontsize=14)
        ax.set_ylabel("Konsentrasi PM2.5 (µg/m³)")
        ax.set_xlabel("Tahun")
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.fill_between(monthly_trend.index, monthly_trend, color='skyblue', alpha=0.3)
        st.pyplot(fig)
        st.info("💡 **Insight:** Polusi memuncak pada musim dingin (Desember-Februari) dan terendah pada musim panas (Juni-Agustus).")
        
    with tab2:
        yearly_station_trend = df.groupby(['year', 'station'])['PM2.5'].mean().unstack()
        fig, ax = plt.subplots(figsize=(15, 7))
        yearly_station_trend.plot(kind='line', marker='s', ax=ax, linewidth=2)
        ax.set_title("Tren Penurunan PM2.5 Tahunan Berdasarkan Stasiun", fontsize=14)
        ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
        ax.set_xlabel("Tahun")
        ax.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, linestyle=':', alpha=0.6)
        st.pyplot(fig)

    # --- Pertanyaan 2 ---
    st.markdown("---")
    st.subheader("2. Distribusi PM2.5 dan Polutan Lainnya")
    pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.violinplot(data=df[pollutants], palette="Set3", inner="quartile", ax=ax)
    ax.set_yscale("log")
    ax.set_title("Kepadatan dan Distribusi Polutan Utama (Skala Logaritma)", fontsize=14)
    ax.set_ylabel("Konsentrasi Polutan (µg/m³)")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig)
    st.info("💡 **Insight:** CO adalah polutan paling dominan. O3 memiliki distribusi yang unik karena dipengaruhi reaksi fotokimia siang hari.")

    # --- Pertanyaan 3 ---
    st.markdown("---")
    st.subheader("3. Korelasi Antar Polutan")
    existing_pollutants = [p for p in pollutants if p in df.columns]
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df[existing_pollutants].corr(), cmap='coolwarm', annot=True, fmt=".2f", linewidths=.5, ax=ax)
    ax.set_title("Heatmap Korelasi Antar Polutan")
    st.pyplot(fig)
    st.info("💡 **Insight:** Polutan kendaraan/industri (PM2.5, PM10, CO, NO2) berkorelasi positif kuat. Sebaliknya, O3 sering berkorelasi negatif dengan polutan primer tersebut.")

    # --- Pertanyaan 4 ---
    st.markdown("---")
    st.subheader("4. Rata-rata Konsentrasi PM2.5 Tertinggi dan Terendah per Stasiun")
    station_averages = df.groupby('station')['PM2.5'].mean().sort_values()
    colors = ['green' if (x == station_averages.min()) else 'red' if (x == station_averages.max()) else 'yellow' for x in station_averages]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    station_averages.plot(kind='bar', color=colors, edgecolor='black', alpha=0.8, ax=ax)
    ax.set_xlabel("Stasiun Pemantauan", fontsize=12)
    ax.set_ylabel("Rata-rata Konsentrasi PM2.5", fontsize=12)
    ax.axhline(y=station_averages.mean(), color='black', linestyle='--', label=f'Rata-rata Kota ({station_averages.mean():.1f})')
    ax.legend()
    ax.grid(axis='y', linestyle=':', alpha=0.7)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
    st.info(f"💡 **Insight:** Stasiun tertinggi adalah **{station_averages.idxmax()}**, sedangkan yang terendah adalah **{station_averages.idxmin()}**.")

    # --- Analisis Tambahan ---
    st.markdown("---")
    st.subheader("📌 Analisis Lanjutan (Pengaruh Cuaca & Waktu)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Tren Polusi per Jam**")
        hourly_avg = df.groupby('hour')['PM2.5'].mean()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(hourly_avg.index, hourly_avg, marker='o', color='darkorange')
        ax.fill_between(hourly_avg.index, hourly_avg, color='orange', alpha=0.2)
        ax.set_xticks(range(0, 24, 2))
        ax.set_xlabel("Jam (00:00 - 23:00)")
        ax.set_ylabel("PM2.5")
        ax.grid(True, linestyle='--')
        st.pyplot(fig)
        
    with col2:
        st.write("**Hari Kerja vs Akhir Pekan**")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(x='is_weekend', y='PM2.5', data=df, hue='is_weekend', palette={'Weekday': 'blue', 'Weekend': 'red'}, legend=False, ax=ax)
        ax.set_yscale('log')
        ax.set_xlabel("Kategori Hari")
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)


elif menu == "Kesimpulan & Saran":
    st.title("📝 Kesimpulan & Rekomendasi")
    
    st.subheader("Kesimpulan Analisis")
    st.markdown("""
    1. **Pola Musiman:** Tingkat PM2.5 sangat parah di musim dingin (penggunaan pemanas/batu bara) dan menurun drastis di musim panas. Meskipun sempat ada tren penurunan polusi yang baik hingga 2016, terjadi lonjakan kembali pada tahun 2017.
    2. **Karakteristik Polutan:** CO adalah polutan yang mendominasi di udara secara jumlah. PM2.5, PM10, CO, dan NO2 memiliki sumber yang berkaitan (kendaraan & industri fosil).
    3. **Ozon (O3):** Memiliki sifat yang terbalik; ketika polutan partikel turun, O3 cenderung naik (terutama siang hari yang cerah).
    4. **Lokasi Stasiun:** Stasiun *Nongzhanguan* memiliki polusi terburuk, biasanya daerah padat penduduk/industri. *Dingling* memiliki udara terbaik karena kemungkinan berada di pinggiran kota.
    5. **Aktivitas Harian:** Polusi memuncak pada malam hari hingga pagi hari akibat aktivitas komuter dan suhu malam yang menjebak polutan. Tidak ada perbedaan drastis antara hari kerja dan akhir pekan.
    """)
    
    st.subheader("Saran dan Rekomendasi")
    st.info("""
    * **Fokus Musim Dingin:** Pemerintah harus mengetatkan regulasi emisi dan pembakaran batu bara saat memasuki musim dingin (Desember - Februari).
    * **Kebijakan Transportasi:** Tingginya korelasi NO2 dan PM2.5 di jam sibuk menunjukkan perlunya pembatasan kendaraan berbahan bakar fosil dan percepatan transisi ke transportasi publik listrik.
    * **Perlakuan Khusus Area Merah:** Stasiun dengan polusi tinggi (seperti Nongzhanguan) memerlukan intervensi langsung, seperti memperbanyak Ruang Terbuka Hijau (RTH) atau pembatasan pabrik di sekitarnya.
    * **Pengawasan Konsisten:** Peningkatan polusi di tahun 2017 adalah *warning* bahwa kebijakan lingkungan tidak boleh kendor meskipun tahun-tahun sebelumnya sudah terlihat ada perbaikan.
    """)
    
    st.success("Terima kasih telah melihat Dashboard Analisis Kualitas Udara Beijing! 🌍")
