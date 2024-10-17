# Analisa Data Sederhana - Sistem Peminjaman Sepeda

## Deskripsi
Proyek ini berfokus pada analisis data eksploratif (EDA) dari Bike Sharing Dataset, yang mencakup peminjaman sepeda berdasarkan waktu, cuaca, dan kondisi lainnya. Notebook ini bertujuan untuk memahami pola dan faktor yang memengaruhi jumlah penyewa sepeda, serta menangani outlier dalam data.

## Tautan Dashboard
[Bike Sharing Dashboard](https://bike-sharing-u9bns7byrx9t2tsxmb2tbj.streamlit.app)

## Dataset
Dataset yang digunakan dalam analisis ini mencakupL
* day.csv: Data harian dengan 731 observasi.
* hour.csv: Data per jam dengan 16,018 observasi.

Variabel penting dalam dataset meliputi:
* cnt: Jumlah penyewa sepeda.
* casual: Penyewa kasual.
* registered: Penyewa terdaftar.
* temp: Suhu.
* hum: Kelembapan.
* windspeed: Kecepatan angin.
* season: Musim (1: Musim Semi, 2: Musim Panas, 3: Musim Gugur, 4: Musim Dingin).

## Langkah-langkah Analisis
1. Pengolahan Outlier
  * Menggunakan metode median untuk mengganti outlier di dataset harian.
  * Menghapus outlier berdasarkan nilai Interquartile Range (IQR) di dataset per jam.

2. Visualisasi Outlier
  Membuat boxplot untuk mendeteksi dan menganalisis outlier dalam data.

![download](https://github.com/user-attachments/assets/8e6d74d6-4345-4cf7-bbbd-e44ddd54f281)


3. Exploratory Data Analysis (EDA)
  * Menggunakan analisis deskriptif untuk memahami karakteristik dataset.
  * Melakukan analisis korelasi antar variabel untuk menentukan hubungan signifikan.
![download](https://github.com/user-attachments/assets/5c7256a3-298c-4872-9ff4-94e386675ff7)

![download](https://github.com/user-attachments/assets/651043de-52d6-4524-b028-4a4193c2202c)


4. Analisis Tren Penyewaan
  * Mengelompokkan dan menghitung jumlah penyewaan berdasarkan waktu dan faktor lainnya.
  * Menerapkan dekomposisi deret waktu untuk memisahkan komponen tren, musiman, dan residual.

## Temuan Utama
1. Hubungan Waktu dan Penyewa
  Terdapat korelasi positif yang signifikan antara jam dalam sehari dan jumlah penyewa, menunjukkan bahwa penyewaan meningkat pada jam-jam tertentu.

![download](https://github.com/user-attachments/assets/964c28e0-cf73-47c6-bba9-1a2ccb03098b)

2. Perbandingan Penyewa
  * Penyewaan cenderung lebih tinggi pada hari kerja dibandingkan dengan hari libur.
  * Aktivitas penyewaan paling tinggi terlihat pada hari Rabu.

![download](https://github.com/user-attachments/assets/289d5709-e5c8-42ba-bb69-b9c122a00e63)

3. Musim Terhadap Penyewaan
  Musim panas dan gugur menunjukkan jumlah penyewa tertinggi, sementara musim semi memiliki jumlah penyewa terendah.

![download](https://github.com/user-attachments/assets/1c354a4d-783b-44f2-ae87-2c8f02e7b518)

4. Tren Penyewaan
  Penyewaan sepeda mengalami fluktuasi signifikan dengan pola musiman yang jelas, meningkat pada bulan-bulan hangat dan menurun saat musim dingin.

![download](https://github.com/user-attachments/assets/e89c868f-312a-4a20-9090-25cbaf54b9c2)

![download](https://github.com/user-attachments/assets/4947dd89-2604-4290-a977-1c3e07ffe391)

![download](https://github.com/user-attachments/assets/2d3d176b-dd68-4e6d-bf38-0a18c009614f)

## Implikasi
Strategi Operasional
  * Peningkatan layanan selama musim puncak dapat dilakukan untuk memenuhi permintaan yang tinggi.
  * Kebijakan promosi diperlukan pada musim dingin untuk mempertahankan jumlah penyewa.


Nama Anda
GitHub: @dwikrisnandi
