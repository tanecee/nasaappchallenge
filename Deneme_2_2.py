import streamlit as st
import requests
import pandas as pd
from streamlit_folium import st_folium
import folium
from math import radians, sin, cos, sqrt, atan2
import plotly.express as px

# Eğer bir API anahtarınız varsa buraya ekleyin
API_KEY = "YOUR_API_KEY"  # Eğer gerekliyse

st.title("Türkiye'de Atık Emisyonları")

def fetch_waste_data(country_code, sector, year, limit=1000, offset=0):
    url = "https://api.climatetrace.org/v4/country/emissions"
    params = {
        "country": 'TUR',  # 'TUR' olmalı
        "sector": 'Waste',  # Waste sektörü
        "since": 2020,  # Başlangıç yılı
        "to": 2022,  # Bitiş yılı
        "limit": limit,
        "offset": offset
    }
    headers = {}
    if API_KEY:
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
    response = requests.get(url, headers=headers, params=params)
    st.write(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        st.write("API Yanıtı:", data)
        return data.get('data', [])
    else:
        st.error(f"API Hatası: {response.status_code} - {response.text}")
        return None

# Dünya'nın yarıçapı ile mesafe hesaplama
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Seçilen konumun etrafındaki varlıkları bulma
def get_nearby_assets(df, clicked_lat, clicked_lon, radius_km):
    df['distance_km'] = df.apply(lambda row: calculate_distance(
        clicked_lat, clicked_lon, row['latitude'], row['longitude']), axis=1)
    nearby_assets = df[df['distance_km'] <= radius_km]
    return nearby_assets

# Emisyonları yıllara göre gruplama
def aggregate_emissions(nearby_assets):
    emissions_by_year = nearby_assets.groupby('year')['emissions_co2e_tonnes'].sum().reset_index()
    return emissions_by_year

# Grafiği çizme
def plot_emissions(emissions_by_year):
    fig = px.bar(emissions_by_year, x='year', y='emissions_co2e_tonnes',
                 labels={'year': 'Yıl', 'emissions_co2e_tonnes': 'Emisyonlar (Ton)'},
                 title='Yıllara Göre Atık Emisyonları')
    st.plotly_chart(fig, use_container_width=True)

# Türkiye'nin koordinatları
turkey_coords = [39.0, 35.0]

# Haritayı oluşturma
m = folium.Map(location=turkey_coords, zoom_start=6)

# Harita ve grafiklerin yan yana gösterilmesi
col1, col2 = st.columns(2)

with col1:
    st.subheader("Konum Seçimi")
    map_data = st_folium(m, width=350, height=350)

with col2:
    if map_data['last_clicked'] is not None:
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lon = map_data['last_clicked']['lng']
        st.write(f"Tıklanan konum: Enlem {clicked_lat:.4f}, Boylam {clicked_lon:.4f}")
        
        # Veri çekme ve işleme
        with st.spinner("Veriler alınıyor..."):
            assets = []
            for year in range(2015, 2022):
                data = fetch_waste_data('TUR', 'waste', year)  # 'TUR' geçerli kodu
                if data:
                    for asset in data:
                        asset['year'] = year
                    assets.extend(data)
            if assets:
                df_assets = pd.json_normalize(assets)
                st.write("Varlık Verileri:", df_assets)
                if 'latitude' in df_assets.columns and 'longitude' in df_assets.columns:
                    nearby_assets = get_nearby_assets(df_assets, clicked_lat, clicked_lon, radius_km=50)
                    if not nearby_assets.empty:
                        emissions_by_year = aggregate_emissions(nearby_assets)
                        plot_emissions(emissions_by_year)
                    else:
                        st.write("50 km içinde atık emisyonu varlığı bulunamadı.")
                else:
                    st.error("Varlık verilerinde enlem ve boylam bilgisi bulunamadı.")
            else:
                st.error("API'dan veri alınamadı veya veri boş.")
    else:
        st.write("Lütfen harita üzerinde bir konuma tıklayın.")
