#Librerías
import streamlit as st
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pickle import dump, load
import numpy as np
import joblib
import json

#Función para la barra lateral sidebar
def generarMenu():
    with st.sidebar:
        logo = Image.open("media/TalentoTech.png") 
        st.image(logo)
        st.header("Menú")
        #mostramos una lista personalizada de mis páginas
        st.page_link('app.py', label='Inicio', icon='🏠')
        st.page_link('pages/graficos.py', label='Gráficos', icon='📊')
        st.page_link('pages/prediccion.py', label='Predicción', icon='📈')
        st.markdown("---")
        st.markdown("### 🌐 Recursos externos")
        st.markdown(
            '<a href="https://portafolio-alejandro-castaneda.vercel.app/" target="_blank">🔗 Portafolio Alejandro</a>',
            unsafe_allow_html=True
        )

def transform_arreglo(df_input):
    df = df_input.copy()

    # ---- Cargar encodings categóricos ----
    with open("data/make_encoding.json", "r", encoding="utf-8") as f:
        make_enc = json.load(f)

    with open("data/model_encoding.json", "r", encoding="utf-8") as f:
        model_enc = json.load(f)

    with open("data/trim_encoding.json", "r", encoding="utf-8") as f:
        trim_enc = json.load(f)

    with open("data/body_encoding.json", "r", encoding="utf-8") as f:
        body_enc = json.load(f)

    # ---- Reemplazar categorías por encoding ----
    df["make"] = df["make"].map(make_enc)
    df["model"] = df["model"].map(model_enc)
    df["trim"] = df["trim"].map(trim_enc)
    df["body"] = df["body"].map(body_enc)

    # ---- Manejo de valores no vistos ----
    df.fillna(0.0, inplace=True)

    # ---- Normalizar odometer ----
    with open("data/odometer_scaler.json", "r") as f:
        odo_limits = json.load(f)

    odo_min = odo_limits["min"]
    odo_max = odo_limits["max"]

    df["odometer"] = (df["odometer"] - odo_min) / (odo_max - odo_min)
    df["odometer"] = df["odometer"].clip(0, 1)

    # ---- Normalizar condition ----
    with open("data/condition_scaler.json", "r") as f:
        con_limits = json.load(f)

    con_min = con_limits["min"]
    con_max = con_limits["max"]

    df["condition"] = (df["condition"] - con_min) / (con_max - con_min)
    df["condition"] = df["condition"].clip(0, 1)

    return df

def predecir(df_input):
    df_trans = transform_arreglo(df_input)
    model = joblib.load("data/price_model.pkl")
    price = model.predict(df_trans)[0]

    price = round(price, -2)

    st.markdown("El precio estimado del vehículo es:")
    st.title(f"${price:,.0f}")

