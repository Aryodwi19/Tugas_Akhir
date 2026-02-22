# Air Quality Data Analysis Dashboard

## Gambaran Proyek
Proyek ini bertujuan untuk menganalisis data kualitas udara (Air Quality) dari berbagai stasiun pemantauan. Analisis berfokus pada tren polutan utama (seperti PM2.5), perbandingan antar stasiun, serta pola musiman/bulanan untuk memahami kondisi kualitas udara secara lebih baik.

## 1. Dataset
* Dataset ini memuat data pengukuran kualitas udara dari beberapa stasiun di Beijing. Variabel utama yang tersedia:
* PM2.5
* PM10
* SO₂
* NO₂
* CO
* O₃
* Informasi waktu: year, month, day, hour
* station: nama stasiun pemantau

## 2. Pertanyaan Bisnis (Business Questions)
* Apa saja penyebab utama meningkatnya kadar Pm 2.5?

* Bagaimana perkembangan PM2. 5 dari waktu kewaktu (harian , bulanan dan musiman )?

* Bagaimana perubahan rata-rata konsentrasi PM2.5 di seluruh stasiun pemantauan di Beijing pada periode 2013–2017, dan apakah terjadi tren penurunan yang konsisten dari tahun ke tahun?

## 3. Ringkasan Data Cleaning
Ringkasan tahapan pembersihan data:

* Menggabungkan semua file CSV dari ZIP menjadi satu DataFrame.

* Membuat kolom datetime dari kombinasi year–month–day–hour.

* Menghapus baris dengan datetime yang tidak valid.

* Mengurutkan data berdasarkan waktu dan menjadikan datetime sebagai index.

* Mengisi nilai hilang:

Numerik → median

Kategorikal → mode

* Menghapus baris duplikat berdasarkan index.


## 4. Ringkasan Exploratory Data Analysis (EDA)

* Analisis yang dilakukan meliputi:

* Distribusi polutan utama (boxplot).

* Heatmap korelasi antar polutan.

* Tren harian, bulanan, dan tahunan untuk PM2.5.

* Analisis musiman untuk PM2.5.

* Calendar heatmap untuk PM2.5.

* Perbandingan rata-rata polutan antar stasiun.

* Ranking stasiun berdasarkan konsentrasi rata-rata polutan.

* Semua visualisasi ini ditampilkan baik di notebook maupun dashboard Streamlit.

## 5. Dashboard Streamlit

* Dashboard yang dibangun menyediakan fitur:

* Pemilihan stasiun dan polutan melalui sidebar.

* Tren waktu untuk polutan tertentu pada stasiun yang dipilih.

* Distribusi polutan (histogram + KDE).

* Heatmap korelasi antar polutan.

* Rata-rata bulanan PM2.5.

* Perbandingan antar stasiun dengan smoothing 7 hari.

* Ranking stasiun berdasarkan rata-rata polutan.

* Dashboard dirancang agar mudah digunakan dan responsif.

## 6. Cara Menjalankan Dashboard
1. Instal dependensi

Jika tersedia requirements.txt:

pip install -r requirements.txt

Jika tidak, install dependensi inti berikut:

pip install streamlit pandas seaborn matplotlib requests

2. Jalankan aplikasi

Pastikan file app.py berada di direktori proyek.

streamlit run app.py

3. Buka dashboard

Aplikasi akan berjalan otomatis di browser pada:

http://localhost:8501

