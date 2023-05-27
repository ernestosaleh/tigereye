import streamlit as st
from datetime import datetime
from streamlit_folium import st_folium 
import folium
import json


#st.snow()

st.title("Violencia por delegacion.")

violencia_rango = st.slider(
    "Rango de tiempo:",
    value=(datetime(2020, 1, 18), datetime.now()),
    format=("YYYY-MM")
)

# center on Liberty Bell, add marker
m = folium.Map(location=[25.74741426208384, -100.29117763140721], zoom_start=12)

#2. definir color para cada estado xd.
def color_function(feature):
    if(feature == '006'):
        return '#FF5733'
    else:
        return '#008000'

folium.GeoJson(
    "municipioszmm.geojson", 
    name='geojson', 
    style_function= lambda feature: {'fillColor': color_function(feature['properties']['clave_municipio']), 'fillOpacity':0.5, 'weight':1}
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)