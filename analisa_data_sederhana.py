# -*- coding: utf-8 -*-
"""Analisa data sederhana.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ExZNb8GN2OyCcwzo_LgRbjusgDpAMB36

# Proyek Analisis Data - DICODING

# Import Library yang dibutuhkan untuk data analsis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

"""# Data Wrangling

## Gathering Data
Pada kode dibawah ini dilakukan pengumpulan data, lebih tepatnya mengambil dataset publik dari `Kaggle` denga `API`
"""

# Membuat file kaggle.json dengan API token Anda
api_token = {"username":"krisnandi9998","key":"2d15c9eb5dd2bb51786765892d7218d9"}

# Membuat folder kaggle dan menyimpan token API
!mkdir -p ~/.kaggle
with open('/root/.kaggle/kaggle.json', 'w') as file:
    json.dump(api_token, file)

# Mengubah izin akses untuk file API
!chmod 600 ~/.kaggle/kaggle.json

# Unduh dataset menggunakan API Kaggle
!kaggle datasets download -d lakshmi25npathi/bike-sharing-dataset

"""setelah dilkukan pengunduhan data selanjutnya dilakuan unzip data untuk mengetahui dataset yang sudah kita unduh karena saat terunduk dalam bentuk `ZIP`"""

!unzip bike-sharing-dataset.zip

"""## Assessing Data

### Mengecek Data Awal


Pada proses assesing data yang pertama kita muat dahulu dataset kita kedalam dataframe, dan melihat informasi awal pada data kita
"""

df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')

df_day.info()
print('\n')
df_hour.info()

"""Dari tampilan di atas bisa diketahui dari data keduanya tidak ada nilai yang hilang dan beberapa informasi lain diantranya
1. Dataset `day.csv`
  * Memiliki 731 Baris dan 16 Kolom
  * Tipe Data
    * float64: 4 kolom (temp, atemp, hum, windspeed)
    * int64: 11 kolom (instant, season, yr, mnth, holiday, weekday, workingday, weathersit, casual, registered, cnt)
    * object: 1 kolom (dteday, yang menyimpan tanggal)

2. Dataset `hour.csv`
  * Memiliki 17379 Baris dan 17 Kolom
  * Tipe Data:
    * float64: 4 kolom (temp, atemp, hum, windspeed)
    * int64: 12 kolom (instant, season, yr, mnth, hr, holiday, weekday, workingday, weathersit, casual, registered, cnt)
    * object: 1 kolom (dteday)

### Mengecek Outlier
"""

# Mengatur gaya visualisasi
sns.set(style="whitegrid")

# Membuat boxplot untuk mendeteksi outlier di dataset harian
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.boxplot(data=df_day[['cnt', 'casual', 'registered', 'temp', 'hum', 'windspeed']])
plt.title('Outlier Detection - Day Dataset')
plt.ylabel('Values')

# Membuat boxplot untuk mendeteksi outlier di dataset per jam
plt.subplot(1, 2, 2)
sns.boxplot(data=df_hour[['cnt', 'casual', 'registered', 'temp', 'hum', 'windspeed']])
plt.title('Outlier Detection - Hour Dataset')
plt.ylabel('Values')

plt.tight_layout()
plt.show()

"""Boxplot dari kedua dataset tersebut berisikan informasi

1. Dataset `day.csv`
  * cnt (Total Penyewaan), casual (Pengguna Tidak Terdaftar), registered (Pengguna Terdaftar), temp (Suhu), hum (Kelembaban), dan windspeed (Kecepatan Angin) semuanya ditampilkan
  * Terdapat beberapa outlier yang terlihat pada variabel cnt, casual, dan registered, di mana nilaiNYA jauh lebih tinggi dibandingkan dengan data lainnya

2. Dataset `hour.csv`

  * Boxplot menunjukkan distribusi yang serupa, dengan adanya outlier pada variabel cnt dan casual
  * Beberapa nilai penyewaan juga menunjukkan adanya outlier, tetapi jumlahnya lebih sedikit dibandingkan dengan dataset `day.csv`

Setelah melihat berdasarkan visual, selanjutnya mencari tahu jumlah pasti dari outlier tersebut
"""

# Fungsi untuk menghitung jumlah outlier menggunakan metode IQR
def count_outliers(data, column):
    Q1 = data[column].quantile(0.25)  # Kuartil pertama
    Q3 = data[column].quantile(0.75)  # Kuartil ketiga
    IQR = Q3 - Q1  # Jarak interkuartil
    lower_bound = Q1 - 1.5 * IQR  # Batas bawah untuk outlier
    upper_bound = Q3 + 1.5 * IQR  # Batas atas untuk outlier
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]  # Data outlier
    return outliers.shape[0]  # Mengembalikan jumlah outlier

# Daftar kolom yang akan diperiksa untuk outlier
day_columns = ['cnt', 'casual', 'registered', 'temp', 'hum', 'windspeed']
hour_columns = ['cnt', 'casual', 'registered', 'temp', 'hum', 'windspeed']

# Menghitung jumlah outlier di dataset harian
day_outliers_count = {column: count_outliers(df_day, column) for column in day_columns}

# Menghitung jumlah outlier di dataset per jam
hour_outliers_count = {column: count_outliers(df_hour, column) for column in hour_columns}

day_outliers_count, hour_outliers_count

"""## Cleaning Data

Setelah di cek data oulier pada dataset ini lumayan banyak, selanjutnya kita coba untuk ganti data outlier tersebut

### Mengganti data outlier
"""

# Mengganti outlier dengan nilai median untuk setiap kolom yang memiliki outlier
def replace_outliers_with_median(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Mengganti nilai yang lebih kecil dari lower_bound atau lebih besar dari upper_bound dengan median
    median_value = data[column].median()
    data[column] = data[column].apply(lambda x: median_value if (x < lower_bound or x > upper_bound) else x)

# Mengganti outlier di dataset day
for column in day_columns:
    replace_outliers_with_median(df_day, column)

# Mengganti outlier di dataset hour
for column in hour_columns:
    replace_outliers_with_median(df_hour, column)

# Memeriksa kembali jumlah outlier setelah penggantian
day_outliers_count_after = {column: count_outliers(df_day, column) for column in day_columns}
hour_outliers_count_after = {column: count_outliers(df_hour, column) for column in hour_columns}

day_outliers_count_after, hour_outliers_count_after

"""Setelah dilakukan penggantian data outlier dengan nilai median, masih terdapat banyak banyak outlier pada dataset hour

selanjutanya sisa outlier dataset hour kita hapus dan biarkan outiler pada dataset day
"""

# Mengganti outlier di dataset day.csv dengan median
for column in day_columns:
    replace_outliers_with_median(df_day, column)

# Menghapus outlier di dataset hour.csv
def remove_outliers(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Menghapus outlier
    data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    return data

# Menghapus outlier dari setiap kolom di dataset hour
for column in hour_columns:
    df_hour = remove_outliers(df_hour, column)


day_outliers_count_after = {column: count_outliers(df_day, column) for column in day_columns}
hour_outliers_count_after = {column: count_outliers(df_hour, column) for column in hour_columns}

day_outliers_count_after, hour_outliers_count_after

# Mengatur gaya visualisasi
sns.set(style="whitegrid")

# Membuat boxplot untuk mendeteksi outlier di dataset harian
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.boxplot(data=df_day[['cnt', 'casual', 'registered', 'temp', 'hum', 'windspeed']])
plt.title('Outlier Detection - Day Dataset')
plt.ylabel('Values')

# Membuat boxplot untuk mendeteksi outlier di dataset per jam
plt.subplot(1, 2, 2)
sns.boxplot(data=df_hour[['cnt', 'casual', 'registered', 'temp', 'hum', 'windspeed']])
plt.title('Outlier Detection - Hour Dataset')
plt.ylabel('Values')

plt.tight_layout()
plt.show()

"""Jika dilihat dari grafik yang dihasilkan, dirasa cukup untuk mengatasi outlier ini dikarenakan tidak terlalu signifikan perbedaannya

# Exploratory Data Analysis (EDA)

Pertanyaan untuk analisis data [Bike Sharing Datase](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)
1. Bagaimana hubungan antara jam dan jumlah penyewa ?
2. Seperti apa perbandingan penyewa di weekday, workingday dan holiday ?
3. Pada musim apa penyewa paling tinggi ?
4. Bagaimana tren penyewaan sepeda ?
"""

df_hour.describe(include="all")

"""Dataset ini mencatat penyewaan sepeda berdasarkan waktu, kondisi cuaca, dan hari, mencakup 16.018 observasi dari tahun 2011-2012. Variabel penting meliputi musim, hari kerja, kondisi cuaca, serta suhu, kelembapan, dan kecepatan angin. Selain itu, data mencakup jumlah penyewaan dari pengguna kasual dan terdaftar. Statistik menunjukkan penyewaan sepeda bervariasi dengan rata-rata total penyewaan sekitar 152 sepeda per jam, dengan variasi yang cukup besar, mulai dari 1 hingga 590 sepeda. Dataset ini membantu memahami faktor-faktor yang memengaruhi pola peminjaman sepeda."""

df_day.describe(include="all")

"""Dataset ini terdiri dari 731 observasi yang mencatat penyewaan sepeda harian berdasarkan waktu, cuaca, dan kondisi lainnya. Variabel yang termasuk adalah tanggal (dteday), musim, tahun, bulan, hari libur, hari dalam seminggu, hari kerja, kondisi cuaca, suhu, kelembapan, dan kecepatan angin. Terdapat juga data jumlah pengguna kasual, pengguna terdaftar, dan total penyewaan sepeda (cnt). Rata-rata total penyewaan per hari adalah 4504 sepeda, dengan penyewaan minimum 22 dan maksimum 8714 sepeda. Distribusi data menunjukkan bahwa sebagian besar penyewaan terjadi pada hari-hari kerja dengan kondisi cuaca sedang dan suhu yang nyaman."""

# Ubah kolom 'dteday' menjadi objek datetime jika belum.
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Ekstrak fitur numerik untuk perhitungan korelasi.
# Kecualikan 'dteday', 'instant', dan kolom non-numerik lainnya.
numerical_features = df_hour.select_dtypes(include=['number']).columns
numerical_features = numerical_features.drop(['instant'])  # Hapus 'instant' jika tidak relevan untuk korelasi
corr_matrix = df_hour[numerical_features].corr()

# Plot heatmap korelasi
plt.figure(figsize=(12, 8))  # Atur ukuran gambar
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)

plt.title('Korelasi Antar Kolom Dataset Hour')  # Atur judul heatmap
plt.show()  # Tampilkan heatmap

"""Poin-poin penting dari matriks korelasi ini:
1. **Registered dan cnt** memiliki korelasi yang sangat tinggi (**0.91**), menunjukkan bahwa jumlah penyewa terdaftar sangat memengaruhi total penyewaan.
2. **Casual dan cnt** juga memiliki korelasi positif (**0.55**), namun lebih lemah dibandingkan dengan penyewa terdaftar.
3. **Temperature (temp, atemp)** menunjukkan korelasi positif moderat dengan total penyewaan (sekitar **0.38 dan 0.37**), menunjukkan bahwa semakin nyaman suhu, semakin tinggi jumlah penyewaan.
4. **Windspeed dan cnt** menunjukkan korelasi negatif (**-0.10**), artinya semakin tinggi kecepatan angin, semakin kecil kemungkinan orang akan menyewa sepeda.
5. **Humidity (hum)** memiliki korelasi negatif (**-0.32**) dengan jumlah penyewaan, artinya kelembapan yang lebih tinggi cenderung menurunkan jumlah penyewaan.
6. **Hr (jam)** menunjukkan korelasi yang cukup kuat dengan **casual** (**0.48**) dan **registered** (**0.44**), menunjukkan bahwa waktu dalam sehari memiliki dampak yang signifikan terhadap penyewaan sepeda.

"""

# Ubah kolom 'dteday' menjadi objek datetime jika belum.
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Ekstrak fitur numerik untuk perhitungan korelasi.
# Kecualikan 'dteday', 'instant', dan kolom non-numerik lainnya.
numerical_features = df_day.select_dtypes(include=['number']).columns
numerical_features = numerical_features.drop(['instant'])  # Hapus 'instant' jika tidak relevan untuk korelasi
corr_matrix = df_day[numerical_features].corr()

# Plot heatmap korelasi
plt.figure(figsize=(12, 8))  # Atur ukuran gambar
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)

plt.title('Korelasi Antar Kolom Dataset day')  # Atur judul heatmap
plt.show()  # Tampilkan heatmap

"""Poin-poin penting dari matriks korelasi ini:
1. **Registered dan cnt** memiliki korelasi sangat tinggi (**0.95**), menunjukkan bahwa jumlah penyewa terdaftar sangat berperan dalam total penyewaan.
2. **Casual dan cnt** memiliki korelasi moderat positif (**0.60**), menunjukkan hubungan yang signifikan tetapi tidak sekuat pengguna terdaftar.
3. **Temperature (temp, atemp)** menunjukkan korelasi kuat dengan total penyewaan (**0.63** untuk keduanya), yang berarti semakin nyaman suhu, semakin banyak orang yang menyewa sepeda.
4. **Windspeed** memiliki korelasi negatif dengan penyewaan sepeda (**-0.20**), menunjukkan bahwa kecepatan angin yang lebih tinggi cenderung menurunkan jumlah penyewaan.
5. **Humidity (hum)** juga menunjukkan korelasi negatif dengan penyewaan sepeda (**-0.12**), menunjukkan bahwa kelembapan yang lebih tinggi cenderung sedikit mengurangi jumlah penyewaan.
6. **Weathersit** (kondisi cuaca) memiliki korelasi negatif moderat dengan **cnt** (**-0.30**), artinya cuaca yang buruk menurunkan jumlah penyewaan sepeda.
7. **Season** memiliki korelasi positif moderat dengan **cnt** (**0.41**), menunjukkan bahwa musim tertentu, seperti musim panas, mendorong lebih banyak orang untuk menyewa sepeda.

# Analisis

### 1. Bagaimana Hubungan antara jam dan jumlah pengguna
"""

# Mengatur gaya visualisasi
sns.set(style="whitegrid")

# Menghitung jumlah penyewa berdasarkan jam
hourly_rentals = df_hour.groupby('hr')['cnt'].sum().reset_index()

# Membuat plot untuk hubungan antara jam dan jumlah penyewa
plt.figure(figsize=(12, 6))
sns.barplot(x='hr', y='cnt', data=hourly_rentals, palette='viridis')
plt.title('Jumlah Penyewa Berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewa')
plt.xticks(range(0, 24))  # Menampilkan semua jam
plt.grid(axis='y')
plt.show()

"""Gamabr di atas adalah visualisasi yang menunjukkan jumlah penyewa berdasarkan jam

* Sumbu X: Jam dalam sehari (dari 0 hingga 23).
* Sumbu Y: Jumlah penyewa (cnt) yang menyewa sepeda pada setiap jam.

Analisis Visual

* Grafik menunjukkan jam-jam puncak di mana jumlah penyewa meningkat, dan dapat membantu untuk memahami pola penggunaan sepeda sepanjang hari.
* Dapat dilihat jam-jam tertentu di mana penyewaan lebih tinggi, seperti pada pagi hari antara jam 8-10 dan sore hari antara jam 15-17, yang mungkin berkaitan dengan aktivitas kerja atau sekolah.
"""

# Langkah 1: Menghitung korelasi antara jam dan jumlah penyewa
correlation = hourly_rentals['hr'].corr(hourly_rentals['cnt'])

# Langkah 2: Menghitung statistik deskriptif
statistics = hourly_rentals['cnt'].describe()

correlation, statistics

"""#### Hasil Analisis
1. Korelasi

Korelasi antara jam dan jumlah penyewa: 0.64. Ini menunjukkan hubungan positif yang lumayan kuat antara jam dan jumlah penyewa. Artinya, seiring bertambahnya jam dalam sehari, jumlah penyewa cenderung meningkat lebih signifikan. Hal ini menunjukkan bahwa waktu berperan penting dalam menentukan pola penyewaan.

2. Statistik Deskriptif untuk Jumlah Penyewa (cnt)
* Count: 24 (jumlah jam yang diperiksa)
* Mean (Rata-rata): 101,693.88
* Standard Deviation (Standar Deviasi): 56,622.62
* Minimum: 4,428 (jumlah penyewa terendah di jam tertentu)
* 25th Percentile: 51,131.50
* Median (50th Percentile): 129,782.50
* 75th Percentile: 145,153.25
* Maximum: 174,963 (jumlah penyewa tertinggi di jam tertentu)

#### Interpretasi
* Rata-rata penyewa pada jam tertentu adalah 101,693.88, menunjukkan bahwa banyak pengguna sepeda beroperasi di waktu-waktu tertentu.
* Dengan standar deviasi sebesar 56,622.62, ini menunjukkan variasi yang signifikan dalam jumlah penyewa antar jamnya. Ini berarti ada jam-jam tertentu di mana penyewaan bisa sangat tinggi atau sangat rendah.

### 2. Seperti apa perbandingan penyewa di weekday, workingday dan holiday ?
"""

weekday_comparison = df_day.groupby(['weekday', 'workingday', 'holiday'])['cnt'].mean().reset_index()


plt.figure(figsize=(12, 6))
sns.barplot(data=weekday_comparison, x='weekday', y='cnt', hue='workingday')
plt.title("Perbandingan Weekdays, Working Days, and Holidays")
plt.xlabel("Hari (0 = Hari Minggu)")
plt.ylabel("Rata-rata")
plt.legend(title="(1 = Hari Kerja)")
plt.show()

"""Grafik perbandingan antara penyewa pada weekday (hari kerja), working day (hari efektif kerja), dan holiday (hari libur/non-kerja):

1. Working Day (Hari Kerja Efektif - Oranye)
    
  * Aktivitas penyewaan cukup stabil pada hari 1 hingga 5 (Senin hingga Jumat).
  * Penyewaan di hari kerja cenderung lebih tinggi dibandingkan dengan hari libur, terutama pada hari 2 (Selasa), 3 (Rabu), dan 4 (Kamis).

2. Non-Working Day (Libur - Biru)

  * Aktivitas penyewaan tetap terlihat signifikan pada hari Minggu (0), meski hari tersebut bukan hari kerja.
  * Hari 6 (Sabtu) juga menunjukkan penyewaan yang cukup tinggi, meski lebih rendah dibandingkan beberapa hari kerja efektif.

3. Puncak Aktivitas

  * Puncak aktivitas penyewaan terlihat pada hari Rabu (3), menunjukkan adanya pola lonjakan di tengah minggu, meskipun termasuk hari kerja.

4. Kesimpulan

  * Penyewaan cenderung lebih tinggi dan stabil pada hari kerja dibandingkan pada hari libur. Namun, akhir pekan (Minggu dan Sabtu) juga menunjukkan aktivitas yang tidak jauh berbeda, mengindikasikan permintaan yang kuat untuk aktivitas rekreasi atau layanan tertentu.
"""

import statsmodels.formula.api as sm
from statsmodels.stats.anova import anova_lm

# Analisis ANOVA untuk pengaruh hari kerja terhadap jumlah penyewa
model = sm.ols('cnt ~ C(workingday)', data=df_day).fit()
anova_table = anova_lm(model, typ=2)
print(anova_table)

# Analisis ANOVA untuk pengaruh hari dalam seminggu terhadap jumlah penyewa
model = sm.ols('cnt ~ C(weekday)', data=df_day).fit()
anova_table = anova_lm(model, typ=2)
print(anova_table)

"""Dari hasil di atas dapat disimpulkan

* ANOVA berdasarkan workingday: Tidak ditemukan perbedaan signifikan dalam rata-rata penyewaan antara hari kerja dan akhir pekan.
* ANOVA berdasarkan weekday: Tidak ada perbedaan signifikan dalam rata-rata penyewaan antara hari-hari dalam seminggu.

### 3. Pada musim apa penyewa paling tinggi ?
"""

season_comparison = df_day.groupby('season')['cnt'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=season_comparison, x='season', y='cnt', palette='viridis')
plt.title('Rata-rata Jumlah Penyewa Berdasarkan Musim')
plt.xlabel('Musim (1: Musim Semi, 2: Musim Panas, 3: Musim Gugur, 4: Musim Dingin)')
plt.ylabel('Rata-rata Jumlah Penyewa')
plt.show()

"""Grafik diatas menunjukkan rata-rata jumlah penyewa berdasarkan musim

1. Musim Semi (1)

    Memiliki jumlah penyewa terendah, dengan rata-rata sekitar 2500 penyewa.

2. Musim Panas (2)

    Terjadi peningkatan signifikan, dengan rata-rata jumlah penyewa mendekati 5000. Ini menunjukkan bahwa musim panas adalah salah satu periode dengan permintaan tinggi.

3. Musim Gugur (3)

    Puncak jumlah penyewa terjadi di musim ini, dengan rata-rata melebihi 5000. Ini mungkin mengindikasikan kondisi ideal untuk aktivitas luar ruangan atau rekreasi.

4. Musim Dingin (4)

    Jumlah penyewa sedikit menurun dibandingkan musim gugur, tetapi tetap lebih tinggi daripada musim semi, dengan rata-rata sekitar 4500.

Kesimpulan:

Musim gugur dan panas adalah periode dengan penyewaan tertinggi, sedangkan musim semi memiliki jumlah penyewa terendah. Ini mungkin mencerminkan pola musiman tertentu dalam permintaan layanan atau aktivitas yang disewakan, seperti rekreasi luar ruang yang lebih populer di cuaca hangat atau saat musim liburan.

### 4. Bagaimana tren penyewaan sepeda ?
"""

# Mengelompokkan data harian berdasarkan tanggal dan menghitung jumlah penyewaan
daily_rentals = df_day.groupby('dteday')['cnt'].sum()

# Membuat plot tren penyewaan sepeda
plt.figure(figsize=(12, 6))
plt.plot(daily_rentals.index, daily_rentals.values)
plt.title('Tren Penyewaan Sepeda Harian')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Penyewaan')
plt.grid(True)
plt.xticks(rotation=45)  # Memutar label sumbu x agar lebih mudah dibaca
plt.show()

# Analisis tren dengan rolling average (rata-rata bergerak)
rolling_average = daily_rentals.rolling(window=30).mean()  # Rata-rata bergerak 30 hari

plt.figure(figsize=(12, 6))
plt.plot(daily_rentals.index, daily_rentals.values, label='Jumlah Penyewaan Harian')
plt.plot(rolling_average.index, rolling_average.values, label='Rata-rata Bergerak 30 Hari', color='red')
plt.title('Tren Penyewaan Sepeda Harian dengan Rata-rata Bergerak')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Penyewaan')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()
plt.show()

"""**Penjelasan Grafik Pertama**
1. Tren Penyewaan Sepeda Harian
  * Grafik ini menunjukkan data harian penyewaan sepeda dari awal tahun 2011 hingga akhir 2012.
  * Terlihat adanya fluktuasi signifikan dari hari ke hari.
  * Ada beberapa pola musiman yang tampak
    * Peningkatan aktivitas mulai April hingga Oktober.
    * Penurunan tajam sekitar Desember hingga Februari.

2. Interpretasi
  * Musim panas dan awal gugur (sekitar Juli hingga September) menunjukkan aktivitas penyewaan tertinggi.
  * Musim dingin (akhir Desember hingga awal Februari) menampilkan penurunan signifikan, mungkin terkait dengan cuaca yang tidak mendukung aktivitas luar ruangan.

**Penjelasan Grafik Kedua**
1. Tren Penyewaan dengan Rata-rata Bergerak 30 Hari
  * Grafik ini menampilkan tren harian yang sama seperti grafik pertama, namun dengan tambahan garis rata-rata bergerak 30 hari (garis merah).
  * Garis merah ini memperhalus data harian untuk menunjukkan tren jangka panjang.

2. Temuan dari Grafik Kedua
  * Tren Umum: Ada pola peningkatan penyewaan dari awal 2011 hingga pertengahan 2011, diikuti oleh penurunan musiman saat musim dingin.
  * Pada tahun 2012, pola serupa terlihat: peningkatan signifikan mulai Maret dan mencapai puncak di Agustus–September, sebelum akhirnya menurun menjelang musim dingin.
  * Rata-rata bergerak menunjukkan tren kenaikan secara keseluruhan dari tahun 2011 hingga pertengahan 2012, tetapi dengan fluktuasi musiman.

**Kesimpulan**

Polarisasi Musiman penyewaan sepeda mencapai puncak selama bulan-bulan hangat (musim semi hingga awal musim gugur), sementara menurun drastis di musim dingin.
Rata-rata Bergerak membantu menunjukkan tren jangka panjang di luar fluktuasi harian. Ada peningkatan konsisten dalam penyewaan dari awal 2011 hingga pertengahan 2012, diikuti oleh penurunan musiman di akhir tahun 2012.
Grafik ini berguna untuk perencanaan bisnis, seperti mengidentifikasi waktu optimal untuk promosi atau penyediaan layanan tambahan, terutama saat permintaan sedang tinggi di musim panas dan gugur.

##### Menggunakan Dekomposisi untuk mengetahui tren
"""

# Menggunakan model dekomposisi aditif untuk mengurai komponen tren, musiman, dan residual
from statsmodels.tsa.seasonal import seasonal_decompose

# Konversi kembali kolom 'dteday' ke format datetime dan set sebagai index
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_day.set_index('dteday', inplace=True)

# Melakukan dekomposisi deret waktu dengan model aditif (periode 30 hari untuk pola musiman bulanan)
decomposition = seasonal_decompose(df_day['cnt'], model='additive', period=30)

# Memvisualisasikan hasil dekomposisi (Tren, Musiman, dan Residual)
fig = decomposition.plot()
fig.set_size_inches(14, 8)  # Mengatur ukuran grafik
plt.suptitle('Dekomposisi Deret Waktu Penyewaan Sepeda Harian', fontsize=16)  # Judul
plt.show()  # Menampilkan grafik

"""1. Tren Jangka Panjang

  Terdapat peningkatan signifikan dalam jumlah penyewaan sepeda dari awal 2011 hingga pertengahan 2012. Namun, setelah itu terlihat sedikit penurunan menjelang akhir 2012. Hal ini bisa dipengaruhi oleh faktor eksternal seperti perubahan musim, kebijakan, atau kondisi cuaca.

2. Pola Musiman

  Pola musiman menunjukkan adanya fluktuasi berulang setiap bulan. Ini mengindikasikan bahwa penggunaan sepeda dipengaruhi oleh pola bulanan atau cuaca—misalnya, penyewaan bisa lebih tinggi di hari-hari cerah dan menurun di hari dingin atau hujan.

3. Fluktuasi dan Anomali (Residual)

  Komponen residual memperlihatkan adanya variasi acak yang tidak dijelaskan oleh tren atau pola musiman. Ini bisa disebabkan oleh peristiwa tak terduga seperti hujan deras, perayaan hari libur besar, atau gangguan operasional.

4. Waktu Puncak dan Penurunan

  Penggunaan sepeda cenderung meningkat selama bulan-bulan hangat dan menurun di musim dingin, yang terlihat dari pola tren dan musiman.

Implikasi
* Peningkatan armada dan layanan bisa dilakukan selama musim puncak (seperti musim gugur).
* Kebijakan promosi atau penawaran khusus mungkin diperlukan di musim dingin atau saat penurunan tren untuk menjaga kestabilan penyewaan.
* Manajemen perlu siap menghadapi anomali dengan fleksibilitas operasional jika terjadi perubahan mendadak.
"""