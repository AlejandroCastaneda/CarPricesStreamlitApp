#Librerías
import streamlit as st
import utils
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import chi2_contingency
import plotly.express as px
from PIL import Image
import style

style.load_styles()

#Barra lateral
utils.generarMenu()

#Configuración de la página
st.set_page_config(page_title="Gráficos",
                    page_icon="📊",
                    layout="wide")

#título
st.title("Gráficos")

#mostramos los datos
df = pd.read_csv("data/cleaned_data.csv", index_col=0)
st.subheader("Dataset")
st.dataframe(df.head())
st.subheader("Estadísticas generales")
st.write(df.describe().T)

st.subheader("Análisis exploratorio")
# 1
# Crear la figura
fig, ax = plt.subplots(figsize=(15, 7))
sns.boxplot(data=df,
            x='transmission',
            y='sellingprice',
            hue='transmission',
            ax=ax)

# Mostrar en Streamlit
st.pyplot(fig)

# 2
# Calcular los colores más comunes
c = df['color'].value_counts().head(6)

# Crear la figura
fig, ax = plt.subplots()
ax.pie(x=c, labels=c.index, autopct='%0.2f%%')
ax.set_title("Colores más frecuentes de vehículos")

# Mostrar en Streamlit
st.pyplot(fig)

# 3
# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(10, 6))

# Mapa de calor de las correlaciones
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)

# Título
ax.set_title("Mapa de calor de correlaciones")

# Mostrar en Streamlit
st.pyplot(fig)

# 4
def cramers_v(x, y):
    """Calcula la correlación de Cramér's V entre dos variables categóricas"""
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))

def matriz_correlacion_categorica(df, categorical_cols):
    """Crea matriz de correlación para variables categóricas usando Cramér's V"""
    n = len(categorical_cols)
    corr_matrix = np.ones((n, n))

    for i in range(n):
        for j in range(i+1, n):
            corr_matrix[i, j] = cramers_v(df[categorical_cols[i]], df[categorical_cols[j]])
            corr_matrix[j, i] = corr_matrix[i, j]

    corr_df = pd.DataFrame(corr_matrix, index=categorical_cols, columns=categorical_cols)
    return corr_df

# --- USO EN STREAMLIT ---
categorical_cols = ['make', 'model', 'trim', 'body', 'transmission', 'state', 'color', 'interior']
matriz_cramer = matriz_correlacion_categorica(df, categorical_cols)

# Crear y mostrar la figura
fig = px.imshow(matriz_cramer, 
                text_auto=True, 
                color_continuous_scale="YlGnBu",
                title="Correlación entre variables categóricas (Cramér's V)")
st.plotly_chart(fig, use_container_width=True)

# 5
# Crear tabla pivote
g = df.pivot_table(
    index='year',
    values=['sellingprice', 'mmr'],
    aggfunc='median'
).reset_index()

# Crear y mostrar figura
fig = px.line(
    g,
    x='year',
    y=['sellingprice', 'mmr'],
    title="Tendencia de precios medianos por año",
    labels={'value': 'Precio (mediana)', 'year': 'Año'},
)
st.plotly_chart(fig, use_container_width=True)

# 6
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
for col in numeric_cols:
    with st.expander(f"📊 Distribución de {col}"):
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df[col].dropna(), kde=True, ax=ax)

        median = df[col].dropna().median()
        mean = df[col].dropna().mean()

        ax.axvline(mean, color='blue', linestyle='--', linewidth=2, label=f'Media: {mean:,.2f}')
        ax.axvline(median, color='red', linestyle='--', linewidth=2, label=f'Mediana: {median:,.2f}')
        ax.legend()
        ax.set_xlabel(col)
        ax.set_ylabel('Frecuencia')

        st.pyplot(fig)

# Clusters
logo = Image.open("media/clusters.jpeg") 
st.image(logo)

# modelo
st.subheader("Modelo")
logo = Image.open("media/modelo1.jpeg") 
st.image(logo)
logo = Image.open("media/modelo2.jpeg") 
st.image(logo)
logo = Image.open("media/modelo3.jpeg") 
st.image(logo)