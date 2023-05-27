import streamlit as st
from datetime import datetime
from streamlit_folium import st_folium 
import folium

# 1. Crea un mapa
m = folium.Map(location=[25.74741426208384, -100.29117763140721], zoom_start=12)

# 2. Define una función de estilo
def style_function(feature):
    return {
        'fillColor': '#FF5733',  # reemplace '#color' con la lógica de color deseada
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5'
    }

folium.GeoJson(
    "municipioszmm.geojson", 
    name='geojson', 
    style_function= lambda feature: {'fillColor':'#FF5733', 'fillOpacity':0.9, 'weight':1}
).add_to(m)

# 4. Muestra el mapa en Streamlit
st_data = st_folium(m, width=725)