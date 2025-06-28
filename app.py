
import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Título de la app
st.set_page_config(page_title="Mapa Interactivo de México", layout="wide")
st.title("📍 Mapa de México por Estatus")
st.markdown("Sube un archivo Excel con los estados y estatus para visualizar el mapa dinámico.")

# Cargar GeoJSON
with open("estados_mexico.json", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Cargar Excel
uploaded_file = st.file_uploader("📄 Subir archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Validar columnas necesarias
    if "Estado" not in df.columns or "Estatus" not in df.columns:
        st.error("❌ El archivo debe contener las columnas 'Estado' y 'Estatus'.")
    else:
        # Colores personalizados
        colores = {
            "Integrado": "#10253f",     # Azul Rey
            "En proceso": "#f0bd0b",    # Naranja
            "Sin acción": "#c61a19"     # Rojo Carmesí
        }

        df["Color"] = df["Estatus"].map(colores)

        # Mostrar DataFrame
        st.subheader("📊 Datos cargados:")
        st.dataframe(df)

        # Crear el mapa
        fig = px.choropleth(
            df,
            geojson=geojson,
            featureidkey="properties.name",
            locations="Estado",
            color="Estatus",
            color_discrete_map=colores,
            scope="north america"
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

        # Mostrar el mapa
        st.subheader("🗺️ Mapa Interactivo:")
        st.plotly_chart(fig, use_container_width=True)

        # Botón para descargar HTML
        if st.button("💾 Exportar como HTML"):
            fig.write_html("mapa_mexico_estatus_custom.html")
            with open("mapa_mexico_estatus_custom.html", "rb") as f:
                st.download_button("Descargar archivo HTML", f, file_name="mapa_mexico_estatus.html")
