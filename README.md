Air Quality Analysis Dashboard: Beijing (2013-2017)
Proyek ini bertujuan untuk melakukan analisis mendalam mengenai kualitas udara di 12 stasiun pemantauan utama di Beijing selama periode 2013 hingga 2017. Analisis difokuskan pada polutan utama seperti PM2.5, PM10, SO2, NO2, CO, dan O3 untuk memberikan wawasan yang berguna bagi kebijakan pengendalian emisi.

# Pertanyaan Bisnis
Bagaimana pola dan tren konsentrasi PM2.5 di setiap stasiun pemantauan kualitas udara di Beijing pada periode 2013-2017?

Bagaimana distribusi PM2.5 serta polutan lain (PM10, NO2, SO2, CO, O3) selama tahun 2013-2017?

Bagaimana korelasi antara PM2.5 dengan polutan lainnya?

Stasiun mana yang memiliki rata-rata konsentrasi PM2.5 tertinggi dan terendah?

# Panduan Menjalankan Dashboard
Ikuti langkah-langkah di bawah ini untuk menjalankan proyek di perangkat lokal Anda dengan aman.

# 1. Pengaturan Lingkungan (Setting Environment)
Gunakan virtual environment untuk menghindari konflik versi antar library.
Menggunakan venv (Bawaan Python):
# Masuk ke direktori proyek
cd tugas_akhir

# Membuat virtual environment
python -m venv venv

# Mengaktifkan environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 2. Instalasi Dependensi
pip install --upgrade pip
pip install -r requirements.txt

# 3. Menjalankan Aplikasi
Jalankan dashboard menggunakan perintah berikut:
streamlit run dashboard/Streamlit_Proyek_Akhir.py

# Alur Analisis Data

Data Wrangling: Menggabungkan 12 file CSV dari berbagai stasiun pemantauan.

Cleaning: Mengatasi missing values menggunakan metode median (numerik) dan mode (kategorikal), serta penyesuaian indeks datetime.

EDA: Eksplorasi distribusi polutan dan statistik deskriptif per stasiun.

Visualization: Pembuatan grafik tren musiman, heatmap korelasi, dan perbandingan antar stasiun.

# Kesimpulan Utama
Pola Musiman: Polusi PM2.5 mencapai puncaknya pada Musim Dingin (Desember-Februari) dan berada di titik terendah pada Musim Panas.

Stasiun Terpolusi: Stasiun Nongzhanguan memiliki rata-rata PM2.5 tertinggi, sementara stasiun Dingling adalah yang terbersih.

Korelasi: Polutan PM2.5, PM10, CO, dan NO2 memiliki korelasi positif yang sangat kuat, menunjukkan sumber emisi yang serupa (kendaraan dan industri).

Pengaruh Angin: Terdapat korelasi negatif antara kecepatan angin (WSPM) dan PM2.5; angin yang lebih kencang membantu menyebarkan polutan.

Profil Penulis

Nama: Aryo Dwi Haryanto

Email: aryodwi122@gmail.com

ID Dicoding: aryo_dwi_h

Email: aryodwi122@gmail.com

ID Dicoding: aryo_dwi_h
