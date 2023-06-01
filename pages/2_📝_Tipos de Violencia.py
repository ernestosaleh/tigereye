from datetime import datetime, date
import pandas as pd
import streamlit as st
import folium
import json
from streamlit_folium import folium_static
import branca

st.title("📝 Tipos de violencia.")

hoy = datetime.now()

col1, col2 = st.columns([3,1])

dfo=pd.read_csv("Page1.csv")
new_cols=["tipo", "fecha", "valor", "lugar"]
result_df=dfo.rename(columns={dfo.columns[i]: new_cols[i] for i in range(dfo.shape[1])})

result_df["fecha"] = pd.to_datetime(result_df["fecha"]).dt.date

violencia_rango = st.slider(
    "Rango de tiempo:",
    value=(datetime(2020, 1, 18), datetime(hoy.year, hoy.month, hoy.day)),
    format=("MM/YY"),

)

cities = {
    "Apodaca": "006", 
    "García": "018", 
    "San Pedro Garza García": "019",
    "Escobedo": "021",
    "Guadalupe": "026", 
    "Juárez": "031",
    "Monterrey": "039",
    "San Nicolás de los Garza": "046",
    "Santa Catarina": "048",
    "Juarez": "031",
    "Santiago": "049",
}

poblacion = {
    "006": 656464.0, 
    "018": 397205.0, 
    "019": "NULL",
    "021": 500000,
    "026": 643143.0, 
    "031": 500000,
    "039": 1142994.0,
    "046": 500000,
    "048": 306322.0,
    "049": 46784.0,
}

def calculate_values(violencia_rango,multiple, radio_valor):
    mask = (result_df['fecha'] > violencia_rango[0].date()) & (result_df['fecha'] <= (violencia_rango[1].date()))
    postdf = result_df.loc[mask]
    filtered_df = postdf[postdf['tipo'].isin(multiple)]
    filtered_df = filtered_df.groupby(['lugar'])['valor'].sum().reset_index()
    filtered_df["clave_municipio"]=filtered_df["lugar"].apply(lambda x: cities[x])
    filtered_df["percapita"] = (filtered_df["valor"] / filtered_df["clave_municipio"].map(poblacion)) * 1000
    variable = []

    if radio_valor == "Casos Percapita":
        variable = [int(filtered_df["percapita"].max()), "percapita"]
    else:
        variable = [int(filtered_df["valor"].max()), "valor"]

    colormap = branca.colormap.linear.YlOrRd_09.scale(0, variable[0])
    map = folium.Map(location=[25.651887, -100.370891], zoom_start=10)

    folium.Choropleth(
        geo_data="municipioszmm.geojson", 
        name='choropleth',
        data=filtered_df,
        columns=['clave_municipio', variable[1]],
        key_on='feature.properties.clave_municipio', 
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='N. de casos'
    ).add_to(map)
    
    folium_static(map)
   

with col2:
    radio_valor = st.radio(
        "Rasgo a considerar",
        ('N. de casos', 'Casos Percapita'),
        key="N. de personas",
    )

with col1:
    choice = ['Patrimonio', 'Familia', 'Libertad y Seguridad Sexual', 'Sociedad', 'Vida e Integridad Corporal', 'Libertad Personal', 'Otros Bienes Jurídicos Afectados (Del Fuero Común)']
    multiple = st.multiselect(
        'Violencia en:',
        choice,
        choice
    )

calculate_values(violencia_rango,multiple, radio_valor)