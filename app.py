import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Mapa Interactivo de México", layout="wide")
st.title("📍 Mapa de México por Estatus")
st.markdown("Sube un archivo Excel con los estados y el estatus del convenio para visualizar el mapa dinámico.")

with open("estados_mexico.json", "r", encoding="utf-8") as f:
    geojson = json.load(f)

uploaded_file = st.file_uploader("📄 Subir archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, header=1)
    st.write("Columnas detectadas:", df.columns.tolist())
    
    if "Estado" not in df.columns or "Convenio Status" not in df.columns:
        st.error("❌ El archivo debe contener las columnas 'Estado' y 'Convenio Status'.")
    else:
        colores = {
            "Detenido": "#c61a19",
            "En proceso": "#EBDE7C",
            "Firmado": "#035223"
        }

        df["Color"] = df["Convenio Status"].map(colores)

        st.subheader("📊 Datos cargados:")
        st.dataframe(df)

        fig = px.choropleth(
            df,
            geojson=geojson,
            featureidkey="properties.name",
            locations="Estado",
            color="Convenio Status",
            color_discrete_map=colores,
            scope="north america"
        )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

        config = {
            "toImageButtonOptions": {
                "format": "png",
                "filename": "mapa_mexico",
                "scale": 2
            }
        }

        st.subheader("🗺️ Mapa Interactivo:")
        st.plotly_chart(fig, use_container_width=True, config=config)

        with st.expander("💾 Exportar como HTML"):
            fig_html = fig.to_html(full_html=True)
            st.download_button(
                "Descargar HTML interactivo",
                data=fig_html,
                file_name="mapa_mexico.html",
                mime="text/html"
            )
