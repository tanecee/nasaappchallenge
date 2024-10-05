




'''

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Başlık ve açıklama
st.title("Interaktif Hava Durumu Görüntüleyici")
st.write("Harita üzerinde bir yere tıklayarak o konumun saatlik hava durumu verilerini görüntüleyebilirsiniz.")

# Session State ile tıklanan konumu saklama
if 'location' not in st.session_state:
    st.session_state['location'] = None

# Harita oluşturma ve tıklanan konumu alma kısmı kaldırıldı

# Sadece verileri gösteren sütun
if st.session_state['location'] is not None:
    # Veri çekme ve gösterme
    latitude = st.session_state['location'][0]
    longitude = st.session_state['location'][1]
    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,soil_temperature_0cm",
            "timezone": "auto"
        }

        api_url = "https://api.open-meteo.com/v1/forecast"
        response = requests.get(api_url, params=params)
        data = response.json()

        # Saatlik verileri alma
        hourly_data = data['hourly']
        df = pd.DataFrame(hourly_data)
        df['time'] = pd.to_datetime(df['time'])

        # Verileri gösterme
        st.subheader("Saatlik Hava Durumu Verileri")
        st.dataframe(df)

        # Grafikleri çizme
        st.subheader("Sıcaklık ve Rüzgar Hızı Grafiği")
        fig = px.line(df, x='time', y=['temperature_2m', 'wind_speed_10m'], labels={
            'time': 'Zaman',
            'value': 'Değer',
            'variable': 'Değişken'
        })
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Nem ve Toprak Sıcaklığı Grafiği")
        fig2 = px.line(df, x='time', y=['relative_humidity_2m', 'soil_temperature_0cm'], labels={
            'time': 'Zaman',
            'value': 'Değer',
            'variable': 'Değişken'
        })
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Veri alınırken hata oluştu: {e}")
else:
    st.write("Lütfen harita üzerinde bir konuma tıklayın.")




'''
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Başlık ve açıklama
st.title("Interaktif Hava Durumu Görüntüleyici")
st.write("Harita üzerinde bir yere tıklayarak o konumun saatlik hava durumu verilerini görüntüleyebilirsiniz.")

# Session State ile tıklanan konumu saklama
if 'location' not in st.session_state:
    st.session_state['location'] = None

# Uygulama düzeni için iki sütun oluşturma
col1, col2 = st.columns([1, 1])

with col1:
    # Haritayı oluşturma
    default_location = [41.015, 28.979]  # İstanbul koordinatları
    if st.session_state['location'] is not None:
        # Tıklanan konumu kullanarak haritayı oluştur
        m = folium.Map(location=st.session_state['location'], zoom_start=8)
        # İşaretçi ekleme
        folium.Marker(
            location=st.session_state['location'],
            tooltip="Seçilen Konum",
            icon=folium.Icon(color='red')
        ).add_to(m)
    else:
        # Varsayılan harita
        m = folium.Map(location=default_location, zoom_start=2)

    # Haritayı göster ve tıklama olaylarını yakala
    returned = st_folium(m, width=350, height=350)

    # Kullanıcı haritaya tıkladıysa
    if returned['last_clicked'] is not None:
        # Tıklanan konumu sakla
        st.session_state['location'] = [returned['last_clicked']['lat'], returned['last_clicked']['lng']]

        st.write(f"Tıklanan konum: Enlem {st.session_state['location'][0]:.4f}, Boylam {st.session_state['location'][1]:.4f}")

with col2:
    if st.session_state['location'] is not None:
        # Veri çekme ve gösterme
        latitude = st.session_state['location'][0]
        longitude = st.session_state['location'][1]
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "hourly": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,soil_temperature_0cm",
                "timezone": "auto"
            }

            api_url = "https://api.open-meteo.com/v1/forecast"
            response = requests.get(api_url, params=params)
            data = response.json()

            # Saatlik verileri alma
            hourly_data = data['hourly']
            df = pd.DataFrame(hourly_data)
            df['time'] = pd.to_datetime(df['time'])

            # Verileri gösterme
            st.subheader("Saatlik Hava Durumu Verileri")
            st.dataframe(df)

            # Grafikleri çizme
            st.subheader("Sıcaklık ve Rüzgar Hızı Grafiği")
            fig = px.line(df, x='time', y=['temperature_2m', 'wind_speed_10m'], labels={
                'time': 'Zaman',
                'value': 'Değer',
                'variable': 'Değişken'
            })
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Nem ve Toprak Sıcaklığı Grafiği")
            fig2 = px.line(df, x='time', y=['relative_humidity_2m', 'soil_temperature_0cm'], labels={
                'time': 'Zaman',
                'value': 'Değer',
                'variable': 'Değişken'
            })
            st.plotly_chart(fig2, use_container_width=True)

        except Exception as e:
            st.error(f"Veri alınırken hata oluştu: {e}")
    else:
        st.write("Lütfen harita üzerinde bir konuma tıklayın.")
