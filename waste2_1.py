import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# CSV dosyasını oku
df = pd.read_csv("C:/Users/bahce/Desktop/solid-waste-disposal_emissions_sources.csv")

# 'emissions_quantity' sütununu sayısal değere çevir ve NaN olmayanları tut
df['emissions_quantity'] = pd.to_numeric(df['emissions_quantity'], errors='coerce')

# NaN değerleri çıkar ve 'OpenStreetMap Landfill' kaydını filtrele
df = df.dropna(subset=['emissions_quantity'])
df = df[df['source_name'] != 'OpenStreetMap Landfill']

# 'emissions_quantity' sütununa göre çoktan aza sırala
sorted_df = df.sort_values(by='emissions_quantity', ascending=False)

# İlk 27 veriyi seç
top_10_data = sorted_df.head(27)

# Streamlit başlığı
st.title("Top 10 Emissions Quantity Locations on the Map")

# Folium haritası oluştur, merkezi bir konum belirle
map_center = [top_10_data['lat'].mean(), top_10_data['lon'].mean()]  # Merkez noktayı ortalama yapabilirsin
m = folium.Map(location=map_center, zoom_start=2)

# Her satır için haritaya marker ekle
for _, row in top_10_data.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=(f"Location: {row['source_name']}<br>Emissions Quantity: {row['emissions_quantity']}"),
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Haritayı Streamlit'te göster
st_folium(m, width=725, height=500)

st.subheader("Emissions Quantity Bar Chart")

# Yatay bar grafiği oluşturmak için Plotly kullan
fig = px.bar(top_10_data, y='source_name', x='emissions_quantity',
             labels={'source_name': 'Location', 'emissions_quantity': 'Emissions Quantity (Ton)'},
             title="Top 10 Emissions Quantity Locations",
             orientation='h')  # 'h' ile çubukları yatay yapıyoruz

# Grafiği Streamlit'te göster
st.plotly_chart(fig)
