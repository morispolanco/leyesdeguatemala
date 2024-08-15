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

# Función para combinar las respuestas
def combinar_respuestas(respuesta_together, respuesta_perplexity):
    # Aquí podrías implementar lógica para combinar las respuestas.
    # Por ejemplo, podrías simplemente concatenarlas, elegir la más relevante,
    # o fusionarlas de alguna manera.
    respuesta_final = f"Together: {respuesta_together}\n\nPerplexity: {respuesta_perplexity}"
    return respuesta_final

# Botón para enviar la pregunta
if st.button("Consultar"):
    if pregunta:
        respuesta_together = consultar_together(pregunta)
        respuesta_perplexity = consultar_perplexity(pregunta)
        
        respuesta_final = combinar_respuestas(respuesta_together, respuesta_perplexity)
        
        st.write("**Respuesta:**")
        st.write(respuesta_final)
    else:
        st.write("Por favor, escribe una pregunta.")
