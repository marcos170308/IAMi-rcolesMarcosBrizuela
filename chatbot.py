
import streamlit as st
from groq import Groq
import os

st.set_page_config(
    page_title="Tu ChatBot",
    page_icon="🤖",
    layout="wide"
)

MODELOS = [
    'llama-3.1-8b-instant',
    'llama-3.3-70b-versatile',
    'deepseek-r1-distill-llama-70b'
]

def configurar_pagina():
    st.sidebar.title("Configuración de Tu ChatBot")
    elegirModelo = st.sidebar.selectbox(
        "Elegir un modelo",
        options=MODELOS,
        index=0
    )
    return elegirModelo

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    if not clave_secreta:
        st.error("❌ No se encontró la clave GROQ_API_KEY. Configurala en tu entorno.")
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=False
    )
    return respuesta.choices[0].message.content

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

st.title("Tu ChatBot 🤖")
st.write("Habla con tu chatbot aquí debajo:")

clienteUsuario = crear_usuario_groq()
inicializar_estado()
modelo = configurar_pagina()

mensaje = st.chat_input("✏️ Escribí tu mensaje:")

if mensaje:
    st.chat_message("user").write(mensaje)
    respuesta = configurar_modelo(clienteUsuario, modelo, mensaje)
    st.chat_message("assistant").write(respuesta)
