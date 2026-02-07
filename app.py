#librerías
import streamlit as st
from PIL import Image
import utils
import style
style.load_styles()



#Configuración de la página
st.set_page_config(page_title="Mercado automovilístico",
                    page_icon="🏠",
                    layout="wide")

# Menú
utils.generarMenu()

# Página principal
st.title("💵 Análisis explicativo y predictivo del precio de los automóviles en EE.UU. entre 1982 y 2015")
logo = Image.open("media/portada.jpeg") 
st.image(logo)
st.write("""El mercado automotriz de vehículos usados en Estados Unidos representa uno de los sectores con mayor dinamismo y volumen de transacciones dentro de la industria del transporte. Entre 1982 y 2015, se observó un notable crecimiento en la cantidad de vehículos disponibles, así como una gran variabilidad en los precios, influenciada por factores como la marca, el modelo, la antigüedad, el kilometraje, el estado del vehículo y las condiciones del mercado. En este contexto, surge la necesidad de analizar y comprender los determinantes que afectan el precio de los automóviles, tanto desde una perspectiva explicativa como predictiva.
                """)

# Footer
footer_html = """
<style>
footer {visibility: hidden;}
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0E1117;
    color: white;
    text-align: center;
    padding: 10px 0;
    font-size: 14px;
    border-top: 1px solid #444;
}
.footer a {
    color: #00BFFF;
    text-decoration: none;
    margin: 0 10px;
}
.footer a:hover {
    text-decoration: underline;
}
</style>

<div class="footer">
    💻 Proyecto desarrollado por:
    <a href="https://www.linkedin.com/in/diego-alejandro-casta%C3%B1eda-ossa-947745283/" target="_blank">Alejandro</a> |
    <a href="https://www.linkedin.com/in/integrante2" target="_blank">Daniel</a> |
    <a href="https://www.linkedin.com/in/integrante3" target="_blank">Estiben</a> |
    <a href="https://www.linkedin.com/in/natalia-patricia-remolina-rodriguez-1327a8220/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app" target="_blank">Natalia</a> |
    <a href="https://www.linkedin.com/in/integrante5" target="_blank">Yuberth</a>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
