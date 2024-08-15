import streamlit as st
import requests

# Cargar las claves API desde los secrets
together_api_key = st.secrets["together"]["api_key"]
perplexity_api_key = st.secrets["perplexity"]["api_key"]

# Configuración de la aplicación
st.title("Asistente Legal de Guatemala")
st.write("Haz tus preguntas sobre las leyes de Guatemala.")

# Campo para ingresar la pregunta
pregunta = st.text_input("Escribe tu pregunta aquí:")

# Seleccionar la API a utilizar
api_seleccionada = st.selectbox("Selecciona la API:", ("Together", "Perplexity"))

# Función para consultar la API de Together
def consultar_together(pregunta):
    url = "https://api.together.xyz/v1/query"
    headers = {
        "Authorization": f"Bearer {together_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": pregunta
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("response", "No se pudo obtener una respuesta.")
    else:
        return "Error al consultar la API de Together."

# Función para consultar la API de Perplexity
def consultar_perplexity(pregunta):
    url = "https://api.perplexity.ai/v1/query"
    headers = {
        "Authorization": f"Bearer {perplexity_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": pregunta
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("response", "No se pudo obtener una respuesta.")
    else:
        return "Error al consultar la API de Perplexity."

# Botón para enviar la pregunta
if st.button("Consultar"):
    if pregunta:
        if api_seleccionada == "Together":
            respuesta = consultar_together(pregunta)
        else:
            respuesta = consultar_perplexity(pregunta)
        
        st.write("**Respuesta:**")
        st.write(respuesta)
    else:
        st.write("Por favor, escribe una pregunta.")
