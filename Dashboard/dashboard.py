import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import statsmodels.formula.api as sm
from statsmodels.stats.anova import anova_lm
from statsmodels.tsa.seasonal import seasonal_decompose

df_hour = pd.read_csv('Dashboard/hour.csv')
df_day = pd.read_csv('Dashboard/day.csv')

# Streamlit app title
st.title("Bike Sharing Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
selected_analysis = st.sidebar.radio("Select Analysis:", 
                                    ["Correlation Analysis", "Hourly Rental", "Weekday Comparison", "Season Comparison", "Rental Trend"])


if selected_analysis == "Correlation Analysis":
    st.header("Correlation Analysis")
    st.subheader("Hourly Data")
    # Your existing correlation analysis code for df_hour (heatmap)
    numerical_features = df_hour.select_dtypes(include=['number']).columns
    numerical_features = numerical_features.drop(['instant'])
    corr_matrix = df_hour[numerical_features].corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
    plt.title('Korelasi Antar Kolom Dataset Hour')
    st.pyplot(plt)

    st.subheader("Daily Data")
    # Your existing correlation analysis code for df_day (heatmap)
    numerical_features = df_day.select_dtypes(include=['number']).columns
    numerical_features = numerical_features.drop(['instant'])
    corr_matrix = df_day[numerical_features].corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
    plt.title('Korelasi Antar Kolom Dataset day')
    st.pyplot(plt)


elif selected_analysis == "Hourly Rental":
    st.header("Hourly Rental Analysis")

    # Your existing hourly rental analysis code (bar plot)
    hourly_rentals = df_hour.groupby('hr')['cnt'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='hr', y='cnt', data=hourly_rentals, palette='viridis')
    plt.title('Jumlah Penyewa Berdasarkan Jam')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Penyewa')
    plt.xticks(range(0, 24))
    plt.grid(axis='y')
    st.pyplot(plt)


elif selected_analysis == "Weekday Comparison":
    st.header("Weekday Comparison")

    # Your existing weekday comparison code (bar plot)
    weekday_comparison = df_day.groupby(['weekday', 'workingday', 'holiday'])['cnt'].mean().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(data=weekday_comparison, x='weekday', y='cnt', hue='workingday')
    plt.title("Perbandingan Weekdays, Working Days, and Holidays")
    plt.xlabel("Hari (0 = Hari Minggu)")
    plt.ylabel("Rata-rata")
    plt.legend(title="(1 = Hari Kerja)")
    st.pyplot(plt)


elif selected_analysis == "Season Comparison":
    st.header("Season Comparison")

    # Your existing season comparison code (bar plot)
    season_comparison = df_day.groupby('season')['cnt'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=season_comparison, x='season', y='cnt', palette='viridis')
    plt.title('Rata-rata Jumlah Penyewa Berdasarkan Musim')
    plt.xlabel('Musim (1: Musim Semi, 2: Musim Panas, 3: Musim Gugur, 4: Musim Dingin)')
    plt.ylabel('Rata-rata Jumlah Penyewa')
    st.pyplot(plt)


elif selected_analysis == "Rental Trend":
    st.header("Rental Trend Analysis")

    # Your existing rental trend analysis code (line plot with rolling average)
    daily_rentals = df_day.groupby('dteday')['cnt'].sum()
    plt.figure(figsize=(12, 6))
    plt.plot(daily_rentals.index, daily_rentals.values)
    plt.title('Tren Penyewaan Sepeda Harian')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Penyewaan')
    plt.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(plt)

    rolling_average = daily_rentals.rolling(window=30).mean()
    plt.figure(figsize=(12, 6))
    plt.plot(daily_rentals.index, daily_rentals.values, label='Jumlah Penyewaan Harian')
    plt.plot(rolling_average.index, rolling_average.values, label='Rata-rata Bergerak 30 Hari', color='red')
    plt.title('Tren Penyewaan Sepeda Harian dengan Rata-rata Bergerak')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Penyewaan')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)

    # Dekomposisi
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    df_day.set_index('dteday', inplace=True)
    decomposition = seasonal_decompose(df_day['cnt'], model='additive', period=30)
    fig = decomposition.plot()
    fig.set_size_inches(14, 8)
    plt.suptitle('Dekomposisi Deret Waktu Penyewaan Sepeda Harian', fontsize=16)
    st.pyplot(plt)
