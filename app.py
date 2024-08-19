import streamlit as st
import requests
import json
from docx import Document
from docx.shared import Inches
from io import BytesIO

# Configuración de la página con opciones adicionales para ocultar menús
st.set_page_config(
    page_title="Asistente Legal de Guatemala",
    page_icon="🇬🇹",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Ocultar el menú de Streamlit y el botón de GitHub
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Título de la aplicación
st.title("Asistente Legal de Guatemala")

# El resto del código permanece igual...
# Acceder a las claves de API de los secretos de Streamlit
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

def buscar_informacion(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query + " ley Guatemala"
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

# ... (el resto de las funciones y el código de la interfaz de usuario permanecen sin cambios)

# Agregar información en el pie de página
st.markdown("---")
st.markdown("**Nota:** Este asistente utiliza IA para generar respuestas basadas en información disponible en línea. "
            "Siempre verifica la información con fuentes oficiales o un abogado para asuntos legales importantes.")
