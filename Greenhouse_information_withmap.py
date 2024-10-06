import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Main title
st.title("Greenhouse Gas Effects: CO₂ and CH₄")

# Two columns for images at the top
col1, col2 = st.columns(2)

with col1:
    st.image("C:/Users/bahce/Pictures/Screenshots/aspdasd.png", use_column_width=True)
with col2:
    st.image("C:/Users/bahce/Pictures/Screenshots/Ekran görüntüsü 2024-10-06 124748.png", use_column_width=True)

# Introduction
st.markdown("""
**Greenhouse gases** are gases that contribute to the warming of the Earth by trapping heat in the atmosphere; among them, carbon dioxide and methane are the most significant.
""")

# Create tabs for CO₂, CH₄, and Map
tab1, tab2, tab3 = st.tabs(["CO₂", "CH₄", "Map"])

# CO₂ Tab
with tab1:
    st.subheader("Carbon Dioxide (CO₂)")
    st.markdown("""
    **CO₂** is the most common greenhouse gas. Human activities such as the burning of fossil fuels (coal, oil, natural gas) and deforestation increase CO₂ emissions.
    """)
    
    # Data for CO₂ emissions from 1990 to 2021
    data_co2 = {
        'Year': [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 
                 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 
                 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 
                 2019, 2020, 2021],
        'CO2 Emissions (Million Tonnes)': [
            151.6, 158.1, 164.1, 171.1, 167.6, 
            181.4, 199.6, 212.1, 212.1, 207.9, 
            229.9, 213.6, 221.2, 236.8, 244.8, 
            264.9, 282.4, 313.7, 310.6, 316.4, 
            316.2, 342.1, 356.1, 347.3, 364.0, 
            384.9, 406.0, 430.9, 422.1, 402.7, 
            412.9, 452.7
        ]
    }
    
    # Create a DataFrame
    df_co2 = pd.DataFrame(data_co2)
    
    # Create a line chart using Plotly
    fig_co2 = px.line(df_co2, x='Year', y='CO2 Emissions (Million Tonnes)', 
                      title='CO₂ Emissions Over the Years', 
                      markers=True)
    
    # Display the chart
    st.plotly_chart(fig_co2)
    


# CH₄ Tab
with tab2:
    st.subheader("Methane (CH₄)")
    st.markdown("""
    **CH₄** is a more potent greenhouse gas than carbon dioxide. It is released into the atmosphere through natural gas production, agricultural activities (especially livestock), and the decomposition of organic waste in landfills.
    """)
    
    # Data for CH₄ emissions from 1990 to 2021
    data_ch4 = {
        'Year': [1990, 1995, 2000, 2005, 2010, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
        'Emissions (Thousand Tonnes)': [
            1699.5, 1704.5, 1746.7, 1806.9, 
            2065.8, 2111.4, 2223.3, 2272.7, 
            2416.4, 2528.7, 2555.8, 2560.8
        ]
    }
    
    # Create a DataFrame
    df_ch4 = pd.DataFrame(data_ch4)
    
    # Create a line chart using Plotly
    fig_ch4 = px.line(df_ch4, x='Year', y='Emissions (Thousand Tonnes)', 
                      title='CH₄ Emissions Over the Years', 
                      markers=True)
    
    # Display the chart
    st.plotly_chart(fig_ch4)

# Map Tab
with tab3:
    st.subheader("GHG Center CO₂ and CH₄ Map")
    
    latitude = 0  
    longitude = 0  
    zoom_start = 2  
    
    co2 = st.checkbox("Show CO₂ Layer", value=True)
    ch4 = st.checkbox("Show CH₄ Layer", value=False)
    
    m = folium.Map(location=[latitude, longitude], zoom_start=zoom_start, tiles=None)
    
    co2_tile_url = "https://earth.gsfc.nasa.gov/ghgcenter/api/raster/searches/66188a19a80c7f68a5bfa71f60026713/tiles/WebMercatorQuad/{z}/{x}/{y}?assets=xco2&colormap_name=magma&rescale=412%2C422"
    
    ch4_tile_url = "https://earth.gsfc.nasa.gov/ghgcenter/api/raster/searches/ac178c9e3d4f069d1334475c7febad34/tiles/WebMercatorQuad/{z}/{x}/{y}?assets=ensemble-mean-ch4-wetlands-emissions&colormap_name=magma&rescale=0%2C3e-9"
    
    if co2:
        folium.TileLayer(
            tiles=co2_tile_url,
            attr='GHG Center API',
            name='CO₂ Tiles',
            overlay=True,
            control=True,
            max_zoom=9,
            min_zoom=0,
            tile_size=256
        ).add_to(m)
    
    if ch4:
        folium.TileLayer(
            tiles=ch4_tile_url,
            attr='GHG Center API',
            name='CH₄ Tiles',
            overlay=True,
            control=True,
            max_zoom=9,
            min_zoom=0,
            tile_size=256
        ).add_to(m)
    
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='OpenStreetMap',
        name='OpenStreetMap Transparent',
        overlay=True,
        control=True,
        opacity=0.5
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    
    st_data = st_folium(m, width=800, height=600)
    
# Conclusion or further content
st.markdown("""
### **How Are Greenhouse Gases Produced?**

1. **Burning of Fossil Fuels**: The consumption of fuel in vehicles and the use of coal for electricity generation result in carbon dioxide emissions.
2. **Agricultural Activities**: Livestock farming produces methane gas, while the use of fertilizers leads to nitrous oxide emissions.
3. **Industrial Production**: Carbon dioxide and fluorinated gases are released during chemical processes and the production of certain products.
4. **Waste**: The decomposition of organic waste in landfills produces methane gas.
5. **Deforestation**: Trees absorb CO₂, so cutting them down reduces the Earth's capacity to absorb excess CO₂ from the atmosphere.
6. **Energy Consumption**: Increased energy use in homes and businesses contributes to higher CO₂ emissions.

**Note**: Greenhouse gases can also come from natural sources such as volcanic eruptions and the respiration of animals.

**Also**: Additionally, the burning of biomass and wildfires can release significant amounts of carbon dioxide and other greenhouse gases.
""")

# Question and Answer section at the bottom
st.markdown("### Questions and Answers")

with st.expander("Question 1: What is the main source of CO₂ emissions?"):
    st.write("**Answer**: The main source of CO₂ emissions is the burning of fossil fuels such as coal, oil, and natural gas for energy and transportation.")

with st.expander("Question 2: Why is CH₄ considered more potent than CO₂?"):
    st.write("**Answer**: Methane (CH₄) is considered more potent than CO₂ because it has a higher global warming potential, meaning it traps more heat in the atmosphere per molecule than CO₂ over a 100-year period.")

with st.expander("Question 3: How do agricultural activities contribute to greenhouse gas emissions?"):
    st.write("**Answer**: Agricultural activities contribute to greenhouse gas emissions through livestock farming, which produces methane, and the use of fertilizers, which leads to nitrous oxide emissions.")

with st.expander("Question 4: What natural sources produce greenhouse gases?"):
    st.write("**Answer**: Natural sources such as volcanic eruptions, the respiration of animals, and the decomposition of organic matter produce greenhouse gases.")

with st.expander("Question 5: How does deforestation affect CO₂ levels?"):
    st.write("**Answer**: Deforestation reduces the number of trees that can absorb CO₂, leading to higher concentrations of CO₂ in the atmosphere.")

with st.expander("Question 6: What role do wildfires play in greenhouse gas emissions?"):
    st.write("**Answer**: Wildfires release significant amounts of carbon dioxide and other greenhouse gases into the atmosphere, contributing to global warming.")

# Text area for feedback input
feedback = st.text_area("**Submit Your Solutions for Greenhouse Gases and Feedback for the Site:**", "")

# Submit button for feedback
if st.button("Submit"):
    if feedback:
        # Here, you can add the feedback to a data structure for storage
        # For example, we can temporarily use a list
        try:
            # Create a DataFrame to store feedback
            if 'feedbacks' not in st.session_state:
                st.session_state['feedbacks'] = []

            # Save the feedback
            st.session_state['feedbacks'].append(feedback)

            # Success message for the user
            st.success("Your feedback has been successfully recorded!")
        except Exception as e:
            st.error(f"An error occurred while recording your feedback: {e}")
    else:
        st.warning("Please enter your feedback.")

# Display
