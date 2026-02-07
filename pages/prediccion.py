#Librerías
import streamlit as st
import utils
import pandas as pd
import style

style.load_styles()

#Barra lateral
utils.generarMenu()

#Configuración de la página
st.set_page_config(page_title="Predicción",
                    page_icon="📈",
                    layout="wide")

#título
st.title("Predicción")

#cargar los datos
df = pd.read_csv("data/cleaned_data.csv", index_col=0)

# Controles de usuario pa nueva predicción
st.subheader("Herramienta de Predicción del Precio de un Vehículo")
st.markdown("Por favor seleccione las características del carro que desea conocer el precio estimado de venta:")
# === FILA 1: marca - modelo - versión - carrocería ===
col1, col2, col3, col4 = st.columns(4)

with col1:
    marcas = sorted(df["make"].unique())
    marca = st.selectbox("Marca", marcas)

with col2:
    modelos = sorted(df[df["make"] == marca]["model"].unique())
    modelo = st.selectbox("Modelo", modelos)

with col3:
    versiones = sorted(df[df["model"] == modelo]["trim"].unique())
    version = st.selectbox("Versión", versiones)

with col4:
    carrocerias = sorted(df[df["model"] == modelo]["body"].dropna().unique())
    carroceria = st.selectbox("Carrocería", carrocerias)


# === FILA 2: estado - kilometraje - botón ===
col5, col6, col7 = st.columns([2, 2, 1])

with col5:
    st.write("Condición del vehículo")
    colA, colB, colC = st.columns([2, 3, 2])
    with colA:
        st.markdown("Nuevo")
    with colB:
        condicion = st.slider("", 1, 49, 49)
    with colC:
        st.markdown("Malo")

with col6:
    kilometraje = st.number_input("Kilometraje", min_value=0)

with col7:
    st.write("")   # para alinear el botón
    st.write("")
    btn_ejecutar = st.button("Predecir", type="primary")

if btn_ejecutar:
    dict_input = {
        'make': [marca],
        'model': [modelo],
        'trim': [version],
        'body': [carroceria],
        'condition': [float(condicion)],
        'odometer': [float(kilometraje)]
    }
    df_input = pd.DataFrame(dict_input)
    utils.predecir(df_input)



