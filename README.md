Dokumentasi Proyek: Analisis Data Kualitas Udara (Air Quality Data Analysis)
# Import library yang digunakan untuk analisis dan visualisasi
import pandas as pd          # Mengelola data dalam bentuk tabel (DataFrame)

import numpy as np           # Operasi numerik dan komputasi matematis

import matplotlib.pyplot as plt  # Membuat grafik dan visualisasi

import seaborn as sns        # Visualisasi statistik dengan style lebih informatif

import zipfile               # Untuk mengekstrak file ZIP dataset

import os                    # Navigasi direktori dan pencarian file

# Mengatur style default visualisasi seaborn
sns.set(style="whitegrid")


# 1. GATHERING DATA
# Path lokasi file ZIP dataset
zip_path = r"C:\Users\aryod\Downloads\Air-quality-dataset.zip"

# Direktori tempat ekstraksi file ZIP
extract_dir = r"C:\Users\aryod\Downloads\air_quality_data"

# Membuka file ZIP dan mengekstrak seluruh isinya
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_dir)

# List untuk menyimpan lokasi file CSV hasil ekstraksi
csv_files = []

# Menelusuri folder hasil ekstraksi untuk mencari seluruh file .csv
for root, dirs, files in os.walk(extract_dir):

for file in files:

if file.endswith(".csv"):                       # Jika file berakhiran .csv

csv_files.append(os.path.join(root, file))      # Simpan path file

# Membaca seluruh file CSV ke dalam list DataFrame
df_list = [pd.read_csv(f) for f in csv_files]

# Menggabungkan semua DataFrame menjadi satu tabel besar
df = pd.concat(df_list, ignore_index=True)


# 2. ASSESSING DATA


print(df.info())                    # Informasi struktur kolom dan tipe data

print(df.describe())                           # Statistik deskriptif kolom numerik

print("Missing values per column")              #Program akan menampilkan tulisan "Missing values per column" di konsol.

print(df.isnull().sum())                                # Jumlah nilai hilang per kolom

print("Duplikasi baris:", df.duplicated().sum())           # Jumlah baris duplikat


# 3. CLEANING DATA


# Membuat kolom datetime dari kolom year, month, day, hour
df["datetime"] = pd.to_datetime(df[['year', 'month', 'day', 'hour']], errors='coerce')

# Menghapus baris dengan datetime yang gagal di-convert
df.dropna(subset=["datetime"], inplace=True)

# Mengurutkan berdasarkan datetime dan menjadikannya sebagai index dataframe
df = df.sort_values("datetime").set_index("datetime")

# Mengisi nilai kosong pada kolom numerik dengan median
df.fillna(df.median(numeric_only=True), inplace=True)

# Mengisi nilai kosong pada kolom kategorikal dengan nilai mode (yang paling sering muncul)
cat_cols = df.select_dtypes(include='object').columns

for col in cat_cols:
   
df[col] = df[col].fillna(df[col].mode()[0])

# Menghapus duplikasi berdasarkan index (datetime)
df = df[~df.index.duplicated(keep='last')]

# Menampilkan data yang sudah dibersihkan
print("\nData setelah cleaning:")

print(df.head())

print(df['station'].unique()[:20])   # Menampilkan 20 nama stasiun pertama

# 4. EXPLORATORY DATA ANALYSIS (EDA)


# 1. DISTRIBUSI POLUTAN UTAMA (BOXPLOT)
pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]  # Daftar polutan utama

plt.figure(figsize=(10,6))

sns.boxplot(data=df[pollutants])    # Membuat boxplot untuk seluruh polutan

plt.title("Distribusi Polutan Utama") #Program akan menampilkan tulisan "Distribusi Polutan Utama" di konsol.

plt.xticks(rotation=45)             # Rotasi label agar mudah dibaca

plt.yscale("log")                   # Skala log untuk mengatasi outlier

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.show()

# 2. HEATMAP KORELASI ANTAR VARIABEL NUMERIK
numeric_df = df.select_dtypes(include=['int64', 'float64'])  # Mengambil hanya kolom bertipe numerik (int64 dan float64)

if "No" in numeric_df.columns:       # Jika kolom "No" ada di dataframe (sering berupa nomor urut), kolom ini dihapus, karena tidak relevan dan dapat mengganggu analisis korelasi
numeric_df = numeric_df.drop(columns=["No"])

plt.figure(figsize=(14,10))     # Membuat ukuran figure untuk heatmap

sns.heatmap(                            # Membuat heatmap menggunakan seaborn
    numeric_df.corr(),               # Menghasilkan matriks korelasi antar kolom numerik
    cmap='coolwarm',                # Warna visualisasi (biru = korelasi negatif, merah = positif)
    annot=True,                      # Menampilkan nilai korelasi
    fmt=".2f",                        # Format angka dengan 2 decimal
    linewidth=.5                     # Jarak antar sel pada heatmap
)
plt.title("Heatmap Korelasi Numerik")
plt.show()

# 3. TREN HARIAN PM2.5
plt.figure(figsize=(12,6))
df["PM2.5"].plot(color="steelblue", linewidth=1)
plt.title("Tren Harian PM2.5", fontsize=14)
plt.xlabel("Tahun")
plt.ylabel("Mikrogram per meter kubik µg/m³")
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()

# 4. TREN BULANAN PM2.5
monthly_avg = df['PM2.5'].resample("ME").mean()   # Rata-rata per bulan

plt.figure(figsize=(15,5))
monthly_avg.plot(marker='o')
plt.xlabel("Bulan")
plt.ylabel("Mikrogram per meter kubik (µg/m³)")
plt.title("Rata-rata PM2.5 per Bulan")
plt.show()

# 5. TREN TAHUNAN PM2.5
yearly_avg = df.groupby(df.index.year)['PM2.5'].mean()

plt.figure(figsize=(15,5))
yearly_avg.plot(marker='o')
plt.xlabel("Tahun")
plt.ylabel("Mikrogram per meter kubik (µg/m³)")
plt.title("Rata-rata PM2.5 per Tahun")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.show()

# 6. ANALISIS MUSIM
df['month'] = df.index.month           # Tambah kolom bulan
df['season'] = df['month'].map({       # Mapping bulan → musim
    12:'Winter', 1:'Winter', 2:'Winter',
    3:'Spring', 4:'Spring', 5:'Spring',
    6:'Summer', 7:'Summer', 8:'Summer',
    9:'Autumn', 10:'Autumn', 11:'Autumn' 
})

plt.figure(figsize=(8,5))
df.groupby("season")["PM2.5"].mean().plot(kind="bar")
plt.title("Rata-rata PM2.5 per Musim")
plt.xlabel("Musim")
plt.ylabel("Mikrogram per meter kubik (µg/m³)")
plt.show()

# 7. CALENDAR HEATMAP PM2.5
df['day_of_year'] = df.index.dayofyear   # Hari ke- dalam setahun

calendar = df.pivot_table(
    values="PM2.5",
    index=df.index.year,         # Baris = Tahun
    columns='day_of_year'        # Kolom = Hari ke-
)
calendar = calendar.sort_index()

plt.figure(figsize=(18,6))
sns.heatmap(calendar, cmap='viridis', linewidth=0)
plt.title("Calendar Heatmap PM2.5")
plt.xlabel("Hari ke-")
plt.ylabel("Tahun")
plt.show()

# 8. PERBANDINGAN ANTAR STASIUN
station_avg = df.groupby("station")["PM2.5"].mean().sort_values()

plt.figure(figsize=(12,6))
station_avg.plot(kind="bar")
plt.title("Rata-rata PM2.5 per Stasiun")
plt.xlabel("Stasiun")
plt.ylabel("PM2.5")
plt.xticks(rotation=45)
plt.show()
