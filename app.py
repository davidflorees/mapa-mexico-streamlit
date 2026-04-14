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
    df.columns = df.columns.astype(str).str.strip()

    st.write("Columnas detectadas:", df.columns.tolist())

    if "Estado" not in df.columns or "Convenio Status" not in df.columns:
        st.error("❌ El archivo debe contener las columnas 'Estado' y 'Convenio Status'.")
    else:
        df["Estado"] = df["Estado"].astype(str).str.strip()
        df["Convenio Status"] = df["Convenio Status"].astype(str).str.strip()

        # Normaliza posibles variantes
        df["Convenio Status"] = df["Convenio Status"].replace({
            "detenido": "Detenido",
            "en proceso": "En proceso",
            "firmado": "Firmado",
            "DETENIDO": "Detenido",
            "EN PROCESO": "En proceso",
            "FIRMADO": "Firmado"
        })

        colores = {
            "Detenido": "#d32f2f",
            "En proceso": "#f0e68c",
            "Firmado": "#1b5e20"
        }

        st.write("Valores únicos en Convenio Status:", df["Convenio Status"].unique())

        st.subheader("📊 Datos cargados:")
        st.dataframe(df)

        fig = px.choropleth(
            df,
            geojson=geojson,
            featureidkey="properties.name",
            locations="Estado",
            color="Convenio Status",
            color_discrete_map=colores,
            category_orders={"Convenio Status": ["Detenido", "En proceso", "Firmado"]},
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
