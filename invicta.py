import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(page_title="Asistente Legal de Guatemala", page_icon="🇬🇹")

# Título de la aplicación
st.title("Asistente Legal de Guatemala")

# Acceder a las claves de API de los secretos de Streamlit
INVICTA_API_KEY = st.secrets["INVICTA_API_KEY"]

# ID del agente de IA (Agent ID)
AGENT_ID = 849a1645-54e1-4e08-b5a6-faf6777eefa8

# Configuración de la página
st.set_page_config(page_title="Asistente Legal de Guatemala", page_icon="🇬🇹")

# Título de la aplicación
st.title("Asistente Legal de Guatemala")

# Acceder a las claves de API de los secretos de Streamlit
INVICTA_API_KEY = st.secrets["INVICTA_API_KEY"]

# ID del agente de IA (Agent ID)
AGENT_ID = "849a1645-54e1-4e08-b5a6-faf6777eefa8"

def invicta_consulta(user_input):
    url = f"https://api.invictai.io/api/triggers/webhooks/api-key/{AGENT_ID}"
    payload = json.dumps({
        "userInput": user_input,
        "threadId": AGENT_ID,
        "modelName": "gpt-4",
        "variables": []
    })
    headers = {
        'Content-Type': 'application/json',
        'X-INVICTA-API': INVICTA_API_KEY
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

# Interfaz de usuario
pregunta = st.text_input("Ingresa tu pregunta sobre la ley de Guatemala:")

if st.button("Obtener respuesta"):
    if pregunta:
        with st.spinner("Consultando al asistente..."):
            # Realizar consulta a Invicta
            resultado = invicta_consulta(pregunta)

            # Mostrar respuesta
            st.write("Respuesta:")
            st.write(resultado)

    else:
        st.warning("Por favor, ingresa una pregunta.")

# Agregar información en el pie de página
st.markdown("---")
st.markdown("**Nota:** Este asistente utiliza IA para generar respuestas basadas en información disponible en línea. "
            "Siempre verifica la información con fuentes oficiales o un abogado para asuntos legales importantes.")
"

def invicta_consulta(user_input):
    url = f"https://api.invictai.io/api/triggers/webhooks/api-key/{AGENT_ID}"
    payload = json.dumps({
        "userInput": user_input,
        "threadId": AGENT_ID,
        "modelName": "gpt-4",
        "variables": []
    })
    headers = {
        'Content-Type': 'application/json',
        'X-INVICTA-API': INVICTA_API_KEY
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

# Interfaz de usuario
pregunta = st.text_input("Ingresa tu pregunta sobre la ley de Guatemala:")

if st.button("Obtener respuesta"):
    if pregunta:
        with st.spinner("Consultando al asistente..."):
            # Realizar consulta a Invicta
            resultado = invicta_consulta(pregunta)

            # Mostrar respuesta
            st.write("Respuesta:")
            st.write(resultado)

    else:
        st.warning("Por favor, ingresa una pregunta.")

# Agregar información en el pie de página
st.markdown("---")
st.markdown("**Nota:** Este asistente utiliza IA para generar respuestas basadas en información disponible en línea. "
            "Siempre verifica la información con fuentes oficiales o un abogado para asuntos legales importantes.")
