import streamlit as st
import requests
import json
from docx import Document
from docx.shared import Inches
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Asistente Legal de Guatemala", page_icon="🇬🇹", layout="wide")

# Título de la aplicación
st.title("Asistente Legal de Guatemala 🇬🇹⚖️")

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

def generar_respuesta(prompt, contexto):
    url = "https://api.together.xyz/inference"
    payload = json.dumps({
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": f"Contexto: {contexto}\n\nPregunta: {prompt}\n\nResponde la pregunta basándote en el contexto proporcionado y tu conocimiento general sobre las leyes de Guatemala. Si no tienes suficiente información, indica que no puedes responder con certeza.\n\nRespuesta:",
        "max_tokens": 5512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["Pregunta:"]
    })
    headers = {
        'Authorization': f'Bearer {TOGETHER_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['output']['choices'][0]['text'].strip()

def create_docx(pregunta, respuesta, fuentes):
    doc = Document()
    doc.add_heading('Asistente Legal de Guatemala', 0)

    doc.add_heading('Pregunta', level=1)
    doc.add_paragraph(pregunta)

    doc.add_heading('Respuesta', level=1)
    doc.add_paragraph(respuesta)

    doc.add_heading('Fuentes', level=1)
    for fuente in fuentes:
        doc.add_paragraph(fuente, style='List Bullet')

    doc.add_paragraph('\nNota: Este documento fue generado por un asistente de IA. Verifica la información con fuentes oficiales o un abogado para asuntos legales importantes.')

    return doc

# Estado de sesión para almacenar la respuesta y la calificación
if 'respuesta' not in st.session_state:
    st.session_state.respuesta = None
if 'fuentes' not in st.session_state:
    st.session_state.fuentes = []
if 'calificacion' not in st.session_state:
    st.session_state.calificacion = None

# Interfaz de usuario
pregunta = st.text_input("Ingresa tu pregunta sobre la ley de Guatemala:")

if st.button("Obtener respuesta"):
    if pregunta:
        with st.spinner("Buscando información y generando respuesta..."):
            # Buscar información relevante
            resultados_busqueda = buscar_informacion(pregunta)
            contexto = "\n".join([result.get('snippet', '') for result in resultados_busqueda.get('organic', [])])

            # Generar respuesta
            respuesta = generar_respuesta(pregunta, contexto)

            # Almacenar la respuesta y las fuentes en el estado de sesión
            st.session_state.respuesta = respuesta
            st.session_state.fuentes = [f"{resultado['title']}: {resultado['link']}" for resultado in resultados_busqueda.get('organic', [])[:3]]

            # Mostrar respuesta
            st.write("Respuesta:")
            st.write(respuesta)

            # Mostrar fuentes
            st.write("Fuentes:")
            for fuente in st.session_state.fuentes:
                st.write(f"- {fuente}")

            # Crear documento DOCX
            doc = create_docx(pregunta, respuesta, st.session_state.fuentes)

            # Guardar el documento DOCX en memoria
            docx_file = BytesIO()
            doc.save(docx_file)
            docx_file.seek(0)

            # Opción para exportar a DOCX
            st.download_button(
                label="Descargar resultados como DOCX",
                data=docx_file,
                file_name="respuesta_legal_guatemala.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

            # Sistema de feedback
            st.write("Califica la respuesta de 1 a 5, siendo 1 incorrecta y 5 correcta:")
            st.session_state.calificacion = st.slider("Calificación", 1, 5, 3)

            if st.button("Enviar feedback"):
                st.write(f"Gracias por tu feedback. Calificación: {st.session_state.calificacion}")

    else:
        st.warning("Por favor, ingresa una pregunta.")

# Mostrar la respuesta y las fuentes si están en el estado de sesión
if st.session_state.respuesta:
    st.write("Respuesta:")
    st.write(st.session_state.respuesta)

    st.write("Fuentes:")
    for fuente in st.session_state.fuentes:
        st.write(f"- {fuente}")

# Agregar información en el pie de página
st.markdown("---")
st.markdown("**Nota:** Este asistente utiliza IA para generar respuestas basadas en información disponible en línea. "
            "Siempre verifica la información con fuentes oficiales o un abogado para asuntos legales importantes.")
