
import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Mapa Interactivo de México", layout="wide")
st.title("📍 Mapa de México por Estatus")
st.markdown("Sube un archivo Excel con los estados y estatus para visualizar el mapa dinámico.")

with open("estados_mexico.json", "r", encoding="utf-8") as f:
    geojson = json.load(f)

uploaded_file = st.file_uploader("📄 Subir archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    if "Estado" not in df.columns or "Estatus" not in df.columns:
        st.error("❌ El archivo debe contener las columnas 'Estado' y 'Estatus'.")
    else:
        colores = {
            "Integrado": "#10253f",
            "En proceso": "#f0bd0b",
            "Sin acción": "#c61a19"
        }

        df["Color"] = df["Estatus"].map(colores)

        st.subheader("📊 Datos cargados:")
        st.dataframe(df)

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

        st.subheader("🗺️ Mapa Interactivo:")
        st.plotly_chart(fig, use_container_width=True)

        # Botón para exportar a HTML
        if st.button("💾 Exportar como HTML"):
            fig.write_html("mapa_mexico_estatus_custom.html")
            with open("mapa_mexico_estatus_custom.html", "rb") as f:
                st.download_button("Descargar archivo HTML", f, file_name="mapa_mexico_estatus.html")

        # Botón para exportar a PNG
        if st.button("📷 Descargar imagen PNG"):
            fig.write_image("mapa_mexico.png")
            with open("mapa_mexico.png", "rb") as f:
                st.download_button("Descargar archivo PNG", f, file_name="mapa_mexico.png")
