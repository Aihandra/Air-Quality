import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gdown

# Link Google Drive (dengan file ID)
file_id = "1B-hUyNMw4ytdvRwgaVuhkkfb3WAVyx4V"
url = f"https://drive.google.com/uc?export=download&id={file_id}"

# Nama file setelah diunduh
output = "AirQuality.csv"

# Download file
gdown.download(url, output, quiet=False)

# Baca CSV
df = pd.read_csv(output)
# Judul Dashboard
st.title("Dashboard Analisis Polusi Udara")
st.write("menampilkan analisis konsentrasi polutan, dan faktor-faktor yang mempengaruhinya")

# Menampilkan Statistik Deskriptif
st.header("Statistik Deskriptif")
included_columns = ["PM2.5",	"PM10",	"SO2",	"NO2",	"CO",	"O3",	"TEMP",	"PRES",	"DEWP",	"RAIN",	"wd",	"WSPM"]
st.write(df[included_columns].describe())

# Hubungan Suhu (TEMP) terhadap Polutan
st.header("Hubungan Suhu dengan Konsentrasi Polutan")
pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]

df_temp_pollution = df.groupby("TEMP")[pollutants].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
for pollutant in pollutants:
    sns.lineplot(data=df_temp_pollution, x="TEMP", y=pollutant, label=pollutant, ax=ax)

plt.xlabel("Suhu (°C)")
plt.ylabel("Konsentrasi Polutan")
plt.title("Hubungan Suhu dengan Konsentrasi Polutan")
plt.legend()
st.pyplot(fig)

# Dampak Kecepatan Angin terhadap Polutan
st.header("Dampak Kecepatan Angin terhadap Polutan")
df_wind_pollution = df.groupby("WSPM")[pollutants].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 6))
for pollutant in pollutants:
    sns.lineplot(data=df_wind_pollution, x="WSPM", y=pollutant, label=pollutant, ax=ax2)

plt.xlabel("Kecepatan Angin (m/s)")
plt.ylabel("Konsentrasi Polutan")
plt.title("Dampak Kecepatan Angin terhadap Konsentrasi Polutan")
plt.legend()
st.pyplot(fig2)

# fitur interaktif
st.header("Eksplorasi Data Kualitas Udara")
selected_pollutant = st.selectbox("Pilih jenis polutan:", pollutants)

# memilih variabel independen 
selected_variable = st.radio("variabel pengaruh:", ["Suhu (TEMP)", "Kecepatan Angin (WSPM)"])

# Plot sesuai dengan pilihan user
fig, ax = plt.subplots(figsize=(10, 6))

if selected_variable == "Suhu (TEMP)":
    df_temp_pollution = df.groupby("TEMP")[selected_pollutant].mean().reset_index()
    sns.lineplot(data=df_temp_pollution, x="TEMP", y=selected_pollutant, ax=ax, marker="o", color="b")
    plt.xlabel("Suhu (°C)")
    plt.title(f"Hubungan Suhu dengan Konsentrasi {selected_pollutant}")
else:
    df_wind_pollution = df.groupby("WSPM")[selected_pollutant].mean().reset_index()
    sns.lineplot(data=df_wind_pollution, x="WSPM", y=selected_pollutant, ax=ax, marker="o", color="r")
    plt.xlabel("Kecepatan Angin (m/s)")
    plt.title(f"Dampak Kecepatan Angin terhadap Konsentrasi {selected_pollutant}")

plt.ylabel(f"Konsentrasi {selected_pollutant}")
st.pyplot(fig)


# Lokasi dengan Polusi Terendah
st.header("Lokasi dengan Tingkat Polusi Terendah")
location_pollution = df.groupby('station')[pollutants].mean()
location_pollution["Total Pollution"] = location_pollution.sum(axis=1)

lowest_pollution_location = location_pollution["Total Pollution"].idxmin()
lowest_pollution_value = location_pollution["Total Pollution"].min()

st.write(f"**Lokasi dengan polusi terendah:** `{lowest_pollution_location}`")
st.write(f"**Total rata-rata konsentrasi polutan:** `{lowest_pollution_value:.2f}`")

# Visualisasi Lokasi dengan Polusi Terendah
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x=location_pollution.index, y=location_pollution["Total Pollution"], ax=ax3)
plt.xticks(rotation=45)
plt.xlabel("Lokasi")
plt.ylabel("Total Konsentrasi Polutan")
plt.title("Total Polusi Udara di Setiap Lokasi")
st.pyplot(fig3)

